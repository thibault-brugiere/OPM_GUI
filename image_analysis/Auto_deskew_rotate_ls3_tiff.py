# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 16:54:49 2026

@author: tbrugiere

This program should be run with the environnement OPM_gpu that contains the library
cupyx
This program use tiff ls3 images but only charge a part of the images for more
ram efficiency
"""
import gc
import math
import numpy as np
import cupy as cp
import os
from pathlib import Path
import tifffile

from deskew_rotate_cupyx import deskew_and_rotate_opm as deskew_rotate
from deskew_rotate_cupyx import _px_shift_calculation as px_shift_calculation
import parsename
import preprocessing

def open_x_slices_tif(buffer : np.ndarray, file_path_list:list,x_start:int, x_end:int):
    chunk_x = x_end - x_start
    start = 0
    k=0
    for file_path in file_path_list :
        k+=1
        array = tifffile.memmap(file_path)
        z,y,x = array.shape
        end = start + z
        buffer[start:end,:,:chunk_x] = array[:,:,x_start:x_end]
        start = end
        del array

    return buffer[:, :, :chunk_x]

def auto_deskew_rotate_ls3(folder, max_shear_size : int = 2e9, progress_callback = None):
    parse_ls3 = parsename.parse_ls3_filenames(folder)
    metadata = parsename.get_metadata(folder)
    
    if len(parse_ls3['files']) == 0 :
        return
    
    if progress_callback is not None :
        total_images = len(parse_ls3["positions"]) * len(parse_ls3["channels"])
        processed_images = 0

    for position in parse_ls3["positions"] :
        print(f"Position : {position:04d}")
        for channel in parse_ls3["channels"]:
            print(f"Channel : {channel}")
            
            file_path_list = []
            size_list = []

            for index in parse_ls3["index"]:
                filename = f'Position_{position:04d}_{channel}_file_{index:04d}.tif'
                name = f'Position_{position:04d}_{channel}'
                file_path = os.path.join(folder, filename)
                file_path_list.append(file_path)
                
                with tifffile.TiffFile(file_path) as tif:
                    shape = tif.series[0].shape
                    
                size = shape[0]
                size_list.append(size)
                y, x = shape[1:3]
            
            total_size = int(np.sum(size_list))                    
            
            x_slices = x
            y_slices = y
            z = total_size
            
            px_shift = px_shift_calculation(metadata["aspect_ratio"], metadata["angle"], angle_unit = "deg")
            shear_size_zy = z * ( z - 1 ) * px_shift + z * y # during shearing
            max_step_size = max_shear_size / shear_size_zy
            
            steps = math.ceil(x_slices / max_step_size)
            
            if x_slices / steps < 1 :
                raise ValueError("z y size of the imge is too big")
            
            step_size = math.ceil(x_slices / steps)
            
            sub_volume_buffer = np.empty((total_size, y_slices, step_size), dtype=np.uint16)
            
            for k in range(steps):
                if progress_callback is not None :
                    processed_images += 1
                    progress_callback(k,steps,processed_images, total_images)
                
                print(f'\rpart {k + 1}/{steps}', end = "")
                
                sub_volume_zyx = open_x_slices_tif(
                                        sub_volume_buffer,
                                        file_path_list,
                                        k*step_size,
                                        min((k+1) * step_size, x_slices)
                                        )

                out_volume_cp = deskew_rotate(
                    cp.asarray(sub_volume_zyx),
                    dy_um = metadata["px_size"],
                    aspect_ratio = metadata["aspect_ratio"],
                    theta_deg = metadata["angle"])
                
                if k == 0 :
                    z,y = out_volume_cp.shape[-3],out_volume_cp.shape[-2]
                    out_volume_np = np.empty((z,y,x_slices), dtype = np.uint16)

                out_volume_np[:,:,k*step_size : min((k+1) * step_size, x_slices)] = out_volume_cp
                
                del out_volume_cp
                del sub_volume_zyx
                gc.collect()
                cp.get_default_memory_pool().free_all_blocks()
            
            print('')
            print('saving')
                    
            output_file_path = f'{folder}/test_dekew-rotate_{name}.tif'
            tifffile.imwrite(output_file_path, out_volume_np, bigtiff=True, compression=None)

            print('')
            
            del out_volume_np
                                
            
###############################################################################
if __name__ == "__main__" :

    folders = [
        r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260313_110909_Monica_Cos7_NHS-Esther_x4_copie",
        ]
    for folder in folders :
        auto_deskew_rotate_ls3(folder)