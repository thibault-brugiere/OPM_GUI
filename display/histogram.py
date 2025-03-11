# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 10:53:38 2025

@author: tbrugiere
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np

from PySide6.QtCore import QThread, Signal

class HistogramThread(QThread):
    """Generate a histogram of the grayscale image and display it in a QGraphicsView.
    
    Args:
        frame (ndarray): 16-bit grayscale image.
        w_px (int): Desired width in pixels.
        h_px (int): Desired height in pixels.
        dpi (int): Resolution in dots per inch.
        line_width (int): Thickness of the histogram line.
        font_size (int): Size of the font for axis labels and ticks.
    """
    # Signal pour envoyer la scène du graphique une fois le travail terminé
    histogram_ready = Signal(np.ndarray, int, int)

    def __init__(self, frame, min_grayscale=10000, max_grayscale=50000, w_px=1200, h_px=600, dpi=200, line_width=0.5, font_size=8):
        super().__init__()
        self.frame = frame
        self.min_grayscale = min_grayscale
        self.max_grayscale = max_grayscale
        self.w_px = w_px
        self.h_px = h_px
        self.dpi = dpi
        self.line_width = line_width
        self.font_size = font_size

    def run(self):
        """ Cette fonction sera exécutée dans un thread séparé. Elle crée le graphique et l'envoie au thread principal. """
            
        hist, bins = np.histogram(self.frame, bins=256, range=(0, 65535))

        # Crée la figure et l'axe
        fig = plt.Figure(figsize=(self.w_px / self.dpi, self.h_px / self.dpi), dpi=self.dpi)
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        # Trace l'histogramme
        ax.plot(bins[:-1], hist, color="black", linewidth=self.line_width)
        ax.set_xlim(0, 65535)

        # Définir la taille de la police pour les axes
        ax.tick_params(axis='both', which='major', labelsize=self.font_size)
        ax.set_xlabel('Gray Value', fontsize=self.font_size)
        ax.set_ylabel('Density', fontsize=self.font_size)

        # Ajoute les position des min et max gray value
        ax.axvline(x=self.min_grayscale, color='blue', linestyle='--', linewidth=self.line_width)
        ax.axvline(x=self.max_grayscale, color='red', linestyle='--', linewidth=self.line_width)


        # Masquer l'axe y
        ax.set_yticklabels([])

        # Convertir le graphique en image
        canvas.draw()
        w, h = canvas.get_width_height()
        image_data = np.frombuffer(canvas.buffer_rgba(), dtype=np.uint8).reshape(h, w, 4)
        
        # Émettre le signal pour informer le thread principal que l'histogramme est prêt
        self.histogram_ready.emit(image_data, w, h)
        
    def stop(self):
        """Arrête proprement l'acquisition."""
        self.running = False
        self.quit()
        self.wait()