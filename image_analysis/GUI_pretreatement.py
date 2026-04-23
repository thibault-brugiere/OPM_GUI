# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 11:40:06 2025

@author: tbrugiere
"""

"""
Convert file.ui to file.py

pyside6-uic widget/ui_channel_editor.ui -o widget/ui_channel_editor.py

pyside6-uic D:/Projets_Python/OPM_GUI/image_analysis/ui_pretreatement.ui -o D:/Projets_Python/OPM_GUI/image_analysis/ui_pretreatement.py

"""
from functools import partial
import os
import sys
import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QThread, Signal

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

from image_analysis.ui_pretreatement import Ui_Form
from image_analysis.parsename import parse_mda_filenames, parse_ls3_filenames, parse_ls3_foldernames, parse_ls3_deskew_foldernames
from image_analysis.Auto_deskew_rotate_cupy import auto_deskew_rotate_mda
from image_analysis.Auto_deskew_rotate_cupy import auto_deskew_rotate_ls3 as auto_deskew_rotate_ls3_entire_volume
from image_analysis.Auto_deskew_rotate_cupy import ImageTooLargeError
from image_analysis.Zarr_conversion import auto_convert_tiffs_to_zarr
from image_analysis.Zarr_conversion import auto_convert_zarr_to_tiffs
from image_analysis.Auto_deskew_rotate_ls3_zarr import auto_deskew_rotate_ls3

from GUI_pretreatement_worker import pretreatementWorker

class PretreatementWindow(QWidget, Ui_Form):
    """
    Show the window to set default camera size
    """
    
    start_worker = Signal(object, str)

    def __init__(self, folder_path = None, parent=None):
        """
        channels : dictionnary of channel objects 
        """
        
        super().__init__(parent)
        self.setupUi(self)
        
        self.folder_path = folder_path
        
        #
        # Prepare the threading
        #
        
        self.pretreatementThread = QThread()
        self.pretreatementWorker = pretreatementWorker()
        self.pretreatementWorker.moveToThread(self.pretreatementThread)
        
        self.start_worker.connect(self.pretreatementWorker.start)
        
        self.pretreatementWorker.progress_folder.connect(self.update_progress_folder_bar)
        self.pretreatementWorker.progress_file.connect(self.update_progress_file_bar)
        self.pretreatementWorker.finished.connect(self.on_finished)
        self.pretreatementWorker.stopped.connect(self.on_stopped)

        self.pretreatementThread.start()
        
        self.on_init()
        
    def on_init(self):
        #
        # Initialisation of the window
        #
        
        self.setWindowTitle('Pretreatement')
        self.setWindowFlag(Qt.Window)  # Assure que la fenêtre est indépendante
        self.label_parameters.setText("Ready")
        
        if self.parent() is not None :
            pass
        
        #
        # Initialisation of the variables
        #
        
        self.folder_path = None
        self.parse_mda = None
        self.parse_ls3_file = None
        self.parse_ls3_folder = None
        self.parse_ls3_deskew = None
        
        self.processing_image_name = ""
        
        self.status = 'idle'
        self.ls3_full_process = "False"
        
        #
        # Values for displaying
        #
        
        self._last_progress_folder_update = 0.0
        self._last_progress_file_update = 0.0
        self._min_progress_interval = 0.1  # 100 ms
        
        #
        # Tur off unused buttons
        #
        
        self._pb_setEnabled()
        
        ##############################################
        ## Connection between functions and buttons ##
        ##############################################
        
        self.pb_select_folder.clicked.connect(self.pb_select_folder_clicked)
        self.pb_detect_files.clicked.connect(self.pb_detect_files_clicked)
        self.pb_start_MDAdeskew.clicked.connect(self.pb_start_MDAdeskew_clicked)
        self.pb_start_LS3deskew.clicked.connect(self.pb_start_LS3deskew_clicked)
        self.pb_ZARRconvert.clicked.connect(self.pb_ZARRconvert_clicked)
        self.pb_start_LS3deskew_ZARR.clicked.connect(self.pb_start_LS3deskew_ZARR_clicked)
        self.pb_TIFFconvert.clicked.connect(self.pb_TIFFconvert_clicked)
        self.pb_stop.clicked.connect(self.pb_stop_clicked)
        
        #################################
        ## Fonctions called by buttons ##
        #################################
        
    def _pb_setEnabled(self, enabled = False):
        """
        set the enabled state of different buttons of the interface

        Parameters
        ----------
        enabled : bool, optional
            state of the buttons. The default is False.
        """
        self.pb_start_MDAdeskew.setEnabled(enabled)
        self.pb_start_LS3deskew.setEnabled(enabled)
        self.pb_ZARRconvert.setEnabled(enabled)
        self.pb_start_LS3deskew_ZARR.setEnabled(enabled)
        self.pb_TIFFconvert.setEnabled(enabled)
        
        self.cb_only_deskew.setEnabled(enabled)
        self.cb_try_no_ZARR.setEnabled(enabled)
        self.cb_delete_zarr.setEnabled(enabled)
        
        self._reset_progress_bar()
    
    def _reset_progress_bar(self) :
        """
        Reset the progress bar to 0%

        Returns
        -------
        None.

        """
        self.progressBar_folder.setMaximum(100)
        self.progressBar_folder.setValue(0)
        self.progressBar_actual_step.setMaximum(100)
        self.progressBar_actual_step.setValue(0)
        
    def pb_select_folder_clicked(self):
        """
        Select the folder where data will be processed
        stored in self.folder_path
        """
        self.folder_path = QFileDialog.getExistingDirectory(self, "Select images Directory")
        
        self._pb_setEnabled()
        
        if self.folder_path is not None :
            self.label_folder.setText(self.folder_path )
            self.label_folder.adjustSize()
            self.pb_detect_files.setEnabled(True)
            
    def pb_detect_files_clicked(self):
        """
        Automatically detect files to process in the selected folder
        stored in self.parse_mda, self.parse_ls3_file, self.parse_ls3_folder and self.parse_ls3_deskew = None
        Enable the appropriate buttons

        """
        if self.folder_path is not None :
            self._pb_setEnabled()
            
            self.parse_mda = parse_mda_filenames(self.folder_path)
            self.parse_ls3_file = parse_ls3_filenames(self.folder_path)
            self.parse_ls3_folder = parse_ls3_foldernames(self.folder_path)
            self.parse_ls3_deskew = parse_ls3_deskew_foldernames(self.folder_path)
            
            if len(self.parse_mda['files']) != 0: # If MDA experiment is detected
                self.label_parameters.setText("MDA detected")
                self.pb_start_MDAdeskew.setEnabled(True)
                self.cb_only_deskew.setEnabled(True)
                return
                
            
            if len(self.parse_ls3_deskew['files']) != 0: # If images already deskewed detected
                self.label_parameters.setText("LS3 file detected")
                self.pb_TIFFconvert.setEnabled(True)
                self.cb_delete_zarr.setEnabled(True)
                
            
            if len(self.parse_ls3_folder['files']) != 0: # If images already in zarr detected
                self.label_parameters.setText("LS3 file detected")
                self.pb_start_LS3deskew_ZARR.setEnabled(True)
                self.cb_delete_zarr.setEnabled(True)
                
            
            if len(self.parse_ls3_file['files']) != 0: # If ls3 images detected
                self.label_parameters.setText("LS3 file detected")
                self.pb_start_LS3deskew.setEnabled(True)
                self.pb_ZARRconvert.setEnabled(True)
                self.cb_delete_zarr.setEnabled(True)
                self.cb_try_no_ZARR.setEnabled(True)
                
            self.label_parameters.adjustSize()
        
        else :
            self.label_parameters.setText("Select a folder")
            self.label_parameters.adjustSize()
        
    def pb_start_MDAdeskew_clicked(self):
        """
        Process images if an MDA experiment is detected
        detect the status of the self.cb_only_deskew checkbox before processing
        """
        self.status = "MDA deskewing"
        function = partial(auto_deskew_rotate_mda, only_deskew = self.cb_only_deskew.isChecked())
        self.start_worker.emit(function,
                               self.folder_path)
   
    def pb_start_LS3deskew_clicked(self):
        """
        Process images if an LS3 experiment is detected
        Detect the status of the self.cb_try_no_ZARR to start the processing
        without using zarr file conversion
        """
        self.status = "LS3 deskewing"
        if self.cb_try_no_ZARR.isChecked():
            try :
                self.start_worker.emit(auto_deskew_rotate_ls3_entire_volume,
                                       self.folder_path)
            except ImageTooLargeError as e :
                self.label_parameters.setText(str(e))
                self.cb_try_no_ZARR.setCheckState(False)
        else:
            self.ls3_full_process = "zarr_conv"
            self.pb_ZARRconvert_clicked()
    
    def pb_ZARRconvert_clicked(self):
        """
        Convert TIFF images to Zarr format
        Detect if a Zarr file already exist and ask the user before overwriting it
        """
        self.status = "Zarr conversion"
        
        if len(self.parse_ls3_folder['files']) != 0:
            message = "Zarr file already existing, continue?"
            
            proceed = ask_user_confirmation(self,message)
            if proceed is False :
                self.status = "idle"
                return
            
        self.start_worker.emit(auto_convert_tiffs_to_zarr,
                               self.folder_path)
    
    def pb_start_LS3deskew_ZARR_clicked(self):
        """
        Apply deskewing to Zarr images
        Detect the status of the self.cb_delete_zarr checkbox before processing
        to delete or not the zarr processed file
        """
        self.status = "LS3 deskewing"
        
        if len(self.parse_ls3_deskew['files']) != 0 :
            message = "deskewed file already existing, continue?"
            
            proceed = ask_user_confirmation(self,message)
            
            if proceed is False :
                self.status = "idle"
                return
            
        function = partial(auto_deskew_rotate_ls3, delete = self.cb_delete_zarr.isChecked() )
        self.start_worker.emit(function,
                               self.folder_path)
    
    def pb_TIFFconvert_clicked(self):
        """
        Convert processed Zarr images to TIFF
        Detect the status of the self.cb_delete_zarr checkbox before processing
        to delete or not the zarr processed file
        """
        self.status = "TIFF conversion"
        function = partial(auto_convert_zarr_to_tiffs, delete = self.cb_delete_zarr.isChecked(), max_z_size = self.sb_max_z.value() )
        self.start_worker.emit(function,
                               self.folder_path)
        
    def pb_stop_clicked(self):
        """
        Stop the current process
        """
        self.pretreatementWorker.request_stop()
        
        ##############################
        ## Fonctions for displaying ##
        ##############################
    
    def update_progress_folder_bar(self, image = 0, total_image = 100, name = "") :
        """
        Update progressbar_folder base on the information get by the progress_file_callback process
        from GUI_pretreatelent_worker

        Parameters
        ----------
        image : int
            index of the image actually processing
        total_image : int
            total number of images to process
        name : str
            name of the image actually processing
        """
        now = time.monotonic()
        if now - self._last_progress_folder_update < self._min_progress_interval:
            return
        self._last_progress_folder_update = now
        
        self.processing_image_name = name
        self.progressBar_folder.setMaximum(total_image)
        self.progressBar_folder.setValue(image)
        self.label_parameters_update()
    
    def update_progress_file_bar(self,step = 0, total_step = 100) :
        """
        Update progressbar_file base on the information get by the progress_file_callback process
        from GUI_pretreatelent_worker

        Parameters
        ----------
        step : int, optional
            index of the step actually processing in the file. The default is 0.
        total_step : int, optional
            total steps to process in the file. The default is 100.
        """
        now = time.monotonic()
        if now - self._last_progress_file_update < self._min_progress_interval:
            return
        self._last_progress_file_update = now
        
        self.progressBar_actual_step.setMaximum(total_step)
        self.progressBar_actual_step.setValue(step)
        self.label_parameters_update()
        
    def label_parameters_update(self):
        """
        update the message of the label self.label_parameters
        """
        message = f"""{self.status}
        {self.progressBar_folder.value()} / {self.progressBar_folder.maximum()}
        {self.progressBar_actual_step.value()} / {self.progressBar_actual_step.maximum()}
        {self.processing_image_name}"""
        self.label_parameters.setText(message)
        self.label_parameters.adjustSize()
        
    def on_stopped(self):
        self.label_parameters.setText("stopped")
        self.status = 'idle'
    
    def on_finished(self):
        """
        function called when the actual process is finished
        If the full ls3 process was running (after pb_start_LS3deskew_clicked function),
        it will continue the processing with the deskewing and conversion
        """
        self._reset_progress_bar()
        
        if self.ls3_full_process == "zarr_conv" :
            self.pb_start_LS3deskew_ZARR_clicked()
            self.ls3_full_process = "ls3_deskew"
            return
        elif self.ls3_full_process == "ls3_deskew":
            self.pb_TIFFconvert_clicked()
            self.ls3_full_process = "False"
            return

        self.label_parameters.setText("finished")
        self.status = 'idle'
        self.pb_detect_files_clicked()
        
    #################################
    ## Fonctions called by buttons ##
    #################################         
        
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Confirmer changes',
            """"Are you sure you want to exit?""",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Yes:
            event.accept()
        elif reply == QMessageBox.No:
            event.ignore()
        else:
            event.accept()
            
def ask_user_confirmation(parent=None, message: str = None) -> bool:
    """
    A window that open when the programs need user confirmation to proceed

    Parameters
    ----------
    parent : TYPE, optional
        Parent process that needs the user confirmation. The default is None.
    message : str, optional
        Message displayed by the window. The default is None.

    Returns
    -------
    bool
        confirmation from the user.

    """
    if message is None :
        message = "Would you like to proceed?"

    reply = QMessageBox.question(
        parent,
        "Confirmation",
   		message,
   		QMessageBox.Yes | QMessageBox.No,
   		QMessageBox.No  # bouton par défaut
           )
    
    return reply == QMessageBox.Yes

##############################################################################
if __name__ == '__main__':
    app = QApplication(sys.argv)

    editor = PretreatementWindow()
    editor.show()
    sys.exit(app.exec())