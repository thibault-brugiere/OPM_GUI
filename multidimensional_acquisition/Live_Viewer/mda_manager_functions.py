# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 11:57:36 2025

@author: tbrugiere
"""
import cv2
import matplotlib.pyplot as plt
import numpy as np


    
def update_timelapse_strip(strip: np.ndarray, new_image: np.ndarray, max_images: int = 100) -> np.ndarray:
    """
    Ajoute une nouvelle image verticale à la frise temporelle.
    
    strip : np.ndarray
        Image 2D (H, W) représentant la frise (128px de haut, largeur variable).
    new_image : np.ndarray
        Projection frontale (image verticale 2D à concaténer sur la droite).
    max_images : int
        Nombre maximum d’images dans la frise.
    
    Retourne :
        Frise mise à jour (np.ndarray)
    """
    if new_image.shape[0] != 128:
        new_image = resize_image_to_height(new_image, 128)
    
    # Ajouter une ligne blanche de séparation
    separator = np.full((128, 1), 255, dtype=new_image.dtype)  # 2px blancs
    separator2 = np.full((128, 1), 0, dtype=new_image.dtype)
    
    # Nouvelle image avec séparateur
    padded_image = np.hstack((separator, new_image))
    padded_image = np.hstack((separator2, new_image))

    if strip is None:
        return padded_image

    updated = np.hstack((strip, padded_image))

    # Limiter à `max_images`
    strip_width_per_image = new_image.shape[1] + 2
    max_width = strip_width_per_image * max_images
    if updated.shape[1] > max_width:
        updated = updated[:, -max_width:]

    # debug_display_ndarray(updated, title="Frise projection")
    
    return updated
    
def resize_image_to_height(img: np.ndarray, target_height: int) -> np.ndarray:
    h, w = img.shape
    scale = target_height / h
    target_width = int(w * scale)
    resized = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_AREA)
    return resized

def get_timeline_frame_width(img: np.ndarray):
    h, w = img.shape
    scale = 128 / h
    target_width = int(w * scale)

    return target_width

def debug_display_ndarray(img: np.ndarray, title="Debug Image"):
    plt.figure(figsize=(10, 3))
    plt.imshow(img, cmap="gray", aspect="auto")
    plt.title(title)
    plt.colorbar()
    plt.show()
    
def auto_contrast(image: np.ndarray, low_perc: float = 0.5, high_perc: float = 99.5):
    """
    Calcule automatiquement les niveaux de gris pour l'affichage à contraste adapté.
    
    Args:
        image (np.ndarray): Image 2D ou 3D
        low_perc (float): Percentile bas (ex: 0.5)
        high_perc (float): Percentile haut (ex: 99.5)
    
    Returns:
        (float, float): min_grayscale, max_grayscale
    """
    flat = image.flatten()
    min_gray = np.percentile(flat, low_perc)
    max_gray = np.percentile(flat, high_perc)

    if min_gray == max_gray:
        # Évite division par zéro ou contraste nul
        min_gray, max_gray = float(flat.min()), float(flat.max())
    
    return min_gray, max_gray