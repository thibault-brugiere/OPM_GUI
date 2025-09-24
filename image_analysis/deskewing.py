# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 08:41:13 2025

@author: tbrugiere
"""
import math
import numpy as np
import os
import tifffile

class functions_tiff():
    
    def open_tiff():
        pass
    
    def save_tiff():
        pass
    
    def compress_tiff():
        pass

class deskew_volume(object):
    
    def __init__(self, images, aspect_ratio, angle, angle_unit = "rad"):
        """
        
        Args:
        image (tiff) : volume acquired from OPM microscope
        aspect_ratio (float) : ratio of the distance between two plane and piexel
            size of the camera.
        angle (float) : angle in between focal plane of the objective
            and bessel beam. It can be in radian or degree, defined aby angle_unit
            default is radian.
        angle_unit (str) : unit of the angle, can be "deg" or "rad"

        """
        self.images = images
        self.deskewed_image = None
        self.aspect_ratio = aspect_ratio
        self.angle = angle
        
        self.angle = angle if angle_unit == "rad" else np.deg2rad(angle)
        
        self.px_shift_calculation()

    def px_shift_calculation(self):
        """
        Calculate the pixel translation between two frames.

        Returns:
        self.px_shift (int) : shifting in pixels between two frames

        """
        
        px_shift = self.aspect_ratio/math.tan(self.angle)
        
        int_px_shift = round(px_shift)
        
        if not math.isclose(px_shift, int_px_shift, rel_tol=0.0001):
            raise ValueError(f'Aspect ratio is not legal, pixel shift = {px_shift}')
            
        self.px_shift =int(int_px_shift)
    
    def deskew_volume(self):
        self.deskewed_image = self.deskew_numpy(volume = self.images, px_shift_y = self.px_shift)

    def save_numpy_image(self, name = "numpy_deskewed", path=''):
        """
        Save the shifted images as a TIFF stack.

        """
        if self.deskewed_image is not None :
            output_file_path = f'{path}{name}.tiff'
            tifffile.imwrite(output_file_path, self.deskewed_image, compression='zlib')
            
            print(f"Volume TIFF enregistré sous {output_file_path}")
        else:
            raise ValueError("No deskewed image")
    
    def legalize_voxel_aspect_ratio(aspect_ratio, angle):
        """
        Pixels between two frames, 
        We need the pixels aligned in the R' frame, and we have the relation:
        tan(theta) = x'/z'
        So in order to keep the tilting angle, the aspect ratio must be a multiple
        of tan(theta), with theta the tilting angle.
        """
        return max(int(round(aspect_ratio / math.tan(angle))), 1) * math.tan(angle)
    
    def deskew_numpy(self, volume: np.ndarray, px_shift_y: int = 0, px_shift_x: int = 0) -> np.ndarray:
        """
        Deskew a 3D volume (Z, Y, X) by shifting each Z-slice along Y and/or X
        by a fixed number of pixels per slice.

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
    
###############################################################################

if __name__ == '__main__':
    
    name = "Beads_01"
    
    path = "D:\Projets_Python\OPM_GUI\image_analysis"
    
    file_path = os.path.join(path, f'{name}.tif')
    
    image = tifffile.imread(file_path)
    
    volume = deskew_volume(image, aspect_ratio = 0.8390996311772799, angle = 40, angle_unit = "deg")
    
    volume.deskew_volume()

    volume.save_numpy_image(f'deskew_{name}',f'{path}/')
    