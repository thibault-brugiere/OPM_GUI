# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 16:54:49 2026

@author: tbrugiere

This program should be run with the environnement OPM_gpu that contains the library
cupyx
This programm charge the entire during processing meaning that volumes too big are not supported
"""
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

def auto_deskew_rotate_mda(folder, progress_callback = None):
    print(folder)
    parse_mda = parsename.parse_mda_filenames(folder)
    metadata = parsename.get_metadata(folder)
    
    if len(parse_mda['files']) == 0 :
        return
    
    if progress_callback is not None :
        total_images = len(parse_mda["files"])
        processed_images = 0
        
    for file in parse_mda["files"] :
        if file['process'] :
            file_path = Path(file['path'])
            name = file_path.name
            
            if progress_callback is not None :
                processed_images += 1
                progress_callback(0,0,processed_images, total_images)
            else:
                print(f'Image: {name}')
            
            volume_zyx = tifffile.imread(file_path)
            volume_zyx_cp = cp.asarray(volume_zyx)
            
            # volume_zyx_cp = preprocessing.subtract_bg_xy_gpu(volume_zyx_cp, 20)
                
            out_volume = deskew_rotate(volume_zyx_cp, dy_um = metadata["px_size"],
                                       aspect_ratio = metadata["aspect_ratio"],
                                       theta_deg = metadata["angle"])
            
            out_volume_np = cp.asnumpy(out_volume)
            
            output_file_path = f'{folder}/dekew-rotate_{name}'
            tifffile.imwrite(output_file_path, out_volume_np, bigtiff=True, compression='zlib')
                
def auto_deskew_rotate_ls3(folder, max_shear_size = 2e9, max_size_bytes = 15e9, progress_callback = None) :
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
            size_bytes = 0

            for index in parse_ls3["index"]:
                filename = f'Position_{position:04d}_{channel}_file_{index:04d}.tif'
                name = f'Position_{position:04d}_{channel}'
                file_path = os.path.join(folder, filename)
                file_path_list.append(file_path)
                size_bytes += os.path.getsize(file_path)
                
                with tifffile.TiffFile(file_path) as tif:
                    shape = tif.series[0].shape
                    
                size = shape[0]
                size_list.append(size)
                y,x = tifffile.TiffFile(file_path).series[0].shape[1:3]
                
            if size_bytes > max_size_bytes :
                size_gb = round(size_bytes / 1024 / 1024 / 1024,2)
                max_size_gb = round(max_size_bytes / 1024 / 1024 / 1024,2)
                raise ValueError(f"Image is too big :  {size_gb} / {max_size_gb} GB")
            
            total_size = int(np.sum(size_list))
            volume_zyx = np.empty((total_size,y,x), dtype = np.uint16)
            start=0

            for k in range(len(file_path_list)):
                file_path = file_path_list[k]
                end = start + size_list[k]
                volume_zyx[start : end,:,:] = tifffile.imread(file_path)
                start = end 
                
                print(f'\rcharged : {k} / {len(parse_ls3["index"])-1}', end = "")
            print("")
            
            
            z, y, x_slices = volume_zyx.shape                    
            
            px_shift = px_shift_calculation(metadata["aspect_ratio"], metadata["angle"], angle_unit = "deg")
            shear_size_zy = z * ( z - 1 ) * px_shift + z * y # during shearing
            max_step_size = max_shear_size / shear_size_zy
            
            steps = math.ceil(x_slices / max_step_size)
            
            step_size = math.ceil(x_slices / steps)
            
            for k in range(steps):
                if progress_callback is not None :
                    processed_images += 1
                    progress_callback(k,steps,processed_images, total_images)
                
                print(f'\rpart {k + 1}/{steps}', end = "")

                out_volume_cp = deskew_rotate(
                    cp.asarray(volume_zyx[:, :, k*step_size : min((k+1) * step_size, x_slices)]),
                    dy_um = metadata["px_size"],
                    aspect_ratio = metadata["aspect_ratio"],
                    theta_deg = metadata["angle"])
                
                if k == 0 :
                    z,y = out_volume_cp.shape[-3],out_volume_cp.shape[-2]
                    out_volume_np = np.empty((z,y,x_slices), dtype = np.uint16)

                out_volume_np[:,:,k*step_size : min((k+1) * step_size, x_slices)] = out_volume_cp
                
                del out_volume_cp
                cp.get_default_memory_pool().free_all_blocks()
            
            del volume_zyx
            
            print('')
            print('saving')
                    
            output_file_path = f'{folder}/test_dekew-rotate_{name}.tif'
            tifffile.imwrite(output_file_path, out_volume_np, bigtiff=True)
            
            print('')
            
            del out_volume_np

###############################################################################
if __name__ == "__main__" :

    folders = [
        r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260324_145316_Neurosphere_GFP_DIV7",
        # r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260313_110909_Monica_Cos7_NHS-Esther_x4_copie",
        ]
    for folder in folders :
        auto_deskew_rotate_mda(folder)
        auto_deskew_rotate_ls3(folder)