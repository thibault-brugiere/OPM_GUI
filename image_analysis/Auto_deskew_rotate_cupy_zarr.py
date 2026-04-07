# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 16:54:49 2026

@author: tbrugiere

This program should be run with the environnement OPM_gpu that contains the library
cupyx
"""
import gc
import math
import numpy as np
import cupy as cp
import os
from pathlib import Path
import tifffile
import zarr

from deskew_rotate_cupyx import deskew_and_rotate_opm as deskew_rotate
import parsename
import preprocessing

import time as t

def open_x_slices_zarr(buffer : np.ndarray, file_path:list,x_start:int, x_end:int):
    file = file_path + r"\ZarrFiles.zarr"
    z = zarr.open(file, mode="r")
    return z[:, :, x_start:x_end]

def auto_deskew_rotate(folders):
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
                    tifffile.imwrite(output_file_path, out_volume_np, bigtiff=True, compression=None)
            
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
                        y, x = shape[1:3]
                    print(f'y: {y} x: {x}')
                    
                    total_size = int(np.sum(size_list))                    
                    
                    x_slices = x
                    y_slices = y
                    steps = 32
                    step_size = math.ceil(x_slices / steps)
                    
                    sub_volume_buffer = np.empty((total_size, y_slices, step_size), dtype=np.uint16)
                    
                    for k in range(steps):
                        print(f'\rpart {k + 1}/{steps}', end = "")
                        
                        sub_volume_zyx = open_x_slices_zarr(sub_volume_buffer,
                                                            folder,
                                                            k*step_size,
                                                            min((k+1) * step_size, x_slices))
                        
                        out_volume_cp = deskew_rotate(
                            cp.asarray(sub_volume_zyx),
                            dy_um = metadata["px_size"],
                            aspect_ratio = metadata["aspect_ratio"],
                            theta_deg = metadata["angle"])
                        
                        if k == 0 :
                            z,y = out_volume_cp.shape[-3],out_volume_cp.shape[-2]
                            
                            out_file = folder + r"\deskew.zarr"
                            
                            zarr_array = zarr.open(
                            out_file,
                            mode="w",
                            shape=(z, y, x_slices),
                            chunks=(64, y , step_size),
                            dtype=np.uint16,
                        )

                        zarr_array[:,:,k*step_size : min((k+1) * step_size, x_slices)] = out_volume_cp
                        
                        del out_volume_cp
                        del sub_volume_zyx
                        gc.collect()
                        cp.get_default_memory_pool().free_all_blocks()
                    
                    print('deskew_rotate finished')
                    
                    print('saving')
                    
                    print('volume saved')
                                
            
###############################################################################
if __name__ == "__main__" :

    folders = [
        r"C:\Users\tbrugiere\Documents\Images_OPM\20260330_154402_Image",
        # r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260313_110909_Monica_Cos7_NHS-Esther_x4"
        ]
    t0 = t.time()
    auto_deskew_rotate(folders)
    t1 = t.time()
    print(f'TOTAL TIME : {t1-t0}s')