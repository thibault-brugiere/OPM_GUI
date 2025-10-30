# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 13:21:31 2025

@author: tbrugiere
"""
from PySide6.QtCore import QObject, Signal, QThread
import time


class CountWorker(QObject):
    trigger_received = Signal(int)  # Signal envoyé à chaque événement

    def __init__(self, daq_backend, filterwheel, filter_move, poll_interval=0.01, parent=None):
        super().__init__(parent)
        self.daq = daq_backend
        self.filterwheel = filterwheel
        self.filter_move = filter_move
        self.n_filters = len(self.filter_move)
        
        self._running = False
        self._last_count = 0
        self.poll_interval = poll_interval
        

    def start(self):
        self._running = True
        self._run_loop()
        

    def stop(self):
        self._running = False

    def _run_loop(self):
        while self._running:
            try:
                count = self.daq.read_count()
                # print(f'count_worker: {count}')
                if count > self._last_count:
                    self.trigger_received.emit(count)
                    self.goto_next_filter(count)
                self._last_count = count
            except Exception as e:
                print("[Count Worker]Erreur :", e)
            time.sleep(self.poll_interval)

    def get_count(self):
        return self._last_count
    
    def goto_next_filter(self, count):
        """Sélectionne le filtre correspondant au count (cyclique) et déplace la roue."""
        idx = int((count) % self.n_filters)
        next_move = self.filter_move[idx]
        """
        time.sleep(0.3)        
        self.filterwheel.setTrigFilter(next_filter) 
        Je ne peux pas utiliser cette méthode
        Car la lecture de la position est trop longue.
        """
        self.filterwheel.setTrigMove(next_move)
        
def mouvement_sequence(filters, filterseq):
    """
    Calcule les mouvements cycliques à faire sur la roue de filtres.

    Args:
        filters : Liste complète des positions de la roue (ordre physique).
        filterseq: Liste des filtres à utiliser (ordre acquisition).

    Returns:
        liste_de_mouvements: Liste des déplacements cycliques entre chaque filtre (en slots, positifs ou négatifs).
    """
    n = len(filters)
    positions = [filters.index(filtre) for filtre in filterseq]
    positions.append(positions[0])
    mouvements = []
    for i in range(1, len(positions)):
        pos_actuelle = positions[i-1]
        pos_voulue = positions[i]
        # Mouvement minimal (cyclique)
        delta_plus = (pos_voulue - pos_actuelle) % n
        if delta_plus <= n/2:
            mouvement = delta_plus
        else:
            mouvement = delta_plus - n
        mouvements.append(mouvement)
    return mouvements