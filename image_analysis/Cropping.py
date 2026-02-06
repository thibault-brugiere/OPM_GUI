# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 14:58:45 2026

@author: tbrugiere
"""
import math
import numpy as np
import os
import tifffile

def crop_stack(arr, x1: int, y1: int, x2: int, y2: int):
    """
    arr can be:
      - (H, W) single image
      - (N, H, W) stack
      - (N, H, W, C) etc. (we crop only H,W axes as last two axes)
    We assume last two axes are (H, W).
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

def compute_bleach_factors(n_frames: int, anchors: dict[int, float]) -> np.ndarray:
    """
    Facteur multiplicatif par frame (1..n_frames) par interpolation linéaire.
    anchors : {frame_index_1based: ratio}
      ex: {1:1.0, 11:1.32, 21:1.71, ...}
    """
    items = sorted(anchors.items())
    x = np.array([k for k, _ in items], dtype=float)   # frames (1-based)
    y = np.array([v for _, v in items], dtype=float)   # ratios

    frames = np.arange(1, n_frames + 1, dtype=float)
    factors = np.interp(frames, x, y, left=y[0], right=y[-1])
    return factors

def apply_bleach_correction_tiff(img, factor: float, background: float = 0.0):
    """
    Applique la correction de bleaching à UNE image TIFF :
    - (img - background) * factor + background
    puis sauvegarde.
    
    Parameters
    ----------
    img : array
        image a corriger
    factor : float
        Facteur multiplicatif de correction pour cette frame.
    background : float
        Background constant (ex: 1) à préserver.
    """
    if img.dtype != np.uint16:
        raise TypeError(f"Image dtype is {img.dtype}, expected uint16.")
    
    img_f = img.astype(np.float32, copy=False)
    corrected = (img_f - background) * float(factor) + background
    
    corrected = np.clip(corrected, 0, 65535).astype(np.uint16)
    
    return corrected
        
def save_image(image, name = "numpy_deskewed", path=''):
    """
    Save the shifted images as a TIFF stack.

    """
    
    output_file_path = f'{path}{name}.tif'
    tifffile.imwrite(output_file_path, image, compression='zlib')


###############################################################################

if __name__ == '__main__':
    
    # channels_list = ["BFP","GFP", "CY3.5", "TexRed"]
    
    channels = ["BFP"]
    
    # # path = "D:/Projets_Python/OPM_GUI/Images/20251212_Lipid_Droplets/20251212_155228_Lipid_Droplets"
    # path = "C:/Users/tbrugiere/Documents/Images_OPM/20251212_Lipid_Droplets/20251212_155228_Lipid_Droplets"
    # # path = "D:/Projets_Python/OPM_GUI/Images/20251205_153047_PSF_4Color_170nmBeads" 
    
    # # time_code = ['20251217_170044','20251217_170619']
    
    # # for time in time_code :
    # #     print(f'FOLDER : {time}')
    
    # for channel in channels :
        
    #     for k in range(60) : # Nombre de fichiers du timelaps
    
    #         name = f'{channel}_volume_{k:04d}'
            
    #         print(f'Cropping {name}')


    #         file_path = os.path.join(path, f'{name}.tif')
            
    #         image = tifffile.imread(file_path)
            
    #         cropped_image = crop_stack(image, 0, 512 , 2999, 1023)
            
    #         save_image(cropped_image, f'{name}',f'{path}/cropped/')
            
    # path = "D:/Projets_Python/OPM_GUI/Images/20251212_Lipid_Droplets/20251212_155228_Lipid_Droplets"
    path = "C:/Users/tbrugiere/Documents/Images_OPM/20251212_Lipid_Droplets/20251212_155228_Lipid_Droplets/cropped/deskewed"
    # path = "D:/Projets_Python/OPM_GUI/Images/20251205_153047_PSF_4Color_170nmBeads" 
    
    # time_code = ['20251217_170044','20251217_170619']
    
    # for time in time_code :
    #     print(f'FOLDER : {time}')
    
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
    
            name = f'deskew_{channel}_volume_{k:04d}'
            
            print(f'correcting {name}')

            file_path = os.path.join(path, f'{name}.tiff')
            
            image = tifffile.imread(file_path)
            
            corr_image = apply_bleach_correction_tiff(image, factors[k], background)
            
            save_image(corr_image, f'corr_{name}',f'{path}/corrected/')