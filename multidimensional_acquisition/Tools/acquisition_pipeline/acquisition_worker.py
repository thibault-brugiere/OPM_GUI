import threading
import queue
import time
import os
from tifffile import imwrite  # Pour l'export TIFF
import numpy as np

# Container class for a single image frame, with optional timestamp and metadata
class ImageFrame:
    def __init__(self, data, timestamp=None, metadata=None):
        self.data = data
        self.timestamp = timestamp or time.time()
        self.metadata = metadata or {}

# Main class that handles image acquisition, saving, and live viewing in parallel threads
# Main class that handles image acquisition, saving, and live viewing in parallel threads
class AcquisitionWorker:
    def __init__(self, camera_worker, save_dir, n_steps, timepoints,channel_names=None, max_volume_queue=5):
        """
        Initialize the acquisition pipeline.

        Parameters:
        - camera_worker: object
            Instance of a camera control class with a read_camera() method.
        - save_dir: str
            Path where TIFF stacks (volumes) will be saved.
        - n_steps: int
            Number of frames per volume (Z-slices).
        - channel_names: list of str, optional
            Names of the acquisition channels (e.g. ["GFP", "RFP"]). Used for file naming.
        - max_volume_queue: int
            Maximum number of volumes to store in RAM before saving.
        """
        self.camera = camera_worker  # Instance de la classe camera_worker (contrôle matériel caméra)
        self.save_dir = save_dir  # Répertoire où les images seront sauvegardées
        self.n_steps = n_steps  # Nombre d'images par volume
        self.timepoints = timepoints
        self.max_volume_queue = max_volume_queue
        self.max_queue_size = max_volume_queue * n_steps
        self.channel_names = channel_names or ["CH"]
        self.frame_queue = queue.Queue(maxsize=self.max_queue_size)  # File partagée entre les threads

        self.stop_event = threading.Event()  # Permet de stopper tous les threads proprement
        self.threads = []

        self.viewer_callback = None  # Fonction externe appelée à chaque nouvelle image (GUI, etc.)

        # Statistiques
        self.total_frames = 0
        self.total_dropped = 0
        self.total_volumes = 0
        self.start_time = None

    def start(self):
        """
        Start acquisition, saving and viewer threads.
        Initializes the time reference for statistics computation.
        """
        # Lance les trois threads principaux : acquisition, sauvegarde, affichage
        self.stop_event.clear()
        self.start_time = time.time()
        self.threads = [
            threading.Thread(target=self.acquisition_loop, name="AcquisitionThread"),
            threading.Thread(target=self.saving_loop, name="SavingThread"),
            threading.Thread(target=self.viewer_loop, name="ViewerThread")
        ]
        for t in self.threads:
            t.start()

    def stop(self):
        """
        Signal all threads to stop, wait for them to join,
        and print acquisition statistics. Also appends summary to log.txt.
        """
        self.stop_event.set()
        for t in self.threads:
            t.join()
        self._print_stats()
        
        self._append_acquisition_summary()

    def _print_stats(self):
        """
        Print acquisition statistics in the console:
        total frames, dropped frames, volumes saved, frame/volume rates, etc.
        """
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
        
    def _get_stats_dictionnary(self):
        elapsed = time.time() - self.start_time if self.start_time else 0
        self.stats = {
                "total_frames": self.total_frames,
                "total_dropped": self.total_dropped,
                "total_volumes": self.total_volumes,
                "elapsed": elapsed,
                }
        
        if elapsed > 0:            
            self.stats["FPS"] = self.total_frames / elapsed
            self.stats["Hz"] = self.total_volumes / elapsed


    def acquisition_loop(self):
        """
        Acquisition thread: reads frames from the camera as fast as possible
        and puts them into the shared RAM queue. Tracks dropped frames.
        """
        # Lit les images depuis la caméra aussi rapidement que possible
        while not self.stop_event.is_set():
            frames = self.camera.read_camera()  # Doit retourner une liste de tableaux numpy
            for frame in frames:
                image = ImageFrame(data=frame)
                try:
                    self.frame_queue.put(image, timeout=0.1)  # Place l'image dans la file partagée
                    self.total_frames += 1
                    print(f"[Acquisition workers] total read: {self.total_frames} images", end='\r')
                except queue.Full:
                    self.total_dropped += 1
                    print("[WARNING] Frame queue full. Dropping frame.")
            time.sleep(0.001)  # Petite pause pour éviter de monopoliser le CPU

    def saving_loop(self):
        """
        Saving thread: collects frames from the queue, assembles them into
        3D stacks (volumes), and saves them as TIFF files.
        """
        # Sauvegarde les volumes depuis la file vers le disque (SSD)
        os.makedirs(self.save_dir, exist_ok=True)
        volume_id = 0
        channel_frames = {name: [] for name in self.channel_names}
        channel_index = 0

        while (not self.stop_event.is_set() or not self.frame_queue.empty()):
            try:
                frame = self.frame_queue.get(timeout=0.1)  # Récupère la prochaine image
                current_channel = self.channel_names[channel_index]
                channel_frames[current_channel].append(frame.data)

                if len(channel_frames[current_channel]) == self.n_steps:
                    stack = np.stack(channel_frames[current_channel], axis=0)
                    filename = os.path.join(self.save_dir, f"{current_channel}_volume_{volume_id:04d}.tiff")
                    imwrite(filename, stack)
                    channel_frames[current_channel].clear()
                    channel_index = (channel_index + 1) % len(self.channel_names)
                    if channel_index == 0:
                        volume_id += 1
                        self.total_volumes += 1
                        # print(f"[Acquisition workers] total saved: {self.total_volumes} volumes", end='\r')

            except queue.Empty:
                continue

    def viewer_loop(self):
        """
        Viewer thread: continuously sends the latest available frame
        and real-time stats to the viewer callback.
        """
        # Affiche la dernière image disponible pour du live preview (si viewer_callback défini)
        # Transmet également les statistiques d'acquisition en temps réel
        try:
            frame = self.frame_queue.queue[-1]  # Récupère la dernière image sans la retirer
            if self.viewer_callback:
                stats = {
                    "total_frames": self.total_frames,
                    "dropped": self.total_dropped,
                    "volumes": self.total_volumes,
                    "fps": self.total_frames / (time.time() - self.start_time + 1e-6)  # évite division par zéro
                }
                self.viewer_callback(frame.data, stats)
        except IndexError:
            pass  # Si la queue est vide
            time.sleep(0.05)  # Framerate ~20 FPS

    def set_viewer_callback(self, callback_func):
        """
        Define the function to be called for live image display.
        The function must accept two arguments: image (ndarray), stats (dict).
        """
        # La fonction doit accepter deux arguments : image, stats
        # Enregistre une fonction à appeler pour l'affichage live
        self.viewer_callback = callback_func
        
    def _append_acquisition_summary(self):
        # Write final stats to log.txt if save_dir exists
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