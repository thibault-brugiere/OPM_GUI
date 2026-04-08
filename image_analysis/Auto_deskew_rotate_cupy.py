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

def auto_deskew_rotate(folders, max_shear_size = 2e9):
    for folder in folders:
        print(folder)
        parse_mda = parsename.parse_mda_filenames(folder)
        parse_ls3 = parsename.parse_ls3_filenames(folder)
        metadata = parsename.get_metadata(folder)
        
        if len(parse_mda['files']) != 0 :
            process = 'mda'
            parse = parse_mda
        elif len(parse_ls3['files']) != 0:
            process = 'ls3'
            parse = parse_ls3
        else:
            print("No image to process")
            
        for file in parse["files"] :
            if process == 'mda' :
                if file['process'] :
                    file_path = Path(file['path'])
                    name = file_path.name
                    print(name)
                    
                    volume_zyx = tifffile.imread(file_path)
                    volume_zyx_cp = cp.asarray(volume_zyx)
                    
                    volume_zyx_cp = preprocessing.subtract_bg_xy_gpu(volume_zyx_cp, 20)
                        
                    out_volume = deskew_rotate(volume_zyx_cp, dy_um = metadata["px_size"],
                                               aspect_ratio = metadata["aspect_ratio"],
                                               theta_deg = metadata["angle"])
                    
                    out_volume_np = cp.asnumpy(out_volume)
                    
                    output_file_path = f'{folder}/dekew-rotate_{name}'
                    tifffile.imwrite(output_file_path, out_volume_np, bigtiff=True, compression='zlib')
            
        if process == 'ls3':
            for position in parse_ls3["positions"] :
                for channel in parse_ls3["channels"]:
                    
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
                        y,x = tifffile.TiffFile(file_path).series[0].shape[1:3]
                    
                    total_size = int(np.sum(size_list))
                    volume_zyx = np.empty((total_size,y,x), dtype = np.uint16)
                    start=0

                    for k in range(len(file_path_list)):
                        file_path = file_path_list[k]
                        end = start + size_list[k]
                        volume_zyx[start : end,:,:] = tifffile.imread(file_path)
                        start = end 
                        
                        print(f'charged : {k} / {len(parse_ls3["index"])-1}')
                    
                    
                    z, y, x_slices = volume_zyx.shape                    
                    
                    px_shift = px_shift_calculation(metadata["aspect_ratio"], metadata["angle"], angle_unit = "deg")
                    shear_size_zy = z * ( z - 1 ) * px_shift + z * y # during shearing
                    max_step_size = max_shear_size / shear_size_zy
                    
                    steps = math.ceil(x_slices / max_step_size)
                    
                    print(steps)
                    
                    step_size = math.ceil(x_slices / steps)
                    
                    print(f'X: {volume_zyx.shape[-1]} Y: {volume_zyx.shape[-2]} Z: {volume_zyx.shape[-3]}, stepsize: {step_size}')
                    
                    for k in range(steps):
                        print(f'part {k}/{steps-1}')
    
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
                    
                    print('deskew_rotate finished')
                    
                    print('saving')
                            
                    output_file_path = f'{folder}/test_dekew-rotate_{name}.tif'
                    tifffile.imwrite(output_file_path, out_volume_np, bigtiff=True)
                    
                    print('volume saved')
                    
                    del out_volume_np
                            
    
                                
            
###############################################################################
if __name__ == "__main__" :

    folders = [
        r"C:\Users\tbrugiere\Documents\Images_OPM\20260330_154402_Image",
        # r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260313_110909_Monica_Cos7_NHS-Esther_x4"
        ]
    
    auto_deskew_rotate(folders)