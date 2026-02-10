# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 16:54:49 2026

@author: tbrugiere

This program should be run with the environnement OPM_gpu that contains the library
cupyx
"""

import numpy as np
import os
import tifffile
import time

from deskewing_class import deskew_volume
import preprocessing as pp
import deskewing
# from preprocessing import crop_stack, save_image, subtract_bg_xy_gpu, bleach_correction_exp

aspect_ratio = 3.3564

channels = ["BFP"]

path1 = "C:/Users/tbrugiere/Documents/Images_OPM/20260206_LipidDroplets/20260206_111018_Lipid_Droplets"

path2 = "C:/Users/tbrugiere/Documents/Images_OPM/20260206_LipidDroplets/20260206_103347_Lipid_Droplets"

crop1 = [0,30,1999,410]

crop2 = [0,50,1999,450]

parameters1 = {
    "path" : "C:/Users/tbrugiere/Documents/Images_OPM/20260206_LipidDroplets/20260206_111018_Lipid_Droplets",
    "crop" : [0,30,1999,410],
    "BFP" : {
        'I0' : 551,
        'bleach_constant' : 0.25 / 5,
        'background' : 203,
        'back_ground_substraction' : True,
        'rolling_ball_radius' : 20,
        },
    "GFP" : {
        'I0' : 304,
        'bleach_constant' : 0.0570 / 5,
        'background' : 203,
        'back_ground_substraction' : True,
        'rolling_ball_radius' : 20,
        }
    }

parameters2 = {
    "path": "C:/Users/tbrugiere/Documents/Images_OPM/20260206_LipidDroplets/20260206_103347_Lipid_Droplets",
    "crop" : [0,50,1999,450],
    "BFP" : {
        'I0' : -73,
        'bleach_constant' : -0.0572 / 5,
        'background' : 203,
        'back_ground_substraction' : True,
        'rolling_ball_radius' : 433,
        },
    "GFP" : {
        'I0' : 288,
        'bleach_constant' : 0.0517 / 5,
        'background' : 150,
        'back_ground_substraction' : True,
        'rolling_ball_radius' : 20,
        }
    }

experiments = [parameters1]

images = [0,10,20,30,40,50]

for parameters in experiments:
        
    path = parameters["path"]
    crop = parameters["crop"]
        
    
    for channel in channels :
        I0 = parameters[channel]["I0"]
        bleach_constant = parameters[channel]["bleach_constant"]
        background = parameters[channel]["background"]
        back_ground_substraction = parameters[channel]["back_ground_substraction"]
        rolling_ball_radius = parameters[channel]["rolling_ball_radius"]
        
        for i in range(60) : # Nombre de fichiers du timelaps
        # for k in images :
            
            k = i
        
            t0 = time.perf_counter()
    
            name = f'{channel}_volume_{k:04d}'
            
            print(f'Pre-treatement : {name}')
            
            #
            # Open the Image
            #
    
            file_path = os.path.join(path, f'{name}.tif')
            
            image = tifffile.imread(file_path)
            

            print("oppened")
            
            #
            # Crop the image
            #
            
            image = pp.crop_stack(image, crop[0], crop[1] , crop[2], crop[3])
            
            print("croped")
            
            #
            # Apply bleach correction
            #
            
            image = pp.bleach_correction_exp(image, k, I0, bleach_constant, background)
            
            print("bleach corrected")
            
            #
            # Substract background
            #
            if back_ground_substraction :
                # image = pp.subtract_bg_xy_gpu(image, rolling_ball_radius, gpu_id=1)
                image = pp.subtract_bg_stack_xy_gpu(image, rolling_ball_radius, gpu_id = 0)
                
                print("Background substracted       ")
            
            #
            # Deskew
            #
            px_shift = deskewing.px_shift_calculation(aspect_ratio, angle = 40, angle_unit = "deg")
            
            deskew = deskewing.deskew_numpy(image,px_shift_y=px_shift)
            
            
            print("deskewed")
            
            #
            # Save images
            #
            
            os.makedirs(f'{path}/cropped_deskew_corrected', exist_ok=True)
            
            pp.save_image(deskew, f'deskew_{name}',f'{path}/cropped_deskew_corrected/')
            
            mip = np.max(deskew, axis=0)
            
            pp.save_image(mip, f'mip_{name}', f'{path}/cropped_deskew_corrected/')
            
            duration = time.perf_counter() - t0
            
            print(f"Duration for {k:04d} : {duration:.3f} s")
            
            print(" ")