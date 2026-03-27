# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 14:58:45 2026

@author: tbrugiere

This program should be run with the environnement OPM_gpu that contains the library
cupyx
"""
import cupy as cp
from cupyx.scipy import ndimage as cndi
import numpy as np
from skimage.restoration import rolling_ball
import tifffile

def crop_stack(arr: np.ndarray, x1: int, y1: int, x2: int, y2: int):
    """
    Crop a rectangular region of interest (ROI) from an array.
    
    The function supports both 2D images and higher-dimensional stacks.
    Cropping is always applied to the last two axes, which are assumed to
    correspond to spatial dimensions (Y, X).
    
    Parameters
    ----------
    arr : np.ndarray
        Input array. Can be a 2D image (H, W) or a stack with shape
        (..., H, W). All leading dimensions are preserved.
    x1, y1 : int
        Coordinates of the top-left corner of the ROI (inclusive).
    x2, y2 : int
        Coordinates of the bottom-right corner of the ROI (inclusive).
    
    Returns
    -------
    np.ndarray
        Cropped view of the input array with shape (..., y2-y1+1, x2-x1+1).
    """
    if arr.ndim < 2:
        raise ValueError(f"Array has ndim={arr.ndim}, expected at least 2.")
    
    h = arr.shape[-2]
    w = arr.shape[-1]
    
    for name, v, lo, hi in [
        ("x1", x1, 0, w - 1),
        ("x2", x2, 0, w - 1),
        ("y1", y1, 0, h - 1),
        ("y2", y2, 0, h - 1),
        ]:
        if not (lo <= v <= hi):
            raise ValueError(f"{name}={v} out of bounds. Valid: [{lo}, {hi}]")
    
    if x2 < x1 or y2 < y1:
        raise ValueError("Invalid ROI: need x2>=x1 and y2>=y1.")
    
    # y then x
    return arr[..., y1 : y2 + 1, x1 : x2 + 1]


def rolling_ball_stack(stack: np.ndarray, radius: int):
    """
    Perform background subtraction on a 3D stack using 2D rolling ball 
    
    Parameters
    ----------
    stack: np.ndarray
    Input 3D stack with shape (Z, Y, X). Can be uint16 or float.
    The array is transferred to the GPU internally.
    radius: int
        Radius of the circular structuring element in pixels. This value
        should be larger than the typical object size to preserve objects
        while removing slowly varying background.
        
    Returns
    -------
    np.ndarray
        Background-subtracted 3D stack, transferred back to CPU memory.
        All negative values are clipped to zero. 
    """
    out = np.empty_like(stack)

    for z in range(stack.shape[0]):
        bg = rolling_ball(stack[z], radius=radius)
        out[z] = stack[z] - bg
        print(f"Backgournd substraction : {z}\r", end ="")

    out[out < 0] = 0
    return out

def subtract_bg_xy_gpu(stack: np.ndarray, radius_px: int, gpu_id: int = 0, return_numpy: bool = False):
    """
    Perform background subtraction on a 3D stack using 2D grey opening
    (morphological opening) applied slice-by-slice on the GPU.
    
    This function is designed for OPM (Oblique Plane Microscopy) data where
    consecutive Z planes are not spatially aligned. For this reason, the
    background is estimated independently in each XY plane rather than
    using a full 3D operation.
    
    The background is estimated using a circular structuring element
    (disk) with a given radius, and subtracted from the original image.
    Negative values are clipped to zero.
    
    Parameters
    ----------
    stack_np : np.ndarray
        Input 3D stack with shape (Z, Y, X). Can be uint16 or float.
        The array is transferred to the GPU internally.
    radius_px : int
        Radius of the circular structuring element in pixels. This value
        should be larger than the typical object size to preserve objects
        while removing slowly varying background.
    gpu_id : int, optional
        CUDA device index to use (default: 0).
    return_numpy: bool
        tell if the function returns a numpy or a cupy array
    
    Returns
    -------
    np.ndarray ot cp.ndaray
        Background-subtracted 3D stack, transferred back to CPU memory.
        All negative values are clipped to zero.
    """
    
    with cp.cuda.Device(gpu_id):
        
        # Ensure contiguous memory before transfer to GPU
        stack = np.ascontiguousarray(stack)
        stack = cp.asarray(stack)
    
        # Build a 2D circular footprint (disk) in the XY plane
        yy, xx = cp.ogrid[-radius_px:radius_px+1, -radius_px:radius_px+1]
        footprint = (xx*xx + yy*yy) <= radius_px*radius_px
    
        # Estimate background using grey opening on GPU
        out = cp.empty_like(stack)
        for z in range(stack.shape[0]):
            bg = cndi.grey_opening(stack[z], footprint=footprint, mode="reflect")
            out[z] = stack[z] - bg
            print(f"Backgournd substraction : {z}\r", end ="")
    
        # Subtract background and clip negative values
        out = cp.maximum(out, 0)
        if return_numpy:
            return cp.asnumpy(out)
        
        return out
    
def subtract_bg_stack_xy_gpu(stack: np.ndarray, radius_px: int, gpu_id: int = 0):
    """
    Subtract background from a 3D stack using a 2D morphological opening
    applied simultaneously to all Z planes on the GPU.
    
    A circular structuring element is used in the XY plane, while the Z
    dimension is left untouched (footprint size = 1 in Z). This makes the
    method suitable for OPM data where Z planes are not spatially aligned.
    
    Parameters
    ----------
    stack : np.ndarray
        Input 3D stack with shape (Z, Y, X).
    radius_px : int
        Radius of the circular structuring element in pixels.
        Should be larger than the typical object size.
    gpu_id : int, optional
        CUDA device index to use (default: 0).
    
    Returns
    -------
    np.ndarray
        Background-subtracted 3D stack. Negative values are clipped to zero
        and the result is returned in CPU memory.
    """
    
    with cp.cuda.Device(gpu_id):
        
        # Ensure contiguous memory before transfer to GPU
        stack = np.ascontiguousarray(stack)
        stack = cp.asarray(stack)
    
        # Build a 2D circular footprint (disk) in the XY plane
        yy, xx = cp.ogrid[-radius_px:radius_px+1, -radius_px:radius_px+1]
        footprint2d = (xx*xx + yy*yy) <= radius_px*radius_px
        
        # Extend footprint to 3D (Z size = 1) to enforce XY-only operation
        footprint3d = footprint2d[None, :, :]

        # Estimate background using grey opening on GPU
        bg = cndi.grey_opening(stack, footprint=footprint3d, mode="reflect")
        
        # Subtract background and clip negative values
        out = cp.maximum(stack - bg, 0)

        return cp.asnumpy(out)


def bleach_correction_exp(img, idx, I0, bleach_constant, background):
    """
    Apply exponential bleach correction to a single image or volume.
    
    The correction follows the model:
        I_corr = (I - background) * exp(idx * bleach_constant) + background
    
    Parameters
    ----------
    img : np.ndarray
        Input image or volume, expected dtype uint16.
    idx : int
        Frame index (must start at 0).
    I0 : float
        Intensity at first image (e.g. fitted parameter c).
    bleach_constant : float
        Exponential bleach constant per frame.
    background : float
        Background intensity offset (e.g. fitted parameter c).
    
    Returns
    -------
    np.ndarray
        Bleach-corrected image, dtype uint16.
    """
    
    if img.dtype != np.uint16:
        raise TypeError(f"Image dtype is {img.dtype}, expected uint16.")
    
    out = img.astype(np.float32, copy=False)
    
    y0 = I0 + background
    yt = I0 * np.exp(-bleach_constant * idx) + background
    f = y0 / yt
    # out = (out - background) * f + background
    
    out -= background
    out *= f
    out += background
    
    return np.clip(out, 0, 65535).astype(np.uint16)
    
        
def save_image(image: np.ndarray, name: str = "numpy_deskewed", path: str=''):
    """
    Save an image or image stack to a TIFF file.
    
    The input array is written as a TIFF or BigTIFF file depending on its
    size. Compression is enabled to reduce disk usage.
    
    Parameters
    ----------
    image : np.ndarray
        Image or image stack to save.
    name : str, optional
        Base name of the output file without extension
        (default: ``"numpy_deskewed"``).
    path : str, optional
        Output directory. The file name is appended to this path
        (default: empty string).
    
    Returns
    -------
    None
    """
    
    output_file_path = f'{path}{name}.tif'
    tifffile.imwrite(output_file_path, image, compression='zlib')
    
def max_intensity_projection(volume, axis=0):
    """
    Compute a maximum intensity projection (MIP) of a 3D volume.

    Parameters
    ----------
    volume : np.ndarray
        Input 3D array (e.g. shape (Z, Y, X)).
    axis : int, optional
        Axis along which to compute the projection.
        Default is 0 (Z projection).

    Returns
    -------
    np.ndarray
        2D maximum intensity projection.
    """

    if volume.ndim != 3:
        raise ValueError(f"Expected a 3D array, got {volume.ndim}D.")

    return np.max(volume, axis=axis)