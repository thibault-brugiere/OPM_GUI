# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 16:54:49 2026

@author: tbrugiere

This program should be run with the environnement OPM_gpu that contains the library
cupyx
This program us ls3 acquisition images in zarr format for more efficiency
The theoritical maximum z plans is around 22337 sor 18.115mm
(for 2000 pixels in y and anaspect ratio of 3.37 and a graphic card with 16gb of memorry)
"""
import gc
import math
import numpy as np
import cupy as cp
import zarr

from deskew_rotate_cupyx import deskew_and_rotate_opm as deskew_rotate
from deskew_rotate_cupyx import _px_shift_calculation as px_shift_calculation
import parsename

import time as t

def open_x_slices_zarr(buffer : np.ndarray, file_path:list,x_start:int, x_end:int):
    file = file_path + r"\ZarrFiles.zarr"
    z = zarr.open(file, mode="r")
    return z[:, :, x_start:x_end]

def auto_deskew_rotate_ls3(folder, max_shear_size : int = 2e9, progress_callback = None):
    """
    Automaticallu deskew and rotate images from LS3 protocol contained in a folder.
    The images should be in a .zarr folder in the format : "Position_{:04d}_{str}_file.zarr"
    It save the images in the same folder in the zarr format : "deskew_Position_{:04d}_{str}_file.zarr"

    Parameters
    ----------
    folder : of str
        folder containing the images to deskew and rotate
    max_shear_size : int, optional, The default is 2e9.
        Maximum size in pixels of the image after shearing, should be 1/4 of
        the memorry of the graphic card. Lower it if necessary
    progress_callback : None, optionlal
        External process use to follow the advancement of the program

    Returns
    -------
    None.

    """
    print(folder)
    parse_ls3 = parsename.parse_ls3_foldernames(folder)
    metadata = parsename.get_metadata(folder)
    

    if len(parse_ls3['files']) == 0:
        print("No image to process")
        return
        
    if progress_callback is not None :
        total_images = len(parse_ls3["positions"]) * len(parse_ls3["channels"])
        processed_images = 0
                
    for position in parse_ls3["positions"] :
        print(f"Position : {position:04d}")
        for channel in parse_ls3["channels"]:
            print(f"Channel : {channel}")
            
            file = folder + r"\Position_"+ f"{position:04d}_{channel}_file.zarr"
            
            volume = zarr.open(file, mode="r")
            
            z, y, x = volume.shape
              
            x_slices = x
            
            px_shift = px_shift_calculation(metadata["aspect_ratio"], metadata["angle"], angle_unit = "deg")
            shear_size_zy = z * ( z - 1 ) * px_shift + z * y # during shearing
            max_step_size = max_shear_size / shear_size_zy
            
            steps = math.ceil(x_slices / max_step_size)
            
            if x_slices / steps < 1 :
                raise ValueError("z y size of the imge is too big")
            
            step_size = math.ceil(x_slices / steps)
            
            
            for k in range(steps):
                
                if progress_callback is not None :
                    processed_images += 1
                    progress_callback(k,steps,processed_images, total_images)
                else:
                    print(f'\rpart {k + 1}/{steps}', end = "")
                
                out_volume_cp = deskew_rotate(
                    volume[:, :, k*step_size:min((k+1) * step_size, x_slices)],
                    dy_um = metadata["px_size"],
                    aspect_ratio = metadata["aspect_ratio"],
                    theta_deg = metadata["angle"])
                
                if k == 0 :
                    z,y = out_volume_cp.shape[-3],out_volume_cp.shape[-2]
                    
                    out_file = folder + r"\deskew_Position_"+ f"{position:04d}_{channel}_file.zarr"
                    
                    zarr_array = zarr.open(
                    out_file,
                    mode="w",
                    shape=(z, y, x_slices),
                    chunks=(64, y , step_size),
                    dtype=np.uint16,
                )

                zarr_array[:,:,k*step_size : min((k+1) * step_size, x_slices)] = out_volume_cp
                
                del out_volume_cp
                
                gc.collect()
                cp.get_default_memory_pool().free_all_blocks()
            
            print('')
                                
            
###############################################################################
if __name__ == "__main__" :

    folders = [
        # r"C:\Users\tbrugiere\Documents\Images_OPM\20260330_154402_Image",
        # r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260313_110909_Monica_Cos7_NHS-Esther_x4",
        r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260313_110909_Monica_Cos7_NHS-Esther_x4_copie"
        ]
    t0 = t.time()
    for folder in folders :
        auto_deskew_rotate_ls3(folder)
    t1 = t.time()
    print(f'TOTAL TIME : {t1-t0}s')