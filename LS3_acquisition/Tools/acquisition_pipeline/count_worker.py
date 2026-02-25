# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 13:21:31 2025

@author: tbrugiere
"""
from PySide6.QtCore import QObject, Signal, QThread
import time


class CountWorker(QObject):
    trigger_received = Signal(int)  # Signal envoyé à chaque événement

    def __init__(self, daq_backend, filterwheel, filterseq, poll_interval=0.01, parent=None):
        super().__init__(parent)
        self.daq = daq_backend
        self.filterwheel = filterwheel
        self.filterseq = filterseq
        self.n_filters = len(self.filterseq)
        
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