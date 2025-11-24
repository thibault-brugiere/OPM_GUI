# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 14:37:39 2025

@author: tbrugiere
"""
import math
import numpy as np
import os
import tifffile as tiff

class OPMReconstruction():
    
    def __init__(
            self,
            src_path : str,
            dst_path : str,
            aspect_ratio : float,
            angle : float,
            chunk_size : int = 8,
            direction : str = "y",
            compute_mip : bool = False,
            bigtiff: bool = True,
            ):
        self.src_path = src_path
        self.dst_path = dst_path
        self.aspect_ratio = aspect_ratio
        self.angle = angle
        self.chunk_size = chunk_size
        self.direction = direction
        self.compute_mip = compute_mip
        self.bigtiff = bigtiff
        
        self.px_shift_calculation()
        
        # Métadonnées source
        with tiff.TiffFile(self.src_path) as tf:
            self.n_frames = len(tf.pages)
            if self.n_frames == 0:
                raise ValueError("Aucune image dans le fichier source.")
            first_image = tf.pages[0].asarray()
            self.image_dtype = first_image.dtype
            self.in_h, self.in_w = first_image.shape[-2], first_image.shape[-1]
            
        # Détermination taille de sortie (on ajoute l'amplitude max du décalage)
        if self.direction == "y":
            self.px_shift_y = abs(self.px_shift) * (self.n_frames - 1)
            self.px_shift_x = 0
        elif self.direction == "x":
            self.px_shift_x = abs(self.px_shift) * (self.n_frames - 1)
            self.px_shift_y = 0
        else:
            raise ValueError(f"Direction should be 'x' or 'y', actual : {direction}")
        
        self.out_h = self.in_h + add_h
        self.out_w = self.in_w + add_w
        
        if self.compute_mip:
            self.mip = np.ndarray((self.out_h,self.out_w), self.image_dtype)
            self.mean_projection = np.ndarray((self.out_h,self.out_w), self.image_dtype)
        
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
        
    def _translate_image(self, image: np.ndarray, z) -> np.ndarray:
        """
        Deskew a 3D volume (Z, Y, X) by shifting each Z-slice along Y and/or X
        by a fixed number of pixels per slice.

        Parameters:
        - volume: np.ndarray of shape (Z, Y, X)
        - z : image position in the volume

        Returns:
        - np.ndarray of shape self.out_h, self.out_w
        """

        out_image = np.zeros((self.out_h,self.out_w), dtype = self.image_dtype)

        y_start = z * self.px_shift_y if self.px_shift_y >= 0 else new_Y - Y - z * abs(self.px_shift_y)
        y_end = y_start + Y

        x_start = z * self.px_shift_x if self.px_shift_x >= 0 else new_X - X - z * abs(px_shift_x)
        x_end = x_start + X

        deskewed[z, y_start:y_end, x_start:x_end] = volume[z]

        return deskewed
        
        