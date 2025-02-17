# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:00:36 2025

@author: tbrugiere
"""

"""
Convert file.ui to file.py

pyside6-uic ui_Control_Microscope_Main.ui -o ui_Control_Microscope_Main.py

TODO :
    Finir de programmer les boutons
    Vérifier pour les quels je veux qu'un message s'affiche
    Commener tout le texte / les fonctions
    
    => Faire afficher le streaming de la camera
"""
import os
import sys

import numpy as np
import tifffile
from PySide6 import QtWidgets
from PySide6.QtCore import QCoreApplication, QEventLoop, QTimer
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QFileDialog, QMessageBox, QComboBox

from Functions_UI import functions_ui, HistogramThread
from Functions_Hardware import CameraThread, functions_camera
from configs.config import camera, channel_config
from hardware.hamamatsu import HamamatsuCamera

from ui_Control_Microscope_Main import Ui_MainWindow
from widget_OPM_GUI import ChannelEditorWindow

class GUI_Microscope(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Show the graphical interface
    """
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.on_init()
        self.show()

    def on_init(self):
        self.setWindowTitle('Control Microscope')
        
        #Crée la status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready") #Change le message de la status bar
        
        ############################
        ## Création des Variables ##
        ############################
        
        ## Saving
        
        self.DATA_PATH = "D:/EqSibarita/Python/Control_Microscope_GUI/Images"
        self.EXP_NAME = "Image"
        
        self.setup = "Thibault" #Permet de choisir entre le Setup de Thibault et celui d'Armin
        
        ## Initialisation of the cameras
        
        self.camera = [camera(camera_id = 0 ),
                       camera(camera_id = 1)]
        
        self.camera_id = 0 # index de la caméra actuellement sélectionnée
        
        ## initialisation of the channels
        
        self.lasers = ["405","488","561","640"]
        
        self.channel_names = ['BFP','GFP','CY3.5','TexRed']
        
        self.channel = {}
        
        for channel in self.channel_names:
            self.channel[channel] = channel_config(channel, self.lasers)
        
            ### Library to set the channels
        
        self.checkBox_laser = {"405" : self.checkBox_laser_405,
                               "488" : self.checkBox_laser_488,
                               "561" : self.checkBox_laser_561,
                               "640" : self.checkBox_laser_640
                               } #Dictionnary of the laser checkboxes
        
        self.spinBox_laser_power = {"405": self.spinBox_laser_405,
                                    "488" : self.spinBox_laser_488,
                                    "561" : self.spinBox_laser_561,
                                    "640" : self.spinBox_laser_640
                                    } # Dictionnary of the laser power spin boxes
        
        self.list_channel_interface = { "checkBox_laser" :      self.checkBox_laser,
                                       "spinBox_laser_power" :  self.spinBox_laser_power,
                                       "filter" :               self.comboBox_channel_filter,
                                       "camera" :               self.comboBox_channel_camera,
                                       "exposure_time" :        self.spinBox_channel_exposure_time
                                       } # Dictionnary used to set all the interface elements for a given channel
        
        self.comboBoxes_channel_order = [] # Liste des combo boxes permettant de sélectionner les cannaux actifs
        self.active_channels = [] #contiendra la liste et l'ordre des cannaux activés
        
        self.comboBox_channel_name_set_indexes() #Ajoute tous les cannaux dans la comboBox_channel_name
                
        ## Timelaps settings
        self.timepoints = 10 # Nombre de points dans le timelaps
        self.time_intervals = 1 #temps entre deux volumes du timelaps en secondes
        self.total_duration = 10 #Durée totale du timelaps en secondes
        
        ## Scanner settings
        self.scanner_position = 0 #Position actuelle du scanner en µm
        self.scan_range = 20 # taille de la zone scannée en µm
        
        #Preview
        self.is_preview = False # Si une image est affichée dans le preview
        self.is_preview_paused = False # Si le preview est en pause
        self.preview_frame = None # Image actuellement affichée
        self.preview_camera = 0 # Camera utilisée dans le preview
        self.preview_channel = self.comboBox_channel_name.currentText() # Canal affiché dans le préview (laser et filtre)
        
        self.histogram_greyvalue_thread = None # Thread utilisé pour créer le graphique des niveaux de gris
        
        self.min_grayscale = 0 #Valeur de gris la plus basse du preview
        self.max_grayscale = 65535 #valeur de gris la plus haute du preview
        self.preview_zoom = 0.25 #rescale factor of the preview ()
        self.look_up_table = 'grayscale'
        
        #########################################
        ## Fonctions appelées pour les boutons ##
        #########################################
        
            ## Saving / Setup
        
        self.pb_data_path.clicked.connect(self.pb_data_path_value_changed)
        self.comboBox_setup.currentIndexChanged.connect(self.comboBox_setup_value_changed)
        self.lineEdit_exp_name.editingFinished.connect(self.lineEdit_exp_name_modified)
        
            ## Camera
        self.spinBox_hsize.editingFinished.connect(self.spinBox_hsize_value_changed)
        self.spinBox_hpos.editingFinished.connect(self.spinBox_hpos_value_changed)
        self.spinBox_vsize.editingFinished.connect(self.spinBox_vsize_value_changed)
        self.spinBox_vpos.editingFinished.connect(self.spinBox_vpos_value_changed)
        self.comboBox_size_preset.currentIndexChanged.connect(self.comboBox_size_preset_value_changed)
        self.pb_center_FOV.clicked.connect(self.pb_center_FOV_clicked)
        self.comboBox_binning.currentIndexChanged.connect(self.comboBox_binning_value_changed)
        
            ## Timelaps settings
        self.spinBox_timepoints.editingFinished.connect(self.spinBox_timepoints_value_changed)
        self.spinBox_time_interval.editingFinished.connect(self.spinBox_time_interval_value_changed)
        self.timeEdit_total_duration.editingFinished.connect(self.timeEdit_total_duration_value_changed)
        
            ## Scanner
        self.spinBox_scanner_position.valueChanged.connect(self.spinBox_scanner_position_value_changed)
        self.pb_scanner_center.clicked.connect(self.pb_scanner_center_clicked_connect)
        self.spinBox_scan_range.valueChanged.connect(self.spinBox_scan_range_value_changed)
        
            ## Channels settings
                ### Channel
        self.comboBox_channel_name.currentIndexChanged.connect(self.comboBox_channel_name_update)
        self.pb_channel_save.clicked.connect(self.pb_channel_save_clicked_connect)
        self.pb_channel_add.clicked.connect(self.pb_channel_add_clicked_connect)
        self.pb_channel_remove.clicked.connect(self.pb_channel_remove_clicked_connect)

                ### laser check boxes ans spin boxes
        self.checkBox_laser_405.stateChanged.connect(self.checkBox_laser_changed)
        self.checkBox_laser_488.stateChanged.connect(self.checkBox_laser_changed)
        self.checkBox_laser_561.stateChanged.connect(self.checkBox_laser_changed)
        self.checkBox_laser_640.stateChanged.connect(self.checkBox_laser_changed)
        
        self.spinBox_laser_405.valueChanged.connect(self.spinBox_laser_value_changed)
        self.spinBox_laser_488.valueChanged.connect(self.spinBox_laser_value_changed)
        self.spinBox_laser_561.valueChanged.connect(self.spinBox_laser_value_changed)
        self.spinBox_laser_640.valueChanged.connect(self.spinBox_laser_value_changed)
                
                ### Other parameters
        self.spinBox_channel_exposure_time.editingFinished.connect(self.spinBox_channel_exposure_time_value_changed)
        self.comboBox_channel_filter.currentIndexChanged.connect(self.comboBox_channel_filter_update)
        
            ## Channel selection and orders
            
        self.spinBox_number_channels.valueChanged.connect(self.spinBox_number_channels_value_changed)

            ## Preview
        self.checkBox_show_saturation.stateChanged.connect(self.checkBox_show_saturation_value_changed)
        self.spinBox_min_grayscale.valueChanged.connect(self.spinBox_grayscale_value_changed)
        self.spinBox_max_grayscale.valueChanged.connect(self.spinBox_grayscale_value_changed)
        self.pb_auto_grayscale.clicked.connect(self.pb_auto_grayscale_clicked_connect)
        self.pb_reset_grayscale.clicked.connect(self.pb_reset_grayscale_clicked_connect)
        self.pb_preview.clicked.connect(self.pb_preview_clicked)
        self.pb_pause_preview.clicked.connect(self.pb_pause_preview_clicked)
        self.pb_stop_preview.clicked.connect(self.pb_stop_preview_clicked)
        self.comboBox_preview_zoom.currentIndexChanged.connect(self.comboBox_preview_zoom_value_changed)
        self.pb_snap.clicked.connect(self.pb_snap_clicked_connect)
        
            ## For the preview - Timer pour l'affichage des images
            
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self.update_preview)
        
        self.timer_gray_hystogram = QTimer()
        self.timer_gray_hystogram.timeout.connect(self.update_gray_histogram)
        
            ## Acquisition
        self.pb_snoutscope_acquisition.clicked.connect(self.pb_snoutscope_acquisition_clicked_connect)
        self.pb_multidimensional_acquisition.clicked.connect(self.pb_multidimensional_acquisition_clicked_connect)
        
        ###############################################
        ## Fonctions appelées par les menus d'action ##
        ###############################################
        
        self.action_channel_editor.triggered.connect(self.openChannelEditor)
        
    def closeEvent(self, event):
        # Show a dialog box asking the user to close the interface
        result = QtWidgets.QMessageBox.question(self,
                                                "Confirm Exit...",
                                                "Do you want to exit ?",
                                                (QtWidgets.QMessageBox.Yes |
                                                 QtWidgets.QMessageBox.No))
        if result == QtWidgets.QMessageBox.Yes:
            # permet d'ajouter du code pour fermer proprement
            if self.is_preview:
                self.pb_stop_preview_clicked()
            
            event.accept()
        else:
            event.ignore()
        
    #####################################
    ## Functions called by the buttons ##
    #####################################
    
        ## Saving
        
    def pb_data_path_value_changed(self):
        """
        Opens a dialog to select a directory and updates the pb_data_path field.
        """
        self.DATA_PATH = QFileDialog.getExistingDirectory(self, "Select Data Directory")
        
        if self.DATA_PATH:  # Si un dossier a été sélectionné
            self.label_data_path.setText(self.DATA_PATH)
        
    def lineEdit_exp_name_modified(self):
        """Ensures the experiment name is correctly formatted """
        exp_name = self.lineEdit_exp_name.text().strip()

        if not exp_name:
            self.status_bar.showMessage("Experiment name cannot be empty!", 5000)
            self.lineEdit_exp_name.setText(self.EXP_NAME)
            return
            
        name_ok, self.EXP_NAME = functions_ui.legalize_name(exp_name)
        
        if name_ok :
            self.status_bar.showMessage(f"Experiment name set to: {exp_name}", 2000)
        else:
            self.status_bar.showMessage("Invalid experiment name! Avoid spaces and special characters.", 5000)
            self.lineEdit_exp_name.setText(self.EXP_NAME)
        
    def comboBox_setup_value_changed(self):
        """
        Handle changes in the setup selection and update the interface accordingly.
    
        This function is triggered when the value of `comboBox_setup` changes.
        It updates the `setup` variable, adjusts the available camera options in 
        `comboBox_camera`, and enables or disables channels in `comboBox_channel` 
        based on the selected setup.
    
        The available setups are:
        - "Thibault": Enables all channel selections, disables disable laser chackBoxes and provides "Camera 1".
        - "Armin": Disables all channel selections and provides "Camera 1" and "Camera 2".
    
        The function also temporarily blocks signals from `comboBox_camera` while updating its items 
        to prevent unwanted signal emissions.
        """
        curent_value = self.comboBox_setup.currentText()
        if curent_value == "Thibault":
            self.setup = "Thibault"
            camera_list = ["Camera 1"]
            cam_list = ["Cam 1"]
            
            'active / desactive les fonctions inutiles'
            for combo in self.comboBox_channel.values():
                combo.setDisabled(False)  
                
            for combo in self.comboBox_camera_list.values():
                combo.setDisabled(True)
                
            self.comboBox_camera.setDisabled(True)
            
        if curent_value == "Armin":
            self.setup = "Armin"
            camera_list = ["Camera 1","Camera 2"]
            cam_list = ["Cam 1", "Cam2"]
            
            'active / desacive les fonctions inutiles' #J'ai mis deux boucles pour plus de lisibilité
            for combo in self.comboBox_channel.values():
                combo.setDisabled(True)
                
            for combo in self.comboBox_camera_list.values():
                combo.setDisabled(False)
                
            self.comboBox_camera.setDisabled(False)
                
        'Gére les options des différentes comboBox'    
               
        functions_ui.set_comboBox(self.comboBox_camera,camera_list)
        
        for combo in self.comboBox_camera_list.values():
            functions_ui.set_comboBox(combo, cam_list)

        ## Camera
        
        """
    These functions update the selected camera's region of interest (ROI) parameters 
    based on user input from spin boxes.
    
    Each function retrieves the currently selected camera from `comboBox_camera` and updates 
    one of its four parameters accordingly:
    - `hsize`: Horizontal size of the ROI (`spinBox_hsize`).
    - `hpos`: Horizontal position of the ROI (`spinBox_hpos`).
    - `vsize`: Vertical size of the ROI (`spinBox_vsize`).
    - `vpos`: Vertical position of the ROI (`spinBox_vpos`).
    - 'binning' : Binning of the camera ('spinBox_binning')
    
    The updated values are stored in the `camera` dictionary, indexed by the camera's 
    current selection in `comboBox_camera`.
    """
    
    def spinBox_hsize_value_changed(self):
        'Horizontal size of the ROI'
        camera_id = self.comboBox_camera.currentIndex()
        
        # set hsize
        size = functions_ui.set_size(self.spinBox_hsize.value(),
                                     self.camera[camera_id].hchipsize)
        
        self.spinBox_hsize.setValue(size)
        
        self.camera[camera_id].hsize = size
        
        #set hpos
        self.spinBox_hpos_value_changed()
        
    def spinBox_hpos_value_changed(self):
        'Horizontal position of the ROI'
        camera_id = self.comboBox_camera.currentIndex()
        
        pos = self.spinBox_hpos.value()
        pos = functions_ui.set_pos(pos, self.camera[camera_id].hsize, self.camera[camera_id].hchipsize)

        self.spinBox_hpos.setValue(pos)
        
        self.camera[camera_id].hpos = pos
        
    def spinBox_vsize_value_changed(self):
        'Vertical size of the ROI'
        camera_id = self.comboBox_camera.currentIndex()
        
        # set vsize
        size = functions_ui.set_size(self.spinBox_vsize.value(),
                                     self.camera[camera_id].vchipsize)
        
        self.spinBox_vsize.setValue(size)
        
        self.camera[camera_id].vsize = size
        
        #set vpos
        self.spinBox_vpos_value_changed()
        
    def spinBox_vpos_value_changed(self):
        'Vertical position of the ROI'
        camera_id = self.comboBox_camera.currentIndex()
        
        pos = self.spinBox_vpos.value()
        pos = functions_ui.set_pos(pos, self.camera[camera_id].vsize, self.camera[camera_id].vchipsize)

        self.spinBox_vpos.setValue(pos)
        
        self.camera[camera_id].vpos = pos
        
    def pb_center_FOV_clicked(self):
        'Center the position of the ROI on the camera chip'
        
        self.spinBox_hpos.setValue(
            (self.camera[self.camera_id].hchipsize - self.spinBox_hsize.value())/2)
        
        self.spinBox_vpos.setValue(
            (self.camera[self.camera_id].vchipsize - self.spinBox_vsize.value())/2)
        
    def comboBox_size_preset_value_changed(self):
        'set hpos and vpos to preset values'
        try:
            size = self.comboBox_size_preset.currentText()
            hsize, _ , vsize = size.split()
            
            self.spinBox_hsize.setValue(int(hsize))
            self.spinBox_vsize.setValue(int(vsize))
            
            self.spinBox_hsize_value_changed()
            self.spinBox_vsize_value_changed()
        except:
            pass
        
    def comboBox_binning_value_changed(self):
        'Binning of the camera'
        camera_id = self.comboBox_camera.currentIndex()
        binning = int(self.comboBox_binning.currentText())

        self.camera[camera_id].binning = binning
        
        ## Scanner
        
    def spinBox_scanner_position_value_changed(self):
        self.scanner_position = self.spinBox_scanner_position.value()
        
    def pb_scanner_center_clicked_connect(self):
        self.scanner_position = 0
        self.spinBox_scanner_position.setValue(0)
        
    def spinBox_scan_range_value_changed(self):
        self.scan_range = self.spinBox_scan_range.value()
    
        ## Timelaps settings
    """
    These functions handle user input changes in the spin boxes and time editor related to time-lapse acquisition settings. 
    
    They ensure that the variables `timepoints` and `time_intervals` are updated accordingly when modifying:
    - `spinBox_timepoints`: The number of time points in the acquisition.
    - `spinBox_time_intervals`: The time interval between consecutive time points.
    - `timeEdit_total_duration`: The total duration of the acquisition.
    """
    
    def spinBox_timepoints_value_changed(self):
        self.timepoints = self.spinBox_timepoints.value()
        self.total_duration = self.timepoints * self.time_intervals
        self.timeEdit_total_duration.setTime(functions_ui.seconds_to_QTime(self.total_duration))
        
    def spinBox_time_interval_value_changed(self):
        self.time_intervals = self.spinBox_time_interval.value()
        self.total_duration = self.timepoints * self.time_intervals
        self.timeEdit_total_duration.setTime(functions_ui.seconds_to_QTime(self.total_duration))
        
    def timeEdit_total_duration_value_changed(self):
        self.total_duration = functions_ui.QTime_to_seconds(self.timeEdit_total_duration.time())
        self.time_intervals = self.total_duration / self.timepoints
        self.spinBox_time_interval.setValue(self.time_intervals)
    
        ## Channels settings
        
            ### channel creation and save
    def comboBox_channel_name_set_indexes(self):
        self.comboBox_channel_name.clear()
        self.comboBox_channel_name.addItems(list(self.channel.keys()))
        self.comboBox_channel_name_update()
    
    def comboBox_channel_name_update(self):
        "Configures the interface elements when changing the comboBox_channel from selected channel object."
        functions_ui.channel_set_interface(self.list_channel_interface,
                                           self.channel[self.comboBox_channel_name.currentText()])
        
        self.preview_channel = self.comboBox_channel_name.currentText() # Change the current name of the channel used for preview
    
    def pb_channel_add_clicked_connect(self):
        "Saves the settings from the interface elements into a new channel object named from channel_name lineEdit object."
        index = self.lineEdit_channel_name.text() # get name of the new channel
        
        if not index:
             self.status_bar.showMessage("channel name cannot be empty!", 5000)
             return
        
        name_ok, index = functions_ui.legalize_name(index)
        
        if name_ok == False : self.status_bar.showMessage("Invalid experiment name! Avoid spaces and special characters.", 5000)
        
        self.channel[index] = channel_config(index, self.lasers) #Create the new channel
        functions_ui.save_channel_from_interface(self.list_channel_interface,
                                                 self.channel[self.comboBox_channel_name.currentText()]) #save the channel parameters
        
        self.comboBox_channel_name.addItem(index) # Add the new channel to the comboBox
        self.comboBox_channel_name.setCurrentText(index) # set the comboBox to this index
        self.lineEdit_channel_name.setText(index)
 
    def pb_channel_remove_clicked_connect(self):
        "Removes the currently selected channel from the combo box and the channel dictionary."
        channel_id = self.comboBox_channel_name.currentText()
        index = self.comboBox_channel_name.currentIndex()
        
        if channel_id not in self.channel_names:
            if index >= 0:
                self.comboBox_channel_name.removeItem(index)
                self.channel.pop(channel_id, None) # channel.pop remove the channel from the channel dictionnaire
                
        else:
            self.status_bar.showMessage("Default channel can not be removed", 5000)

    def pb_channel_save_clicked_connect(self):
        "Saves the settings from the interface elements into the specified channel object."
        functions_ui.save_channel_from_interface(self.list_channel_interface,
                                                 self.channel[self.comboBox_channel_name.currentText()])
    
    def checkBox_laser_changed(self):
        pass

    def spinBox_laser_value_changed(self):
        pass
        
    def spinBox_channel_exposure_time_value_changed(self):
        pass
    
    def comboBox_channel_filter_update(self):
        pass
    
    def spinBox_number_channels_value_changed(self):
        """
        Updates the number of QComboBoxes based on the value of spinBox_number_channels.
        Preserves the current selections of existing QComboBoxes when adding or removing them.
        """
        # Save current selection
        current_selections = [comboBox.currentText() for comboBox in self.comboBoxes_channel_order]
        
        for comboBox in self.comboBoxes_channel_order:
            self.verticalLayout_2.removeWidget(comboBox)
            comboBox.deleteLater()
            
        # Clear the list of QComboBoxes
        self.comboBoxes_channel_order.clear()
        
        # Add the appropriate number of QComboBoxes
        for i in range(self.spinBox_number_channels.value()):
            comboBox = QComboBox()
            comboBox.addItems(['None'] + list(self.channel.keys())) # Choix parmis les canneaux proposés
            self.verticalLayout_2.addWidget(comboBox)
            self.comboBoxes_channel_order.append(comboBox)  # Ajouter à la liste
            
            # Connecter le signal pour mettre à jour active_channels
            comboBox.currentIndexChanged.connect(self.updateActiveChannels)
            
            # Restore selection if available
            if i < len(current_selections):
                index = comboBox.findText(current_selections[i])
                if index >= 0:
                    comboBox.setCurrentIndex(index)
                    
        self.updateActiveChannels()
        
    def updateActiveChannels(self):
        self.active_channels = [comboBox.currentText() for comboBox in self.comboBoxes_channel_order]

        ## Preview
        
            ### Changement min / max grayscales
    
    def checkBox_show_saturation_value_changed(self):
      
        if self.checkBox_show_saturation.isChecked():
            self.look_up_table = 'show_saturation'
        else:
            self.look_up_table = 'grayscale'
    
    def spinBox_grayscale_value_changed(self):
        """
        Updates the grayscale min and max values used for image display, ensuring 
        that min_grayscale is always less than max_grayscale. Also updates the 
        coefficient for grayscale conversion and refreshes the UI elements accordingly.
        """
        
        # Retrieve the current values from the spin boxes
        self.min_grayscale = self.spinBox_min_grayscale.value()
        self.max_grayscale = self.spinBox_max_grayscale.value()
        
        # Ensure that min_grayscale is always strictly less than max_grayscale
        if self.min_grayscale >= self.max_grayscale:
            self.min_grayscale = self.max_grayscale - 1 # Adjust min_grayscale
            
            # Update the spin box value while blocking signals to avoid infinite loops
            self.spinBox_min_grayscale.blockSignals(True)
            self.spinBox_min_grayscale.setValue(self.min_grayscale)
            self.spinBox_min_grayscale.blockSignals(False)
            
            # Update the slider value similarly
            self.slider_min_grayscale.blockSignals(True)
            self.slider_min_grayscale.setValue(self.min_grayscale)
            self.slider_min_grayscale.blockSignals(False)
        
    def pb_auto_grayscale_clicked_connect(self):
        """"
        Sets the grayscale min and max values based on the current preview frame,
        or assigns default values if no frame is available.
        """
        if self.preview_frame is not None:
            frame = self.preview_frame
            self.spinBox_min_grayscale.setValue(np.min(frame))
            self.spinBox_max_grayscale.setValue(np.max(frame))
        else:
            pass
        
    def pb_reset_grayscale_clicked_connect(self):
        "Resets the grayscale range to the full 16-bit scale (0 to 65535)."
        self.spinBox_max_grayscale.setValue(65535)
        self.spinBox_min_grayscale.setValue(0)
            
    def comboBox_preview_zoom_value_changed(self):
        self.preview_zoom = [0.25 , 2 , 1 , 0.5 , 1/3 , 0.25][self.comboBox_preview_zoom.currentIndex()]
            
    def pb_snap_clicked_connect(self):
        """
        Saves the currently displayed frame as a .tiff file for later use.
        
        The user is prompted to select a save location, and the NumPy array 
        is stored in a compressed format.
        """
        
        if self.preview_frame is None:
            self.status_bar.showMessage("No frame available to save.")
            return
    
        # Création du chemin complet
        
        file_path = os.path.join(self.DATA_PATH, f"{self.EXP_NAME}.tiff")
                
        try:
            tifffile.imwrite(file_path, self.preview_frame)
            self.status_bar.showMessage(f"Frame saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save frame:\n{str(e)}")
   
    def pb_preview_clicked(self):
        """
        Starts or resumes the video preview when the "Preview" button is clicked.
        
        - If the preview is not active, initializes the camera and starts acquisition.
        - Retrieves necessary parameters such as exposure time and camera settings.
        - Creates a thread for image acquisition and connects it to the frame processing function.
        - Sets camera properties including exposure time and subarray parameters.
        - Starts the camera acquisition and updates the preview every 30 ms.
        - If the preview was paused, resumes it.
        """
        # TODO: Passer cette partie la du code dans un fichier "Communication Hardware"
        # TODO: Add laser activation
        
        if not self.is_preview: # If preview is not already running
            
            self.status_bar.showMessage("Displaying Preview")
            
            self.is_preview = True
            
            # Disable different parameters modifications while preview is running
            self.preview_tools_desactivation()
            
            # Get the currently selected camera index
            self.camera_id = self.comboBox_camera.currentIndex()
            
            # Retrieve the exposure time from the corresponding spinBox, default to 10ms if not availables
            # TODO: récupérer le exposure time du channel
            self.camera[self.camera_id].exposure_time = 0.01
            
            # Initialize the camera object
            self.hcam = HamamatsuCamera()
            
            # Create and configure the acquisition thread
            self.camera_thread = CameraThread(self.hcam, self.camera_id)
            self.camera_thread.new_frame.connect(self.store_frame) # Get the frame from camera thread process
            
            # Set camera acquisition mode and parameters
            functions_camera.configure_camera_for_preview(self.hcam, self.camera[self.camera_id])
            
            # Start the camera acquisition
            self.hcam.startAcquisition(self.camera_id)
            
            # Start the acquisition thread to handle continuous frame capture
            self.camera_thread.start()
            
            # Start a timer to update the preview display and gray hystogram every 30 ms
            self.preview_timer.start(30)
            self.timer_gray_hystogram.start(30)
            
        # If preview was paused, resume it
        if self.is_preview_paused:
            self.pb_pause_preview_clicked()

    def pb_pause_preview_clicked(self):
        """Fige l'image actuelle sans arrêter la capture losque l'on clique sur le bouton pause
        La pause sera appliquée lorsque l'image est récupérée dans la fonction store_frame """
        if self.is_preview_paused:
            self.is_preview_paused = False
            self.status_bar.showMessage("Displaying Preview")
            # TODO: Rallumera le laser ici
            
        else:
            self.is_preview_paused = True
            self.status_bar.showMessage("Displaying Preview Paused")
            # TODO: Eteindra le laser ici
            
    def pb_stop_preview_clicked(self):
        """Arrête l'acquisition et l'affichage et ferme proprement les processus."""
        # TODO: éteindre les lasers
        self.is_preview = False
        self.preview_tools_desactivation()
        
        # Stop preview
        self.preview_timer.stop()
        self.camera_thread.stop()
        self.camera_thread.wait()
        self.hcam.stopAcquisition(self.camera_id)
        self.hcam.closeCamera(self.camera_id)
        
        # Stop displaying hystograms
        self.timer_gray_hystogram.stop()
        self.histogram_greyvalue_thread.stop()
        self.histogram_greyvalue_thread.wait()
        
        # Clear interface
        self.status_bar.showMessage("Ready")
            
    def update_preview(self):
        """Show the most recent image."""
        if self.is_preview and self.preview_frame is not None :
                        
            qt_image = functions_ui.create_preview(self.preview_frame,
                                                   self.look_up_table,
                                                   self.min_grayscale,
                                                   self.max_grayscale,
                                                   self.preview_zoom)
            
            self.label_image_preview.setPixmap(QPixmap.fromImage(qt_image))
            
        elif self.preview_frame is None :
            self.label_image_preview.setText("No image!")

    def update_gray_histogram(self):
        if not self.histogram_greyvalue_thread or not self.histogram_greyvalue_thread.isRunning() :
            self.generate_histogram()
        
    def generate_histogram(self):
        if self.preview_frame is not None:
            size = self.label_histogram_greyvalue.size()
            w , h = size.width() , size.height()
            self.histogram_greyvalue_thread = HistogramThread(self.preview_frame,
                                                              self.min_grayscale,
                                                              self.max_grayscale,
                                                              w_px = w, h_px = h)
            self.histogram_greyvalue_thread.histogram_ready.connect(self.display_gray_histogram)
            self.histogram_greyvalue_thread.start()
        
    def display_gray_histogram(self, image_data, w, h):
        qimage = QImage(image_data, w, h, w * 4, QImage.Format_RGBA8888)
        self.label_histogram_greyvalue.setPixmap(QPixmap.fromImage(qimage))
            
        
    def store_frame(self, frame):
        """Function used to get the frame from camera thread process"""
        new_frame = frame
        #Update frame if preview is not in pause
        if not self.is_preview_paused :
            self.preview_frame = new_frame
        
    def preview_tools_desactivation(self):
        """activate and desactivate tools during preview"""
        if self.is_preview:
            active = True
        else:
            active = False
            
            # Camera
        self.spinBox_hpos.setDisabled(active)
        self.spinBox_hsize.setDisabled(active)
        self.spinBox_vsize.setDisabled(active)
        self.spinBox_vpos.setDisabled(active)
        self.comboBox_size_preset.setDisabled(active)
        self.pb_center_FOV.setDisabled(active)
        self.comboBox_binning.setDisabled(active)
        
            # Channels
                    
            #Preview

        ## Acquisition
        
    def pb_snoutscope_acquisition_clicked_connect(self):
        """Start acquisition with the Snoutscope protocole from Armin"""
        print("start Snoutscope acquisition")
        self.status_bar.showMessage("start Snoutscope acquisition")
        
    def pb_multidimensional_acquisition_clicked_connect(self):
        """Start acquisition with the Multi Dimentionnal Acquisition protocole from Thibault"""
        print("start multidimensional acquisition")      
        self.status_bar.showMessage("start multidimensional acquisition")
        
        ###############################################
        ## Fonctions appelées par les menus d'action ##
        ###############################################
        
    def openChannelEditor(self):
        self.channel_editor = ChannelEditorWindow(self.channel, self.channel_names, self)
        self.channel_editor.show()
        pass
    
    
if __name__ == '__main__':
    APP = QtWidgets.QApplication(sys.argv)
    FEN = GUI_Microscope()
    FEN.activateWindow()
    sys.exit(APP.exec())