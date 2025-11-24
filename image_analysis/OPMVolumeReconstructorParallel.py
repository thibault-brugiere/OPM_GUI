import threading
import queue
import numpy as np
import tifffile
from tqdm import tqdm

class OPMVolumeReconstructorParallel:
    def __init__(
        self, input_file, shifts_xy, output_file,
        batch_size=4, max_queue_size=8,
        compute_mip=False, compute_mean=False,
        dtype=None   # Si None : dtype détecté automatiquement
    ):
        self.input_file = input_file
        self.shifts_xy = shifts_xy
        self.output_file = output_file
        self.batch_size = batch_size
        self.max_queue_size = max_queue_size
        self.compute_mip = compute_mip
        self.compute_mean = compute_mean

        # Lecture des métadonnées
        with tifffile.TiffFile(self.input_file) as tf:
            self.n_frames = len(tf.pages)
            if self.n_frames == 0:
                raise ValueError("Aucune image dans le fichier source.")
            first_image = tf.pages[0].asarray()
            self.image_dtype = first_image.dtype
            self.in_h, self.in_w = first_image.shape[-2], first_image.shape[-1]

        # Vérif cohérence entre shifts et n_frames
        if len(self.shifts_xy) != self.n_frames:
            raise ValueError(f"Nombre de shifts fourni ({len(self.shifts_xy)}) "
                             f"différent du nombre d'images du fichier ({self.n_frames})")

        self.dtype = dtype if dtype is not None else self.image_dtype

        self.queue = queue.Queue(maxsize=max_queue_size)
        self.stop_token = object()
        self.mip = None
        self.mean = None
        self.n_proj = 0

    def shift_image(self, img, dx, dy):
        res = np.zeros_like(img)
        h, w = img.shape
        x0 = max(dx, 0)
        y0 = max(dy, 0)
        x1 = w + min(dx, 0)
        y1 = h + min(dy, 0)
        res[y0:y1, x0:x1] = img[y0-dy:y1-dy, x0-dx:x1-dx]
        return res

    def producer(self):
        with tifffile.TiffFile(self.input_file) as tif:
            for start in tqdm(range(0, self.n_frames, self.batch_size), desc="Reading+Translating"):
                end = min(start + self.batch_size, self.n_frames)
                imgs = np.stack([
                    tif.pages[i].asarray()
                    for i in range(start, end)
                ])
                # Apply translations
                imgs_shifted = np.stack([
                    self.shift_image(imgs[i - start], *self.shifts_xy[i])
                    for i in range(start, end)
                ])
                # Optionally accumulate projections
                if self.compute_mip:
                    if self.mip is None:
                        self.mip = imgs_shifted.max(axis=0)
                    else:
                        self.mip = np.maximum(self.mip, imgs_shifted.max(axis=0))
                if self.compute_mean:
                    if self.mean is None:
                        self.mean = imgs_shifted.sum(axis=0, dtype=np.float64)
                        self.n_proj = imgs_shifted.shape[0]
                    else:
                        self.mean += imgs_shifted.sum(axis=0, dtype=np.float64)
                        self.n_proj += imgs_shifted.shape[0]
                self.queue.put(imgs_shifted)
        self.queue.put(self.stop_token)

    def consumer(self):
        with tifffile.TiffWriter(self.output_file, bigtiff=True) as out:
            while True:
                batch = self.queue.get()
                if batch is self.stop_token:
                    break
                out.write(batch.astype(self.dtype))
                self.queue.task_done()
        self.queue.task_done()  # for the stop token

    def process(self):
        t_prod = threading.Thread(target=self.producer)
        t_cons = threading.Thread(target=self.consumer)
        t_cons.start()
        t_prod.start()
        t_prod.join()
        t_cons.join()
        # Save projections if needed
        if self.compute_mip:
            tifffile.imwrite(self.output_file.replace('.tif', '_MIP.tif'), self.mip.astype(self.dtype))
        if self.compute_mean:
            mean_img = (self.mean / self.n_proj).astype(self.dtype)
            tifffile.imwrite(self.output_file.replace('.tif', '_Mean.tif'), mean_img)

# --- Exemple d'utilisation ---
input_file = "mon_volume_deskewed.tif"
output_file = "mon_volume_translated.tif"

# Détection automatique du nombre de plans dans la classe
# Pour l’exemple : shift +1 px en x à chaque plan
with tifffile.TiffFile(input_file) as tf:
    n_planes = len(tf.pages)
shifts_xy = [0,3]

reco = OPMVolumeReconstructorParallel(
    input_file=input_file,
    shifts_xy=shifts_xy,
    output_file=output_file,
    batch_size=8,        # ajustable
    max_queue_size=8,
    compute_mip=True,
    compute_mean=True,
    # dtype=None  # <- détection automatique du dtype de la 1ère image
)
reco.process()