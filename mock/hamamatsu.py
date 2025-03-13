# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:46:19 2025

@author: tbrugiere
"""

import numpy as np
import time
from scipy.ndimage import zoom

class DCAM:
    def __init__(self):
        pass
        
    def get_cameras_number():
        return 2
    
    class DCAMCamera(object):
        
        def __init__(self, camera_id):
            self.cav = {'camera_id' : camera_id,
                        'image_detector_pixel_num_horz' : 4000,
                        'image_detector_pixel_num_vert' : 2000,
                        'image_detector_pixel_width' : 5,
                        'subarray_hsize' : 4000,
                        'subarray_vsize' : 2000,
                        'binning' : 1,
                        'internal_line_interval' : 7.309e-06,
                        # "pixel_size" : 5
                        }
            
        def get_attribute_value(self,key):
            value = self.cav[key]
            return value

        def get_detector_size(self):
            return self.cav['image_detector_pixel_num_horz'], self.cav['image_detector_pixel_num_vert']
        
        def set_exposure(timing):
            pass
        
        def start_acquisition(bla,blabla, blablabla):
            pass
        
        def close(self):
            pass
        
        def clear_acquisition(self):
            pass
        
        def read_multiple_images(self):
            """
            Simule la capture d'une image par une caméra de hamamatsu.
            
            Cette fonction crée une instance de Frame avec des dimensions spécifiées dans les paramètres
            de la caméra, simulant ainsi la capture d'une image par une caméra réelle.
            
            Args:
                camera_id (str): Identifiant de la caméra utilisée pour la capture.
            
            Returns:
                list: Liste contenant l'instance de Frame, une chaîne vide, et les dimensions de l'image.
            """
            frame = self.generate_gradient()
            frames = [frame]
            
            return frames
        
        def generate_gradient(self):
            """
            Génère un motif de gradient en niveaux de gris qui semble se déplacer de bas en haut,
            en générant d'abord une image plus petite puis en la redimensionnant.
        
            Returns:
                numpy.ndarray: Tableau 2D contenant le motif de gradient en niveaux de gris.
            """
            # Dimensions réduites pour la génération initiale
            small_hsize = self.cav['subarray_hsize'] // 4
            small_vsize = self.cav['subarray_vsize'] // 4
        
            # Obtenir le temps actuel en secondes avec précision en millisecondes
            current_time = time.time()
        
            # Calculer un décalage vertical basé sur le temps
            offset = int((current_time * 50) % small_vsize)
        
            # Créer un gradient vertical en niveaux de gris avec décalage
            y = np.arange(small_vsize)
            gradient_column = ((y + offset) % small_vsize).astype(np.uint16)
        
            # Normaliser les valeurs pour qu'elles soient dans la plage des 16 bits
            gradient_column = (gradient_column / small_vsize * 65535).astype(np.uint16)
        
            # Dupliquer la colonne pour créer l'image réduite
            small_gradient = np.tile(gradient_column[:, np.newaxis], (1, small_hsize))
        
            # Redimensionner l'image à la taille finale
            gradient = zoom(small_gradient, zoom=(4, 4), order=0)  # Utilisation de l'interpolation "nearest"
        
            return gradient