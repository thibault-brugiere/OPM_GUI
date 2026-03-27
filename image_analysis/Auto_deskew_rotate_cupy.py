# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 16:54:49 2026

@author: tbrugiere

This program should be run with the environnement OPM_gpu that contains the library
cupyx
"""

import cupy as cp
import os
from pathlib import Path
import tifffile

from deskew_rotate_cupyx import deskew_and_rotate_opm as deskew_rotate
import parsename

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
            file_path = Path(file['path'])
            name = file_path.name
            print(name)
            
            volume_zyx = tifffile.imread(file_path)
            volume_zyx = cp.asarray(volume_zyx)
                
            out_volume = deskew_rotate(volume_zyx, dy_um = metadata["px_size"],
                                       aspect_ratio = metadata["aspect_ratio"],
                                       theta_deg = metadata["angle"])
            
            out_volume = cp.asnumpy(out_volume)
            
            output_file_path = f'{folder}/dekew-rotate_{name}'
            tifffile.imwrite(output_file_path, out_volume, bigtiff=True, compression='zlib')
            
###############################################################################
if __name__ == "__main__" :

    folders = [
        r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260313_110909_Monica_Cos7_NHS-Esther_x4",
        r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260324_145316_Neurosphere_GFP_DIV7"
        ]
    
    auto_deskew_rotate(folders)