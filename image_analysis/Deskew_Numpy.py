# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 09:54:13 2025

@author: tbrugiere
"""
import math
import numpy as np

def deskew_numpy(volume: np.ndarray, px_shift_y: int = 0, px_shift_x: int = 0) -> np.ndarray:
    """
    Deskew a 3D volume (Z, Y, X) by shifting each Z-slice along Y and/or X
    by a fixed number of pixels per slice.

    Parameters:
    - volume: np.ndarray of shape (Z, Y, X)
    - px_shift_y: int, shift in Y per Z-plane
    - px_shift_x: int, shift in X per Z-plane

    Returns:
    - np.ndarray of shape (Z, Y + Z*shift_y, X + Z*shift_x)
    """
    Z, Y, X = volume.shape
    new_Y = Y + Z * abs(px_shift_y)
    new_X = X + Z * abs(px_shift_x)

    deskewed = np.zeros((Z, new_Y, new_X), dtype=volume.dtype)

    for z in range(Z):
        y_start = z * px_shift_y if px_shift_y >= 0 else new_Y - Y - z * abs(px_shift_y)
        y_end = y_start + Y

        x_start = z * px_shift_x if px_shift_x >= 0 else new_X - X - z * abs(px_shift_x)
        x_end = x_start + X

        deskewed[z, y_start:y_end, x_start:x_end] = volume[z]

    return deskewed

def compute_px_shift(aspect_ratio, angle, unit = "rad") -> int:
    if unit == "deg":
        angle_rad = angle * math.pi / 180
    else:
        angle_rad = angle
    px = aspect_ratio / math.tan(angle_rad)
    rounded = round(px)
    if not math.isclose(px, rounded, rel_tol=1e-4):
        raise ValueError(f"Invalid aspect ratio: pixel shift = {px}")
    return int(rounded)

def mean_projection_ignore_zeros(volume: np.ndarray, axis=0) -> np.ndarray:
    """
    Compute the mean projection of a volume along the given axis,
    ignoring zero values (often padding from deskewing).

    Parameters:
    - volume: np.ndarray, e.g. (Z, Y, X)
    - axis: int, axis along which to project (default: 0)

    Returns:
    - 2D np.ndarray of shape (Y, X) or equivalent, dtype=float32
    """
    sum_proj = np.sum(volume, axis=axis, dtype=np.float32)
    count_nonzero = np.count_nonzero(volume, axis=axis)

    # Éviter division par zéro : on force le diviseur à 1 (le résultat sera 0)
    count_nonzero[count_nonzero == 0] = 1
    
    mean_proj = sum_proj / count_nonzero
    
    return mean_proj.astype(np.uint16)