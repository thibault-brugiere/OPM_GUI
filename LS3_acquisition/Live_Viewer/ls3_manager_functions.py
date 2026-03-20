# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 11:57:36 2025

@author: tbrugiere
"""
import cv2
import matplotlib.pyplot as plt
import math
import numpy as np
from PySide6.QtGui import qRgb

def _calculate_image_size(camera_vsize: int,
                          camera_hsize: int,
                          camera_pixel_size: int,
                          experiment_scan_range: int,
                          experiment_scanV_range: int,
                          scanV_overlap: float,
                          n_lines: int,
                          experiment_aspect_ratio: float,
                          microscope_tilt_angle: float,
                          ):
    """
    Calculate the size of the previe image, visualized from the angle of the camera
    for the LS3_manager
    Note : horizontal axis of the image and the camera correspond to the v_size
    of the stage

    Parameters
    ----------
    camera_vsize : int
        size of the field of view in the vertical axis of the camera
    camera_hsize : int
        size of the field of view in the horizontal axis of the camera
    camera_pixel_size : int
        size of the pixels of the camera in µm
    experiment_scan_range : int
        size of the imaging field in the scanning axis (scanR axis)
    experiment_scanV_range : int
        size of the imaging field orthogonal to the scanning axis (scanV axis)
    scanV_overlap : float between 0 and 1
        percentage of overlapping between two lines
    n_lines : int
        number of lines in the experiment
    experiment_aspect_ratio : float
        pixel ratio between the z axis and xy axis of the image voxels
    microscope_tilt_angle : float (in degrees)
        angle between the coverslip and the lightsheet of the microscope in degrees

    Returns
    -------
    image_hsize : int
        horizontal size of the preview imahe
    image_vsize : int
        vertical size of the preview imahe
    px_shift : int
        shift in pixels between two images
    scanV_overlap_px: int
        overlap between two lines in pixels during the acquisition
    """
    
    angle_rad = np.deg2rad(microscope_tilt_angle)
    
    px_shift = math.ceil(experiment_aspect_ratio / math.tan(angle_rad))
    step_size = camera_pixel_size * experiment_aspect_ratio / np.sin(angle_rad)
    n_steps = experiment_scan_range / step_size
    
    image_vsize = int(camera_vsize + n_steps * px_shift + 1)
    
    scanV_overlap_px = scanV_overlap * camera_vsize
    
    if n_lines == 1 :
        image_hsize = camera_hsize
    else:
        image_hsize = (camera_hsize - scanV_overlap_px) * n_lines + scanV_overlap_px
    
    return int(image_hsize), int(image_vsize), int(px_shift), int(scanV_overlap_px)

def create_ls3_image(ls3):
    """
    Create the image to display on the LS3_manager UI during LS3 acquisition,
    depending on the parameters of the acquisition.

    Parameters
    ----------
    ls3 : TYPE
        main_LS3 object created during acquisition

    Returns
    -------
    empty_image : np.ndarray
        Image to display
    px_shift : int
        distance in pixels between two consecutive image during acquisition
        in the plan of the camera
    scanV_overlap : int
        overlapping distance between two lines during ls3 acquisition

    """
    
    hsize, vsize, px_shift, scanV_overlap_px = _calculate_image_size(
        ls3.config.cameras[0].vsize,
        ls3.config.cameras[0].hsize,
        ls3.config.cameras[0].sample_pixel_size,
        ls3.config.experiment.stage_scan_range,
        ls3.config.experiment.scanV_range,
        ls3.config.experiment.scanV_overlap,
        ls3.n_lines,
        ls3.config.experiment.aspect_ratio,
        ls3.config.microscope.tilt_angle)
    
    empty_image = np.zeros((vsize, hsize), dtype=int)
    
    return empty_image, px_shift, scanV_overlap_px

def _past_max_project(base_image, add_image, x , y):
    """
    Paste small_img into base_img using max projection.
    
    Parameters
    ----------
    base_image : np.ndarray
        Image cible (H, W).
    small_img : np.ndarray
        Image à coller (h, w).
    y : int
        Coordonnée Y (haut gauche).
    x : int
        Coordonnée X (haut gauche).
    """
    vsize , hsize = add_image.shape
    
    x_end = min((x + hsize), base_image.shape[1])
    y_end = min((y + vsize), base_image.shape[0])
    
    copy_h = y_end - y
    copy_w = x_end - x
    
    if copy_h <=0 or copy_w <=0:
        return base_image
    
    # base_image[y:y_end, x:x_end] = np.maximum( # TODO A supprimer
    #     base_image[y:y_end, x:x_end],
    #     add_image[:copy_h, :copy_w]
    #     )
    
    dst = base_image[y:y_end, x:x_end]
    src = add_image[:copy_h, :copy_w]
    np.maximum(dst, src, out=dst)
    
    return base_image

def add_image(preview_image: np.ndarray,
              image: np.ndarray,
              metadata: dict,
              px_shift: int,
              overlap):
    """
    Add a new deskewed image to the preview image during LS3 acquisition process
    with a maximum projection.

    Parameters
    ----------
    preview_image : np.ndarray
        2d image displayed in the preview
    image : np.ndarray
        2d new image to add to the preview image
    metadata : dict
        metadata of the image to add, containing at least the "file_id" and
        "volume_id"
    px_shift : int
        pixel_shif between two frames of the stack (to calculate the position
                                                    of the image)
    overlap : int
        pixels overlapping between the volumes

    Returns
    -------
    preview_image : np.ndarray
        preview image wi the immage added

    """
    # There is 100 images per file, to the total shift is 100 * file_id (file number) * px_shift
    vsize, hsize = image.shape
    y = int(px_shift * metadata["file_id"] * 100) if "file_id" in metadata else 0
    x = int(metadata["volume_id"] * (hsize - overlap)) #if "vomule_id" in metadata else 0

    preview_image = _past_max_project(preview_image, image, x, y)
    return preview_image

def crop_zoom_image(image: np.ndarray,
                    x_position: int,
                    y_position: int,
                    zoom: float,
                    h_label: int,
                    w_label: int,
                    pad_value:int = 50,
                    ):
    """
    Zoom and crop an image so it fits inside a display window, using normalized
    positions between 0 and 99.

    Parameters
    ----------
    image : np.ndarray
        Input image of shape (H, W) or (H, W, C).
    x_position : int
        Horizontal crop position in [0, 99], 0 = left, 99 = right.
    y_position : int
        Vertical crop position in [0, 99], 0 = top, 99 = bottom.
    zoom : float
        Zoom factor of the image.
    h_label : int
        Height of the target window
    w_label : int
        Width of the target window
    pad_value : int default 50
        value between 0 and 250 around the image

    Returns
    -------
    np.ndarray
        Zoomed and Cropped image.
    """
    
    # Output canvas
    output = np.full((h_label, w_label), pad_value, dtype=np.uint8)
    
    if image is None or image.size == 0:
        return output
    
    if zoom <= 0:
        zoom = 1
    
    x_position = max(0, min(99, x_position))
    y_position = max(0, min(99, y_position))

    h, w = image.shape
    
    # Size of the image after zoom, in display coordinates
    h_zoom = max(1, int(round(h * zoom)))
    w_zoom = max(1, int(round(w * zoom)))
    
    # Visible area inside the zoomed image
    crop_h =min(h_label, h_zoom)
    crop_w = min(w_label, w_zoom)
    
    if crop_w <= 0 or crop_h <= 0:
        return output

    # Top-left corner in the zoomed-image coordinates
    max_x0 = w_zoom - crop_w
    max_y0 = h_zoom - crop_h
    
    if max_x0 <= 0:
        x0_zoom = 0
    else:
        x0_zoom = math.floor((x_position / 99) * max_x0)
        
    if max_y0 <= 0:
        y0_zoom = 0
    else:
        y0_zoom = math.floor((y_position / 99) * max_y0)
    
    x1_zoom = x0_zoom + crop_w
    y1_zoom = y0_zoom + crop_h
    
    # Convert the visible rectangle back to source-image coordinates
    x0_src = max(0, min(w, int(np.floor(x0_zoom / zoom))))
    y0_src = max(0, min(h, int(np.floor(y0_zoom / zoom))))
    x1_src = max(x0_src + 1, min(w, int(np.ceil(x1_zoom / zoom))))
    y1_src = max(y0_src + 1, min(h, int(np.ceil(y1_zoom / zoom))))
    
    roi = image[y0_src:y1_src, x0_src:x1_src]
    
    if roi.size == 0 :
        return output
    
    # Resize only the useful ROI to the visible output size
    if roi.shape[0] == crop_h and roi.shape[1] == crop_w:
        crop_image = roi
    else:
        crop_image = cv2.resize(
            roi,
            (crop_w, crop_h),
            interpolation=cv2.INTER_LINEAR
        )
    
    output[:crop_h, :crop_w] = crop_image
    
    return output
    
def auto_contrast(image: np.ndarray, low_perc: float = 0.5, high_perc: float = 99.5):
    """
    Calcule automatiquement les niveaux de gris pour l'affichage à contraste adapté.
    
    Args:
        image (np.ndarray): Image 2D ou 3D
        low_perc (float): Percentile bas (ex: 0.5)
        high_perc (float): Percentile haut (ex: 99.5)
    
    Returns:
        (float, float): min_grayscale, max_grayscale
    """
    flat = image.flatten()
    min_gray = np.percentile(flat, low_perc)
    max_gray = np.percentile(flat, high_perc)

    if min_gray == max_gray:
        # Évite division par zéro ou contraste nul
        min_gray, max_gray = float(flat.min()), float(flat.max())
    
    return min_gray, max_gray

class LookUpTables :
    
    def __init__(self):
        self.on_init()
    
    def on_init(self):
        self.palettes = {"Grayscale" : [qRgb(i, i, i)   for i in range(256)],
                         "Red"       : [qRgb(i, 0, 0)   for i in range(256)],
                         "Green"     : [qRgb(0, i, 0)   for i in range(256)],
                         "Blue"      : [qRgb(0, 0, i)   for i in range(256)],
                         "Fire"      : self._fire_palette(),
                    }
        
    def _fire_palette(self):
        pal = []
        for i in range(256):
            # zones: 0-127 rouge monte, 128-223 vert monte, 224-255 bleu monte
            if i < 128:
                r, g, b = 2*i, 0, 0
            elif i < 224:
                r, g, b = 255, int(255*(i-128)/96), 0
            else:
                r, g, b = 255, 255, int(255*(i-224)/31)
            pal.append(qRgb(r, g, b))
        return pal
    
    