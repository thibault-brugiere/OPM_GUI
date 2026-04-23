# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 11:49:57 2026

@author: tbrugiere
"""

from PySide6.QtCore import QObject, Signal, Slot

class pretreatementWorker(QObject):
    """
    Woker used by GUI_pretreatement to run the different process
    """
    progress_folder = Signal(int,int,str)
    progress_file = Signal(int,int)
    finished = Signal()
    stopped = Signal()
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.on_init()
        
        
    def on_init(self):
        pass
    
    @Slot()
    def request_stop(self):
        """
        Started when user request to stop the actual process
        """
        self._stop_requested = True
    
    @Slot(object, str)
    def start(self, pretreatement, folder):
        """
        Start the pretreatement process

        Parameters
        ----------
        pretreatement : function
            pretreatement function to proceed
        folder : str
            path of the folder containing image to process

        """
        self._stop_requested = False
        
        pretreatement(folder,
                      progress_folder_callback = self.progress_folder.emit,
                      progress_file_callback = self.progress_file.emit,
                      stop_requested_callback=lambda: self._stop_requested)
        
        if self._stop_requested:
            self.stopped.emit()
        else:
            self.finished.emit()