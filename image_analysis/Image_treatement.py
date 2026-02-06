# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 16:54:49 2026

@author: tbrugiere
"""
import math
import numpy as np
import os
import tifffile

from deskewing import deskew_volume
from Cropping import crop_stack, compute_bleach_factors, apply_bleach_correction_tiff, save_image

aspect_ratio = 5.87370

channels = ["BFP"]

path = "C:/Users/tbrugiere/Documents/Images_OPM/20251212_Lipid_Droplets/20251212_155228_Lipid_Droplets"

crop = [0,425,2999,1010]

anchors_ratio = {
                1: 1.0,
                11: 1.3215965187956669,
                21: 1.7110911185472082,
                31: 2.116829390562918,
                41: 2.5586497308689182,
                51: 3.0835219668605185,
                }

background = 290

factors = compute_bleach_factors(60, anchors_ratio)

for channel in channels :
    
    for k in range(60) : # Nombre de fichiers du timelaps

        name = f'{channel}_volume_{k:04d}'
        
        print(f'Pre-treatement : {name}')

        file_path = os.path.join(path, f'{name}.tif')
        
        image = tifffile.imread(file_path)
        
        print("oppened")
        
        image = crop_stack(image, crop[0], crop[1] , crop[2], crop[3])
        
        print("cropped")
        
        image = apply_bleach_correction_tiff(image, factors[k])
        
        print("corrected")
        
        deskew = deskew_volume(image, aspect_ratio, angle = 40, angle_unit = "deg")
        
        deskew.deskew_volume()
        
        print("deskewed")
        
        deskew.save_numpy_image(f'deskew_{name}',f'{path}/cropped_deskew_corrected/')
        
        print(" ")