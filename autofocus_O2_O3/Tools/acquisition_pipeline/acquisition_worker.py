import gc
import matplotlib.pyplot as plt
import numpy as np
import queue
from pathlib import Path
import threading
from tqdm import tqdm
import time

from PySide6.QtCore import Signal, QObject

if __name__ == "__main__" and (__package__ is None or __package__ == ""):
    # Lancement en script : on relance en module pour activer les imports relatifs
    import sys

    pkg_root = Path(__file__).resolve().parent.parent  # dossier qui contient autofocus_02_03/
    sys.path.insert(0, str(pkg_root))
    
from image_analysis.Deskew_Numpy import deskew_numpy

_STOP = object()

def _drain_queue(q: "queue.Queue"):
    try:
        while True:
            q.get_nowait()
    except queue.Empty:
        pass
    
# Container class for a single image frame, with optional timestamp and metadata
class ImageFrame:
    def __init__(self, buffer, volume_id, channel):
        self.buffer = buffer
        self.volume_id = volume_id
        self.channel = channel

# Main class that handles image acquisition, saving, and live viewing in parallel threads
class AutofocusAcquisitionWorker(QObject):
    new_volume_ready = Signal(np.ndarray, dict)  # signal Qt émis avec buffer + metadata
    
    def __init__(self, camera_worker, channel_name, n_steps, n_positions, n_pixels = 10, px_shift = 0, max_volume_queue=10, interface = False):
        """
        Initialize the acquisition pipeline with multithreaded image reading, buffering, and saving.

        Parameters
        ----------
        camera_worker : object
            An instance of a camera interface class providing a read_camera() method that returns image frames.
        channel_name : str
            Name of the channel that is imaged for autofocus
        n_steps : int
            Number of image frames per volume (typically corresponding to Z-slices in a 3D acquisition).
        n_positions : int
            Number of piezo positions to acquire
        n_pixels : int, optional
            Number of pixels to average for autofocus. The default is 10.
        px_shift : int, optional
            Number of pixels for deskewing image. The default is 0.
        max_volume_queue : int, optional
            Maximum number of volumes allowed in the internal RAM buffer before being written to disk.
            This limits memory usage. The default is 10.
        interface : bool, optional
            If an external interface display the images, there is no need to display it from the worker
        """
        super().__init__()
        self.camera = camera_worker
        self.channel_name = channel_name
        self.n_steps = n_steps
        self.n_positions = n_positions
        self.max_px_intensity = [None] * self.n_positions
        self.n_pixels = n_pixels
        self.px_shift = px_shift
        
        self.max_volume_queue = max_volume_queue
        self.interface = interface

        self.n_frames = self.n_steps * self.n_positions
        self.frame_in_last_file = 0

        self.start_time = None

        self.stop_event = threading.Event()
        self.threads = []
        
        self.preview_callback = False
        self._preview_connected = False
        
        self.total_images = 0
        self.total_frames = 0
        self.total_dropped = 0
        self.total_volumes = 0
        
        # Get shape from camera method
        self.image_shape = self.camera.get_image_shape()

        self.buffer_pool = queue.Queue()
        self.queue_to_save = queue.Queue()

        for _ in range(max_volume_queue):
            buffer = np.empty((self.n_steps, *self.image_shape), dtype=np.uint16)
            self.buffer_pool.put(buffer)

    def start(self):      
        # Initialize tqdm bars
        self.frame_bar = tqdm(total=self.n_frames,
                              desc="Frames Acquired  ", position=0)
        self.volume_bar = tqdm(total=self.n_steps - 1, desc="Volumes Acquired ", position=1)
        
        self.stop_event.clear()
        self.threads = [
            threading.Thread(target=self.acquisition_loop, name="AcquisitionThread"),
            threading.Thread(target=self.saving_loop, name="SavingThread")
        ]
        for t in self.threads:
            t.start()

    def stop(self):
        # 1) stop threads
        self.stop_event.set()
        
        # 2) débloquer saving_loop quoi qu'il arrive
        try:
            self.queue_to_save.put_nowait(_STOP)
        except Exception:
            pass
        
        for t in self.threads:
            t.join()
        
        self.camera = None
        
        self.threads = []
        if self._preview_connected :
            try:
                self.new_volume_ready.disconnect()
            except:
                pass
            self._preview_connected = False
            
        # 3) fermer tqdm
        self.frame_bar.close()
        self.volume_bar.close()
                
        # 4) vider les queues (enlève toutes références restantes)
        _drain_queue(self.queue_to_save)
        _drain_queue(self.buffer_pool)
        
        # 5) casser les références aux gros ndarrays
        self.queue_to_save = None
        self.buffer_pool = None
        
        # 6) si preview Qt : attention, des copies peuvent encore être en transit
        #    (côté GUI). Ici, on fait au moins tomber le flag.
        self.preview_callback = False
        
        # 7) forcer GC
        gc.collect()

    def acquisition_loop(self):
        volume_id = 0 # id of the volume with all the colors
        current_buffer = self.buffer_pool.get()
        slice_idx = 0

        while not self.stop_event.is_set():
            frames = self.camera.read_camera()
            for frame in frames:
                
                expected_slices = self.n_steps

                if slice_idx < expected_slices:
                    current_buffer[slice_idx] = frame
                    slice_idx += 1
                    self.total_frames += 1
                    self.frame_bar.update(1)
                
                if slice_idx == expected_slices:
                    # EMIT the volume as soon as it's filled
                    if self.preview_callback:
                        
                        preview_data = {
                            "volume_id": volume_id,
                            "channel": self.channel_name,
                            "shape": current_buffer.shape
                        }
                        
                        self.new_volume_ready.emit(current_buffer.copy(), preview_data)
                        
                    self.queue_to_save.put(ImageFrame(current_buffer, volume_id, self.channel_name))

                    volume_id += 1
                    if not self.buffer_pool.empty():
                        current_buffer = self.buffer_pool.get()
                        slice_idx = 0
                    else:
                        self.total_dropped += 1
                        print("[WARNING] No available buffer, frame dropped", end='\r')
                        slice_idx = 0
                    self.total_images = self.total_frames + self.total_dropped

            time.sleep(0.001)

    def saving_loop(self):
        while True:
            try:
                frame = self.queue_to_save.get(timeout=0.1)
            except:
                if self.stop_event.is_set():
                    break
                continue
            
            if frame is _STOP:
                break
            
            if not isinstance(frame, ImageFrame):
                print(f"[ERROR] Unexpected object in save queue: {type(frame)}")
                continue
            
            buffer = frame.buffer[0 : self.n_steps] # To get the right number of images saved
            volume_id = frame.volume_id
            
            max_deskewed_image = np.max(deskew_numpy(buffer, px_shift_y=self.px_shift), axis = 0)
            
            if not self.interface :
                self.show_image(max_deskewed_image)
            
            max_deskewed_image = np.max(deskew_numpy(buffer, px_shift_y=self.px_shift), axis = 0).ravel()
            # ravel transfor 2d matrix into 1D matrix

            mean_top_px_intensity = np.mean(np.partition(max_deskewed_image, -self.n_pixels)[-self.n_pixels:])
            
            self.max_px_intensity[volume_id] = mean_top_px_intensity

            self.total_volumes += 1
            self.volume_bar.update(1)
                
            self.buffer_pool.put(buffer)   # recycle the buffer
            
    def show_image(self, image: np.ndarray) -> None:
        """
        Display a 2D NumPy array as an image.
    
        Parameters
        ----------
        image : np.ndarray
            2D image to display.
        """
        if image.ndim != 2:
            raise ValueError("image must be a 2D NumPy array.")
    
        plt.imshow(image, cmap="gray")
        plt.colorbar(label="Intensity")
        plt.tight_layout()
        plt.show()
    
    def get_max_px_intensity(self):
        return self.max_px_intensity
            
    def set_preview_callback(self):
        """
        Register a function to be called with each new volume saved.
        Function must accept two arguments: buffer (ndarray), metadata (dict).
        The function is also connected to as Qt signal for Qt integration
        """
        self.preview_callback = True
        self._preview_connected = True
        # self.new_volume_ready.connect(callback_func)
