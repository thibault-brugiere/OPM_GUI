# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:46:19 2025

@author: tbrugiere
"""

import ctypes
import numpy as np
import time
from scipy.ndimage import zoom

class HamamatsuCamera(object):
    
    def __init__(self):
        self.camera = {'camera_id' : 0,
                       'subarray_hsize' : 400,
                       'subarray_vsize' : 200,
                       "binning" : 1
                       }
        
    def openCamera(self, camera_id):
        pass
    
    def uninit(self):
        pass

    def setACQMode(self, mode, number_frames, camera_id):
        pass

    def startAcquisition(self, camera_id):
        pass

    def stopAcquisition(self, camera_id):
        pass

    def _close(self):
        pass

    def close(self):
        pass

    def getFrames(self, camera_id):
        """
        Simule la capture d'une image par une caméra de hamamatsu.
        
        Cette fonction crée une instance de Frame avec des dimensions spécifiées dans les paramètres
        de la caméra, simulant ainsi la capture d'une image par une caméra réelle.
        
        Args:
            camera_id (str): Identifiant de la caméra utilisée pour la capture.
        
        Returns:
            list: Liste contenant l'instance de Frame, une chaîne vide, et les dimensions de l'image.
        """
        frame_instance = frame(hsize = self.camera['subarray_hsize'], vsize = self.camera['subarray_vsize'])
        frames = [frame_instance]
        
        data = [frames , 'rien',[self.camera['subarray_hsize'],self.camera['subarray_vsize']]]
        
        return data
    
    def setPropertyValue(self, name, prop, camera_id):
        """
        Met à jour la valeur de la propriété 'name' avec 'prop' pour la caméra spécifiée par 'camera_id'.
        
        :param name: Nom de la propriété à mettre à jour.
        :param prop: Nouvelle valeur de la propriété.
        :param camera_id: Identifiant de la caméra dans le dictionnaire.
        """
        # Vérifiez si la propriété existe pour cette caméra
        if name in self.camera:
            # Met à jour la valeur de la propriété
            if name == 'subarray_hsize' or name == 'subarray_vsize' :
                self.camera[name] = prop
        else:
            pass
    
    def closeCamera(self, camera_id):
        pass
    
class frame:
    """
    Classe représentant une image (frame) générée aléatoirement.
    
    Attributes:
        data (numpy.ndarray): Tableau 2D contenant les données de l'image en niveaux de gris 16 bits.
        avec hsize (int): Hauteur de l'imageet vsize (int): Largeur de l'image
    
    Methods:
        getData(): Retourne les données de l'image sous forme de tableau 1D aplati.
    """
    def __init__(self, hsize = 100, vsize = 200):
        
        self.hsize = hsize
        self.vsize = vsize
        self.num_gradients = 5
        
        # self.data = np.random.randint(0, 65536, (vsize, hsize), dtype=np.uint16)
        self.data = self.generate_gradient()
        
    def generate_gradient(self):
        """
        Génère un motif de gradient en niveaux de gris qui semble se déplacer de bas en haut,
        en générant d'abord une image plus petite puis en la redimensionnant.
    
        Returns:
            numpy.ndarray: Tableau 2D contenant le motif de gradient en niveaux de gris.
        """
        # Dimensions réduites pour la génération initiale
        small_hsize = self.hsize // 4
        small_vsize = self.vsize // 4
    
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
    
    def getData (self):
        return self.data.flatten()
    
class functions_daq:
    def analog_out(tension=0, output_channel='Dev1/ao0'):
        print("generation " + str(tension) + " V at " + output_channel)
    
    def digital_out (signal = True, line_name = 'Dev1/port0/line3'):
        if signal:
            print("Start signal at " + line_name)
        else:
            print("Stop signal at " + line_name)
    
    