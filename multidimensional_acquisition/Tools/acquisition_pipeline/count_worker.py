# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 13:21:31 2025

@author: tbrugiere
"""
from PySide6.QtCore import QObject, Signal, QThread
import time


class CountWorker(QObject):
    trigger_received = Signal(int)  # Signal envoyé à chaque événement

    def __init__(self, daq_backend, poll_interval=0.01, parent=None):
        super().__init__(parent)
        self.daq = daq_backend
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
                self._last_count = count
            except Exception as e:
                print("Erreur DAQ:", e)
            time.sleep(self.poll_interval)

    def get_count(self):
        return self._last_count