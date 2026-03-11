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
    """
    
    angle_rad = np.deg2rad(microscope_tilt_angle)
    
    px_shift = math.ceil(experiment_aspect_ratio / math.tan(angle_rad))
    step_size = camera_pixel_size * experiment_aspect_ratio / np.sin(angle_rad)
    n_steps = experiment_scan_range / step_size
    
    image_vsize = camera_vsize + n_steps * px_shift
    
    image_hsize= max(math.ceil(experiment_scanV_range / camera_pixel_size), camera_hsize)
    
    return image_hsize, image_vsize, px_shift

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
    scanV_overlap : float
        overlapping distance between two lines during ls3 acquisition

    """
    hsize, vsize, px_shift = _calculate_image_size(
        ls3.config.camera.vsize,
        ls3.congig.camera.hsize,
        ls3.config.camera.sample_pixel_size,
        ls3.experiment.stage_scan_range,
        ls3.experiment.scanV_range,
        ls3.experiment.aspect_ratio,
        ls3.microscope.tilt_angle)
    
    scanV_overlap = ls3.experiment.scanV_overlap
    
    empty_image = np.zeros((vsize, hsize), dtype=int)
    
    return empty_image, px_shift, scanV_overlap

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
    
    base_image[y:y+vsize, x:x+hsize] = np.maximum(
        base_image[y:y+vsize, x:x+hsize],
        add_image
        )
    
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

    Returns
    -------
    preview_image : np.ndarray
        preview image wi the immage added

    """
    # There is 100 images per file, to the total shift is 100 * file_id (file number) * px_shift
    vsize, hsize = image.shape
    y = px_shift * metadata["file_id"] * px_shift * 100 if "file_id" in metadata else 0
    x = metadata["volume_id"] * (hsize - overlap) if "vomule_id" in metadata else 0
    
    x, y = 0,0
    preview_image = _past_max_project(preview_image, image, x, y)
    return preview_image

def crop_zoom_image(image: np.ndarray,
                    x_position: int,
                    y_position: int,
                    zoom: float,
                    h_label: int,
                    w_label: int,
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

    Returns
    -------
    np.ndarray
        Zoomed and Cropped image.
    """
    
    x_position = max(0, min(99, x_position))
    y_position = max(0, min(99, y_position))

    h, w = image.shape
    h, w = int(h * zoom ) , int (w * zoom) # Calculate after zoom
    crop_w, crop_h = min(w_label, w), min(h_label, h)
    
    max_x0 = w - crop_w
    max_y0 = h - crop_h
    
    if max_x0 <= 0:
        x0 = 0
    else:
        x0 = round((x_position / 99) * max_x0)
    
    if max_y0 <= 0:
        y0 = 0
    else:
        y0 = round((y_position / 99) * max_y0)
    
    x1 = x0 + crop_w
    y1 = y0 + crop_h

    image = cv2.resize(image, (w, h), interpolation=cv2.INTER_LINEAR)

    return image[y0:y1, x0:x1]
    
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
    
    