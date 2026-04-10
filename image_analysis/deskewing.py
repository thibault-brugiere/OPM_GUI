# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 08:41:13 2025

@author: tbrugiere

functions used to deskew the images acquired using the OPM (no rotation)

"""
import math
import numpy as np
import os
import tifffile

def legalize_voxel_aspect_ratio(aspect_ratio:float, angle:float):
    """
    Adjust the voxel aspect ratio to be compatible with an integer pixel
    shift during OPM deskewing.
    
    Parameters
    ----------
    aspect_ratio : float
        Desired voxel aspect ratio (typically dz / dx).
    angle : float
        Tilt angle of the oblique plane, in radians.
    
    Returns
    -------
    float
        Adjusted (legalized) voxel aspect ratio compatible with an integer
        pixel shift.
    """
    return max(int(round(aspect_ratio / math.tan(angle))), 1) * math.tan(angle)

def px_shift_calculation(aspect_ratio:float, angle:float, angle_unit:str = "rad") -> int:
    """
    Compute the integer pixel shift per Z step required for OPM deskewing.

    The deskew operation assumes that the lateral shift between consecutive
    planes is an integer number of pixels. This function computes the pixel
    shift from the voxel aspect ratio and the tilt angle, and checks that
    the result is compatible with this constraint.

    Parameters
    ----------
    aspect_ratio : float
        Voxel aspect ratio (typically dz / dx).
    angle : float
        Tilt angle of the oblique plane.
    angle_unit : str, optional
        Unit of the input angle: ``"rad"`` for radians or ``"deg"`` for
        degrees (default: ``"rad"``).

    Raises
    ------
    ValueError
        If the computed pixel shift is not close to an integer value,
        indicating an incompatible voxel aspect ratio.

    Returns
    -------
    int
        Integer pixel shift per Z plane.
    """
    angle = angle if angle_unit == "rad" else np.deg2rad(angle)
                                                         
    px_shift = aspect_ratio/math.tan(angle)
    
    int_px_shift = round(px_shift)
    
    if not math.isclose(px_shift, int_px_shift, rel_tol=0.0001):
        raise ValueError(f'Aspect ratio is not legal, pixel shift = {px_shift}')
        
    return int(int_px_shift)

def deskew_numpy(volume: np.ndarray, px_shift_y: int = 0, px_shift_x: int = 0) -> np.ndarray:
    """
    Deskew a 3D volume (Z, Y, X) by shifting each Z-slice along Y and/or X
    by a fixed number of pixels per slice.
    For image with my OPM, the pixel shift is made in Y

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
    
###############################################################################

if __name__ == '__main__':
    
    import time
    from pathlib import Path
    
    aspect_ratio = 3.3564
    
    channels_list = ["BFP","GFP", "CY3.5", "TexRed"]
    
    experiment_path = Path(r"D:\Projets_Python\OPM_GUI\Images")
    
    folders= ['20260331_164237_NS_AgaroseStamp_Homer1C-mCherry',
              ]
    
    channels = ["CY3.5"]
    
    for folder in folders :
        print(f'FOLDER : {folder}')
        path = os.path.join(experiment_path , folder)
    
        for channel in channels :
            
            for k in range(60) :
                
                t0 = time.perf_counter()
                
                name = f'{channel}_volume_{k:04d}'
                print(f'Deskewing {name}')
                
                #
                # Opening Image
                #
                
                try :
                
                    file_path = os.path.join(path, f'{name}.tif')
                    
                    image = tifffile.imread(file_path)
                    
                    print("oppened")
                    
                    #
                    # Deskew
                    #
                    
                    px_shift = px_shift_calculation(aspect_ratio, angle = 40, angle_unit = "deg")
                    
                    deskew_image = deskew_numpy(image,px_shift_y=px_shift)
                    
                    print("deskewed")
                    
                    #
                    # Saving
                    #
                    
                    os.makedirs(f'{path}/deskew', exist_ok=True)
                    
                    save_image(deskew_image, f'deskew_{name}', f'{path}/deskew/')
                    
                    print(f"deskew_{name} saved")
                    
                    print(f"Duration: {time.perf_counter() - t0:.3f} s")
                    print(" ")
                    
                except:
                    print("File doesn't exist")
                    print(" ")
        