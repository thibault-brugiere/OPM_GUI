# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 08:41:13 2025

@author: tbrugiere
"""
import math
import numpy as np
import os
from scipy.sparse import csc_array, dia_array, lil_array
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
        self.aspect_ratio = aspect_ratio
        self.angle = angle
        
        self.angle = angle if angle_unit == "rad" else np.deg2rad(angle)
            
        self.planes , self.height, self.width = self.images.shape
        
        self.px_shift_calculation()
        self.image_translation()
    
    def image_translation(self):
        """
        Translate each image in the volume according to the calculated pixel shift.
        """
        self.shifted_images = list()
        for image_index in range(0,self.planes) :
            self.shifted_images.append(self.create_shifted_image(image_index))
            
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
        
    def create_shifted_image(self, image_index):
        """
        Create a shifted sparse matrix for the given image index.
        """
        # Create a sparce matrix LIL (easier for indexation)
        image = self.images[image_index]
        total_rows = self.height + self.planes*self.px_shift
        sparse_matrix = lil_array((total_rows, self.width), dtype=image.dtype)
        
        # Calculate position for the insertion
        start_row = self.px_shift * image_index
        end_row = start_row + image.shape[0]

        # Insert image in the matrix
        sparse_matrix[start_row:end_row, 0:self.width] = image
    
        # Convert LIL matrix into CSC matrix for space saving
        shifted_image = sparse_matrix.tocsc()
    
        return shifted_image

    def save_shifted_image(self, name='Beads_deskew', path=''):
        """
        Save the shifted images as a TIFF stack.

        """
        # Convert each CSC matric into en tableau dense et les empiler
        image = [shifted_image.toarray() for shifted_image in self.shifted_images]
        stacked_images = np.stack(image, axis=0)
        
        # Chemin vers le fichier TIFF de sortie
        output_file_path = f'{path}{name}.tiff'
        
        # Enregistrer le tableau empilé en tant que fichier TIFF compressé
        tifffile.imwrite(output_file_path, stacked_images, compression='zlib')
        
        print(f"Volume TIFF enregistré sous {output_file_path}")
    
    def legalize_voxel_aspect_ratio(aspect_ratio, angle):
        """
        Pixels between two frames, 
        We need the pixels aligned in the R' frame, and we have the relation:
        tan(theta) = x'/z'
        So in order to keep the tilting angle, the aspect ratio must be a multiple
        of tan(theta), with theta the tilting angle.
        """
        return max(int(round(aspect_ratio / math.tan(angle))), 1) * math.tan(angle)
    
###############################################################################

if __name__ == '__main__':
    
    name = "volume_561_t0000"
    
    path = "D:/EqSibarita/Images/OPM/250707_Continuous-Plane_Acquisition/2025-07-07_15-35-02_Beads_1um_AR6_plane_Acquisition/561"
    
    file_path = os.path.join(path, f'{name}.tif')
    
    image = tifffile.imread(file_path)
    
    volume = deskew_volume(image, aspect_ratio = 5.959, angle = 50, angle_unit = "deg")
    
    volume.save_shifted_image(f'deskew_{name}',f'{path}/')
    
#     image = tifffile.imread("Beads.tif")
    
#     volume = deskew_volume(image, aspect_ratio = 3, angle = 45, angle_unit = "deg")
    
    