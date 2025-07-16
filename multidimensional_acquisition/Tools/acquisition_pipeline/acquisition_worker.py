import json
import numpy as np
import queue
import os
import threading
from tqdm import tqdm
from tifffile import imwrite
import time


# Container class for a single image frame, with optional timestamp and metadata
class ImageFrame:
    def __init__(self, buffer, volume_id, channel):
        self.buffer = buffer
        self.volume_id = volume_id
        self.channel = channel

# Main class that handles image acquisition, saving, and live viewing in parallel threads
class AcquisitionWorker:
    def __init__(self, camera_worker, save_dir, n_steps, timepoints,
             channel_names=None, max_volume_queue=6, save_type="TIFF"):
        """
        Initialize the acquisition pipeline with multithreaded image reading, buffering, and saving.

        Parameters:
        - camera_worker: object
            An instance of a camera interface class providing a read_camera() method that returns image frames.
        
        - save_dir: str
            Path to the directory where TIFF stacks (volumes) will be saved on disk.
        
        - n_steps: int
            Number of image frames per volume (typically corresponding to Z-slices in a 3D acquisition).
        
        - timepoints: int
            Number of volumes to acquire (typically corresponding to time-lapse or sequential acquisitions).
        
        - channel_names: list of str, optional
            List of channel identifiers (e.g., ["GFP", "RFP"]) used for naming saved volumes. Defaults to ["CH"].
        
        - max_volume_queue: int
            Maximum number of volumes allowed in the internal RAM buffer before being written to disk. This limits memory usage.
        """
        
        self.camera = camera_worker
        self.save_dir = save_dir
        self.n_steps = n_steps
        self.timepoints = timepoints
        
        self.max_volume_queue = max_volume_queue
        self.channel_names = channel_names or ["CH"]
        self.save_type = save_type.upper()

        self.stop_event = threading.Event()
        self.threads = []
        
        self.total_images = 0
        self.total_frames = 0
        self.total_dropped = 0
        self.total_volumes = 0
        self.start_time = None
        
        # Get shape from camera method
        self.image_shape = self.camera.get_image_shape()

        self.buffer_pool = queue.Queue()
        self.queue_to_save = queue.Queue()

        for _ in range(max_volume_queue):
            for _ in self.channel_names:
                buffer = np.empty((n_steps, *self.image_shape), dtype=np.uint16)
                self.buffer_pool.put(buffer)

        self.frame_bar = tqdm(total=self.n_steps * self.timepoints * len(self.channel_names),
                              desc="Frames Acquired", position=0)
        self.volume_bar = tqdm(total=self.timepoints, desc="Volumes Saved", position=1)

    def start(self):
        os.makedirs(self.save_dir, exist_ok=True)
        self.stop_event.clear()
        self.start_time = time.time()
        self.threads = [
            threading.Thread(target=self.acquisition_loop, name="AcquisitionThread"),
            threading.Thread(target=self.saving_loop, name="SavingThread")
        ]
        for t in self.threads:
            t.start()

    def stop(self):
        self.stop_event.set()
        for t in self.threads:
            t.join()
        self.frame_bar.close()
        self.volume_bar.close()
        self._print_stats()
        self._append_acquisition_summary()

    def acquisition_loop(self):
        volume_id = 0
        channel_index = 0
        current_buffer = self.buffer_pool.get()
        slice_idx = 0
        current_channel = self.channel_names[channel_index]

        while not self.stop_event.is_set():
            frames = self.camera.read_camera()
            for frame in frames:
                if slice_idx < self.n_steps:
                    current_buffer[slice_idx] = frame
                    slice_idx += 1
                    self.total_frames += 1
                    self.frame_bar.update(1)
                
                if slice_idx == self.n_steps:
                    self.queue_to_save.put(ImageFrame(current_buffer, volume_id, current_channel))
                    channel_index = (channel_index + 1) % len(self.channel_names)
                    if channel_index == 0:
                        volume_id += 1
                    current_channel = self.channel_names[channel_index]
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
        while not self.stop_event.is_set() or not self.queue_to_save.empty():
            try:
                frame = self.queue_to_save.get(timeout=0.1)
                if not isinstance(frame, ImageFrame):
                    print(f"[ERROR] Unexpected object in save queue: {type(frame)}")
                    continue
                buffer = frame.buffer
                volume_id = frame.volume_id
                channel = frame.channel

                filename_base = os.path.join(self.save_dir, f"{channel}_volume_{volume_id:04d}")
                if self.save_type == "TIFF":
                    imwrite(f"{filename_base}.tiff", buffer)
                elif self.save_type == "RAW":
                    raw_path = f"{filename_base}.raw"
                    json_path = f"{filename_base}.json"
                    buffer.tofile(raw_path)
                    metadata = {
                        "shape": list(buffer.shape),
                        "dtype": str(buffer.dtype),
                        "channel": channel,
                        "volume_id": volume_id
                    }
                    with open(json_path, 'w') as jf:
                        json.dump(metadata, jf, indent=4)

                self.total_volumes += 1
                self.volume_bar.update(1)
                self.buffer_pool.put(buffer)  # recycle the buffer

            except queue.Empty:
                continue

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
