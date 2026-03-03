import gc
import json
import math
import numpy as np
import queue
import os
import threading
from tqdm import tqdm
from tifffile import imwrite
import time

from PySide6.QtCore import Signal, QObject

_STOP = object()

def _drain_queue(q: "queue.Queue"):
    try:
        while True:
            q.get_nowait()
    except queue.Empty:
        pass
    
# Container class for a single image frame, with optional timestamp and metadata
class ImageFrame:
    def __init__(self, buffer, file_data):
        self.buffer = buffer
        self.file_data = file_data

# Main class that handles image acquisition, saving, and live viewing in parallel threads
class AcquisitionWorker(QObject):
    new_volume_ready = Signal(np.ndarray, dict)  # signal Qt émis avec buffer + metadata
    
    def __init__(self, camera_worker, save_dir, n_steps, n_lines, n_channels,
             channel_names=None, mode = "ls3", images_per_file = 100, max_volume_queue=3, save_type="TIFF"):
        """
        Initialize the acquisition pipeline with multithreaded image reading, buffering, and saving.

        Parameters:
        - camera_worker: object
            An instance of a camera interface class providing a read_camera() method that returns image frames.
        
        - save_dir: str
            Path to the directory where TIFF stacks (volumes) will be saved on disk.
        
        - n_steps: int
            Number of image frames per lines
        
        - n_lines: int
            Number of lines to acquire during scanning.
        
        - channel_names: list of str, optional
            List of channel identifiers (e.g., ["GFP", "RFP"]) used for naming saved volumes. Defaults to ["CH"].
        
        - mode: str
            mode of acquisition, the only mode allowed is "ls3"
            
        - images_per_file : int
            nulmber of images per files saved
        
        - max_volume_queue: int
            Maximum number of volumes of images_per_files images allowed in the internal RAM buffer before being written to disk.
            This limits memory usage.
        
        - save_type:str, optional
            saves volumes as TIFF stacks; 'RAW' saves raw binary files with accompanying JSON metadata.
            Defaults to "TIFF"
        """
        super().__init__()
        self.camera = camera_worker
        self.save_dir = save_dir
        self.n_steps = n_steps
        self.n_lines = n_lines
        self.n_channels = n_channels # The final number of channel will be multiply by the number of lines
        self.channel_names = channel_names or ["CH"]
        self.mode = mode
        self.images_per_file = images_per_file
        self.max_volume_queue = max_volume_queue
        self.save_type = save_type.upper()

        self.n_volumes = self.n_channels * self.n_lines
        self.n_frames = self.n_steps * self.n_volumes
        self.file_per_volume = math.ceil(self.n_steps / self.images_per_file)
        self.n_files = self.file_per_volume * self.n_volumes
        self.images_in_last_file = self.n_steps - (self.file_per_volume - 1) * self.images_per_file #TODO a orriger ici

        self.stop_event = threading.Event()
        self.threads = []
        
        self.preview_callback = False
        self._preview_connected = False
        
        self.total_images = 0
        self.total_frames = 0
        self.total_dropped = 0
        self.total_volumes = 0
        self.total_files = 0
        self.start_time = None
        
        # Get shape from camera method
        self.image_shape = self.camera.get_image_shape()

        self.buffer_pool = queue.Queue()
        self.queue_to_save = queue.Queue()

        for _ in range(max_volume_queue):
            for _ in self.channel_names:
                buffer = np.empty((self.images_per_file, *self.image_shape), dtype=np.uint16)
                self.buffer_pool.put(buffer)

    def start(self):
        os.makedirs(self.save_dir, exist_ok=True)
        
                
        # Initialize tqdm bars
        self.frame_bar = tqdm(total=self.n_frames,
                              desc="Frames Acquired", position=0)
        self.file_bar = tqdm(total=self.n_files,
                             desc="Files Saved    ", position=1)
        self.volume_bar = tqdm(total=self.n_volumes,
                               desc="Volumes Saved  ", position=2)
        
        self.stop_event.clear()
        self.start_time = time.time()
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
        self.file_bar.close()
        self.volume_bar.close()
        
        self._print_stats()
        self._append_acquisition_summary()
        
                
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
        file_id = 0 # id of the file with images_per_file
        actual_volume = 0 # id of the volume, color by color
        channel_index = 0
        current_buffer = self.buffer_pool.get()
        slice_idx = 0
        current_channel = self.channel_names[channel_index]

        while not self.stop_event.is_set():
            frames = self.camera.read_camera()
            for frame in frames:
                
                # --------- Calcul du nombre d'images attendues pour ce volume ----------
                # Dernier volume : ne contiendra pas le même nombre d'images
                if file_id == self.file_per_volume - 1 :
                    expected_slices = self.images_in_last_file
                else:
                    expected_slices = self.images_per_file

                if slice_idx < expected_slices:
                    current_buffer[slice_idx] = frame
                    slice_idx += 1
                    self.total_frames += 1
                    self.frame_bar.update(1)
                
                if slice_idx == expected_slices:
                    
                    file_data = {
                        "file_id" : file_id,
                        "volume_id": volume_id,
                        "channel": current_channel,
                        "shape": current_buffer.shape
                    }
                        
                    # EMIT the volume as soon as it's filled
                            
                    if file_id == self.file_per_volume - 1:
                        # si c'est le dernier volume, il faut passer au channel suivant
                        if channel_index == len(self.channel_names) - 1:
                            volume_id += 1
                        channel_index = (channel_index + 1) % len(self.channel_names)
                        file_id = 0

                        if self.preview_callback:
                            self.new_volume_ready.emit(current_buffer[0:expected_slices-1], file_data)
                    else :
                        if self.preview_callback:
                            self.new_volume_ready.emit(current_buffer.copy(), file_data)
                        file_id +=1
                            
                    self.queue_to_save.put(ImageFrame(current_buffer, file_data))
                    
                    current_channel = self.channel_names[channel_index]
                    actual_volume += 1
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

            file_id = frame.file_data["file_id"]
            volume_id = frame.file_data["volume_id"]
            channel = frame.file_data["channel"]
            
            # Pour le dernier fichier, on ne récupérer qu'une partie des images du buffer
            if file_id == self.file_per_volume - 1 :
                file = frame.buffer[0:self.images_per_file-1]
            else:
                file = frame.buffer

            filename_base = os.path.join(self.save_dir, f"Position_{volume_id:04d}_{channel}_file_{file_id:04d}")
            if self.save_type == "TIFF":
                imwrite(f"{filename_base}.tif", file)
            elif self.save_type == "RAW":
                raw_path = f"{filename_base}.raw"
                json_path = f"{filename_base}.json"
                file.tofile(raw_path)
                metadata = {
                    "shape": list(file.shape),
                    "dtype": str(file.dtype),
                    "channel": channel,
                    "volume_id": volume_id,
                    "file_id" : file_id
                }
                with open(json_path, 'w') as jf:
                    json.dump(metadata, jf, indent=4)

            self.total_files += 1
            self.file_bar.update(1)
            
            if self.total_volumes != math.floor(self.total_files / self.file_per_volume) :
                self.total_volumes = math.floor(self.total_files / self.file_per_volume)
                self.volume_bar.update(1)
                
            self.buffer_pool.put(frame.buffer)   # recycle the buffer
            
    def set_preview_callback(self):
        """
        Register a function to be called with each new volume saved.
        Function must accept two arguments: buffer (ndarray), metadata (dict).
        The function is also connected to as Qt signal for Qt integration
        """
        self.preview_callback = True
        self._preview_connected = True
        # self.new_volume_ready.connect(callback_func)

    def _print_stats(self):
        elapsed = time.time() - self.start_time if self.start_time else 0
        print("\n=== Acquisition Stats ===")
        print(f"Total frames acquired : {self.total_frames}")
        print(f"Total frames dropped  : {self.total_dropped}")
        print(f"Total volumes saved   : {self.total_volumes}")
        print(f"Elapsed time (s)      : {elapsed:.2f}")
        if elapsed > 0:
            print(f"Effective FPS         : {self.total_frames / elapsed:.2f}")
            print(f"Volume rate (Hz)      : {self.total_volumes / elapsed:.2f}")
        print("========================\n")

    def _append_acquisition_summary(self):
        log_file = os.path.join(self.save_dir, "log.txt")
        try:
            with open(log_file, "a") as f:
                f.write("\n=== Acquisition Summary ===\n")
                f.write(f"Total frames acquired : {self.total_frames}\n")
                f.write(f"Total frames dropped  : {self.total_dropped}\n")
                f.write(f"Total volumes saved   : {self.total_volumes}\n")
                elapsed = time.time() - self.start_time if self.start_time else 0
                f.write(f"Elapsed time (s)      : {elapsed:.2f}\n")
                if elapsed > 0:
                    f.write(f"Effective FPS         : {self.total_frames / elapsed:.2f}\n")
                    f.write(f"Volume rate (Hz)      : {self.total_volumes / elapsed:.2f}\n")
                f.write("============================\n")
        except Exception as e:
            print(f"[WARNING] Could not write final stats to log.txt: {e}")
