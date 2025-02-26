# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:00:36 2025

@author: tbrugiere
"""

"""
Convert file.ui to file.py

pyside6-uic ui_Control_Microscope_Main.ui -o ui_Control_Microscope_Main.py

TODO :
    => Fonctions function_ui.label_volume_duration pour l'estimation du nombre de frames et durée de chaque volumes
    => Appeler le programme Snoutscope
    => Enregistrer camera / experiment / microscope
"""

import copy
import json
import numpy as np
import os
import pickle
import sys
import tifffile

from PySide6 import QtWidgets
from PySide6.QtCore import QTimer #, QCoreApplication, QEventLoop
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QFileDialog, QMessageBox, QComboBox

from Functions_UI import functions_ui, HistogramThread
from Functions_Hardware import CameraThread, functions_camera , functions_daq
from configs.config import camera, channel_config, microscope, experiment
# from hardware.hamamatsu import HamamatsuCamera
from mock.hamamatsu_DAQ import HamamatsuCamera
# from mock.hamamatsu_DAQ import functions_daq

from ui_Control_Microscope_Main import Ui_MainWindow

from widget.set_DAQ_Window import setDAQWindow
from widget.Set_Filters_Window import filtersEditionWindow

from widget.Channel_Editor_Window import ChannelEditorWindow
from widget.Preset_ROI_Window import PresetROIWindow

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
        
        self.load_variables() #Si des variables de l'interface ont étées enregistrées, elles seront changées ici
        self.load_channels()
        
        self.microscope = microscope() # Variable contenant les paramétres du microscope
        self.experiment = experiment() # Variable contenant l'expérience
        
        #
        # Saved datas
        #
        
        self.data_path = "D:/EqSibarita/Python/Control_Microscope_GUI/Images"
        self.experiment.exp_name = "Image"
        
        self.setup = "Thibault" #Permet de choisir entre le Setup de Thibault et celui d'Armin
        
        #
        # Creation of the cameras, set interface
        #
        
        self.camera = [camera(camera_id = 0 )] #, camera(camera_id = 1)] # Avant il y avait deux camera dans le soft
        
        self.camera_id = 0 # index de la caméra actuellement sélectionnée
        
        if self.loaded_variables:
            self.preset_size = self.saved_variables['preset_size']
        else:
            self.preset_size = ['44032 - 0 x 2368 - 0','2048 - 1192 x 2048 - 160']
        
        self.comboBox_size_preset_set_indexes()
        
        #
        # creation of the channels / lasers
        #
        
        self.lasers = ["405","488","561","640"] # = self.microscope.lasers
        
        if self.loaded_channels == False: #essaie de charger les cannaux, si cela n'est pas le cas, crée ceux par défault
        
            self.default_channel = {}

            self.channel_names = ['BFP','GFP','CY3.5','TexRed']
            
            for channel in self.channel_names:
                self.default_channel[channel] = channel_config(channel, self.lasers)
                
        self.channel = copy.deepcopy(self.default_channel)
        
            ### Library to set the channels
        
        self.checkBox_laser = {"405" : self.checkBox_laser_405,
                               "488" : self.checkBox_laser_488,
                               "561" : self.checkBox_laser_561,
                               "640" : self.checkBox_laser_640
                               } #Dictionnary of the laser checkboxes
        
        self.spinBox_laser_power = {"405" : self.spinBox_laser_405,
                                    "488" : self.spinBox_laser_488,
                                    "561" : self.spinBox_laser_561,
                                    "640" : self.spinBox_laser_640
                                    } # Dictionnary of the laser power spin boxes
        
        self.slider_laser_power = {"405" : self.slider_laser_405 ,
                                   "488" : self.slider_laser_488 ,
                                   "561" : self.slider_laser_561 ,
                                   "640" : self.slider_laser_640
                                   } # Dictionnary of the laser power spin boxes
        
        self.list_channel_interface = {"checkBox_laser" :      self.checkBox_laser,
                                       "spinBox_laser_power" :  self.spinBox_laser_power,
                                       "slider_laser_power" : self.slider_laser_power,
                                       "filter" :               self.comboBox_channel_filter,
                                       "camera" :               self.comboBox_channel_camera,
                                       "exposure_time" :        self.spinBox_channel_exposure_time
                                       } # Dictionnary used to set all the interface elements for a given channel
        
        self.comboBoxes_channel_order = [] # Liste des combo boxes permettant de sélectionner les cannaux actifs
        self.active_channels = [] #contiendra la liste et l'ordre des cannaux activés
        
        self.laser_emission = False # si le laser est actuellement emmis
        
            ### desable laser settings if not connected to DAQ
            
        self.sync_laser_interface() # Empèche la modification et l'allumage des lasers inutilisables
        
        self.comboBox_channel_name_set_indexes() #Ajoute tous les cannaux dans la comboBox_channel_name
        
        self.sync_filter_interface() # Modifie les channels et l'interface selon les filtres disponibles

        #
        # Preview
        #
        self.min_grayscale = 0 #Valeur de gris la plus basse du preview
        self.max_grayscale = 65535 #valeur de gris la plus haute du preview
        self.preview_zoom = 0.25 #rescale factor of the preview ()
        self.look_up_table = 'grayscale'
        
        self.is_preview = False # Si une image est affichée dans le preview
        self.is_preview_paused = False # Si le preview est en pause
        self.preview_frame = None # Image actuellement affichée
        self.preview_camera = 0 # Camera utilisée dans le preview
        self.preview_channel = self.channel[self.comboBox_channel_name.currentText()] # Canal affiché dans le préview (laser et filtre)
        
        self.histogram_greyvalue_thread = None # Thread utilisé pour créer le graphique des niveaux de gris
        

            ## For the preview - Timer pour l'affichage des images
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self.update_preview)
        
        self.timer_gray_hystogram = QTimer()
        self.timer_gray_hystogram.timeout.connect(self.update_gray_histogram)
        
        #
        # Petites choses de l'interface
        #
        
        self.label_fov_size_set_text()
        
        self.Red_Light_Icon_On = QPixmap('Icons/Red_Light_Icon_On.png')
        self.Red_Light_Icon_Off = QPixmap('Icons/Red_Light_Icon_Off.png')
        
        self.label_laser_icon.setPixmap(self.Red_Light_Icon_Off)
        
        self.spinBox_aspect_ratio.setValue(self.experiment.aspect_ratio)
        
        #########################################
        ## Fonctions appelées pour les boutons ##
        #########################################
        
            ## Saving / Setup
        self.pb_data_path.clicked.connect(self.pb_data_path_value_changed)
        self.lineEdit_exp_name.editingFinished.connect(self.lineEdit_exp_name_modified)
        self.comboBox_setup.currentIndexChanged.connect(self.comboBox_setup_index_changed)
        
            ## Camera 
        self.comboBox_camera.currentIndexChanged.connect(self.comboBox_camera_index_changed)
        self.spinBox_hsize.editingFinished.connect(self.spinBox_hsize_value_changed)
        self.spinBox_hpos.editingFinished.connect(self.spinBox_hpos_value_changed)
        self.spinBox_vsize.editingFinished.connect(self.spinBox_vsize_value_changed)
        self.spinBox_vpos.editingFinished.connect(self.spinBox_vpos_value_changed)
        self.comboBox_size_preset.currentIndexChanged.connect(self.comboBox_size_preset_index_changed)
        self.pb_center_FOV.clicked.connect(self.pb_center_FOV_clicked)
        self.comboBox_binning.currentIndexChanged.connect(self.comboBox_binning_index_changed)
        
            ## Timelaps settings
        self.spinBox_timepoints.editingFinished.connect(self.spinBox_timepoints_value_changed)
        self.spinBox_time_interval.editingFinished.connect(self.spinBox_time_interval_value_changed)
        self.timeEdit_total_duration.editingFinished.connect(self.timeEdit_total_duration_value_changed)
        
            ## Scanner
        self.spinBox_scanner_position.valueChanged.connect(self.spinBox_scanner_position_value_changed)
        self.pb_scanner_center.clicked.connect(self.pb_scanner_center_clicked_connect)
        self.spinBox_scan_range.valueChanged.connect(self.spinBox_scan_range_value_changed)
        self.spinBox_aspect_ratio.valueChanged.connect(self.spinBox_aspect_ratio_value_changed)
        self.spinBox_slit_aperture.valueChanged.connect(self.spinBox_slit_aperture_value_changed)
        
            ## Channels settings
                ### Channel
        self.comboBox_channel_name.currentIndexChanged.connect(self.comboBox_channel_name_index_changed)
        self.pb_channel_save.clicked.connect(self.pb_channel_save_clicked_connect)
        self.pb_channel_add.clicked.connect(self.pb_channel_add_clicked_connect)
        self.pb_channel_remove.clicked.connect(self.pb_channel_remove_clicked_connect)

                ### laser check boxes ans spin boxes
        self.checkBox_laser_405.stateChanged.connect(self.state_laser_405_changed)
        self.checkBox_laser_488.stateChanged.connect(self.state_laser_488_changed)
        self.checkBox_laser_561.stateChanged.connect(self.state_laser_561_changed)
        self.checkBox_laser_640.stateChanged.connect(self.state_laser_640_changed)

        self.spinBox_laser_405.valueChanged.connect(self.state_laser_405_changed)
        self.spinBox_laser_488.valueChanged.connect(self.state_laser_488_changed)
        self.spinBox_laser_561.valueChanged.connect(self.state_laser_561_changed)
        self.spinBox_laser_640.valueChanged.connect(self.state_laser_640_changed)
                
                ### Exposure time / filter / turn on laser
        self.spinBox_channel_exposure_time.editingFinished.connect(self.spinBox_channel_exposure_time_value_changed)
        self.comboBox_channel_filter.currentIndexChanged.connect(self.comboBox_channel_filter_index_changed)
        self.pb_laser_emission.clicked.connect(self.pb_laser_emission_clicked)
        
                ### Channel selection and orders
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
        self.comboBox_preview_zoom.currentIndexChanged.connect(self.comboBox_preview_zoom_index_changed)
        self.pb_snap.clicked.connect(self.pb_snap_clicked_connect)
        
            ## Acquisition
        self.pb_snoutscope_acquisition.clicked.connect(self.pb_snoutscope_acquisition_clicked_connect)
        self.pb_multidimensional_acquisition.clicked.connect(self.pb_multidimensional_acquisition_clicked_connect)
        
    ###############################################
    ## Fonctions appelées par les menus d'action ##
    ###############################################
    
            ## Fichier
        self.action_SaveConfig.triggered.connect(self.save_config)
        
            ## Config
        self.action_DAQ.triggered.connect(self.openDAQEditor)
        self.action_Filters.triggered.connect(self.openFiltersEditor)
        
            # Align
        self.action_Align_O2_O3.triggered.connect(self.openAlign_O2_O3) #Action pas encore définie
        
            # Parameters
        self.action_channel_editor.triggered.connect(self.openChannelEditor)
        self.action_Preset_ROI_size.triggered.connect(self.openPreserROIEditor)
        
        
    #########################################################
    ## Fonctions appelées lors de la fermture du programme ##
    #########################################################
        
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
                # Eteint l'acquisition si nécessaire
                self.pb_stop_preview_clicked()
                # Eteint les lasers si nécessaire
                self.pb_laser_emission.setChecked(False)
                self.pb_laser_emission_clicked()
            event.accept()
        else:
            event.ignore()
        
    #####################################
    ## Functions called by the buttons ##
    #####################################
    
        #
        # Saving
        #
        
    def pb_data_path_value_changed(self):
        """
        Opens a dialog to select a directory and updates the pb_data_path field.
        """
        self.data_path = QFileDialog.getExistingDirectory(self, "Select Data Directory")
        
        if self.data_path:  # Si un dossier a été sélectionné
            self.label_data_path.setText(self.data_path)
        
    def lineEdit_exp_name_modified(self):
        """Ensures the experiment name is correctly formatted """
        exp_name = self.lineEdit_exp_name.text().strip()

        if not exp_name:
            self.status_bar.showMessage("Experiment name cannot be empty!", 5000)
            self.lineEdit_exp_name.setText(self.exp_name)
            return
            
        name_ok, self.exp_name = functions_ui.legalize_name(exp_name)
        
        if name_ok :
            self.status_bar.showMessage(f"Experiment name set to: {exp_name}", 2000)
        else:
            self.status_bar.showMessage("Invalid experiment name! Avoid spaces and special characters.", 5000)
            self.lineEdit_exp_name.setText(self.exp_name)
        
    def comboBox_setup_index_changed(self):
        """ this function was supppose to Handle changes in the setup selection and update the interface accordingly"""
        pass

        #
        # Camera
        #
        
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
    def comboBox_camera_index_changed(self):
        self.camera_id = self.comboBox_camera.currentIndex()
    
    def spinBox_hsize_value_changed(self):
        'Horizontal size of the ROI'
        # set hsize
        size = functions_ui.set_size(self.spinBox_hsize.value(),
                                     self.camera[self.camera_id].hchipsize)
        
        self.spinBox_hsize.setValue(size)
        
        self.camera[self.camera_id].hsize = size
        
        #set hpos
        self.spinBox_hpos_value_changed()
        
    def spinBox_hpos_value_changed(self):
        'Horizontal position of the ROI'
        
        pos = self.spinBox_hpos.value()
        pos = functions_ui.set_pos(pos, self.camera[self.camera_id].hsize, self.camera[self.camera_id].hchipsize)

        self.spinBox_hpos.setValue(pos)
        
        self.camera[self.camera_id].hpos = pos
        
        self.label_fov_size_set_text()
        
    def spinBox_vsize_value_changed(self):
        'Vertical size of the ROI'
        
        # set vsize
        size = functions_ui.set_size(self.spinBox_vsize.value(),
                                     self.camera[self.camera_id].vchipsize)
        
        self.spinBox_vsize.setValue(size)
        
        self.camera[self.camera_id].vsize = size
        
        #set vpos
        self.spinBox_vpos_value_changed()
        
    def spinBox_vpos_value_changed(self):
        'Vertical position of the ROI'
        
        pos = self.spinBox_vpos.value()
        pos = functions_ui.set_pos(pos, self.camera[self.camera_id].vsize, self.camera[self.camera_id].vchipsize)

        self.spinBox_vpos.setValue(pos)
        
        self.camera[self.camera_id].vpos = pos
        
        self.label_fov_size_set_text()
        
    def pb_center_FOV_clicked(self):
        'Center the position of the ROI on the camera chip'
        
        self.spinBox_hpos.setValue(
            (self.camera[self.camera_id].hchipsize - self.spinBox_hsize.value())/2)
        
        self.spinBox_vpos.setValue(
            (self.camera[self.camera_id].vchipsize - self.spinBox_vsize.value())/2)
        
    def comboBox_size_preset_index_changed(self):
        'set hpos and vpos to preset values'
        try:
            size = self.comboBox_size_preset.currentText()
            hsize, _ ,hpos, _ , vsize, _ ,vpos = size.split()
            
            self.spinBox_hsize.setValue(int(hsize))
            self.spinBox_hpos.setValue(int(hpos))
            self.spinBox_vsize.setValue(int(vsize))
            self.spinBox_vpos.setValue(int(vpos))
            
            self.spinBox_hsize_value_changed()
            self.spinBox_hpos_value_changed()
            self.spinBox_vsize_value_changed()
            self.spinBox_vpos_value_changed()
        except:
            pass
        
    def comboBox_size_preset_set_indexes(self):
        'update comboBox_size_preset indexes after modification of preset sizes via specific window'
        text = self.comboBox_size_preset.currentText()
        self.comboBox_size_preset.clear()
        self.comboBox_size_preset.addItems(self.preset_size)
        
        try:
            self.comboBox_size_preset.setCurrentText(text)
        except:
            pass 
        
    def comboBox_binning_index_changed(self):
        'Binning of the camera'
        binning = int(self.comboBox_binning.currentText())

        self.camera[self.camera_id].binning = binning
        
    def label_fov_size_set_text(self):
        'show the size of the fild of view in µm depending on camera settings'
        sample_pixel_size = self.microscope.sample_pixel_size
        hum = self.camera[self.camera_id].hsize*sample_pixel_size # horizontal size in µm
        vum = self.camera[self.camera_id].vsize*sample_pixel_size # vertical size in µm
        
        message = 'Field of view : ' + str(round(hum, 2)) + ' x ' + str(round(vum, 2)) + ' µm'
        
        self.label_fov_size.setText(message)
        
        #
        # Timelaps settings
        #
        
        """
        These functions handle user input changes in the spin boxes and time editor related to time-lapse acquisition settings. 
        
        They ensure that the variables `timepoints` and `time_intervals` are updated accordingly when modifying:
        - `spinBox_timepoints`: The number of time points in the acquisition.
        - `spinBox_time_intervals`: The time interval between consecutive time points.
        - `timeEdit_total_duration`: The total duration of the acquisition.
        """
    
    def spinBox_timepoints_value_changed(self):
        self.experiment.timepoints = self.spinBox_timepoints.value()
        self.experiment.total_duration = self.experiment.timepoints * self.experiment.time_intervals
        self.timeEdit_total_duration.setTime(functions_ui.seconds_to_QTime(self.experiment.total_duration))
        
    def spinBox_time_interval_value_changed(self):
        self.experiment.time_intervals = self.spinBox_time_interval.value()
        self.experiment.total_duration = self.experiment.timepoints * self.experiment.time_intervals
        self.timeEdit_total_duration.setTime(functions_ui.seconds_to_QTime(self.experiment.total_duration))
        
    def timeEdit_total_duration_value_changed(self):
        self.experiment.total_duration = functions_ui.QTime_to_seconds(self.timeEdit_total_duration.time())
        self.experiment.time_intervals = self.experiment.total_duration / self.experiment.timepoints
        self.spinBox_time_interval.setValue(self.experiment.time_intervals)
        
        #
        # Scanner
        #
        
        """
        These functions update the scanning parameters based on user input from spin boxes.
        """
        
        
    def spinBox_scanner_position_value_changed(self):
        self.experiment.scanner_position = self.spinBox_scanner_position.value()
        
    def pb_scanner_center_clicked_connect(self):
        self.experiment.scanner_position = 0
        self.spinBox_scanner_position.setValue(0)
        
    def spinBox_scan_range_value_changed(self):
        self.experiment.scan_range = self.spinBox_scan_range.value()
        print(self.spinBox_scan_range.value())
        print(self.microscope.sample_pixel_size)
        print(self.spinBox_aspect_ratio.value())
        print(self.microscope.tilt_angle)
        print(self.preview_channel.exposure_time)
        self.label_volume_duration.setText(functions_ui.label_volume_duration(self.spinBox_scan_range.value(),
                                                                              self.microscope.sample_pixel_size,
                                                                              self.spinBox_aspect_ratio.value(),
                                                                              self.microscope.tilt_angle,
                                                                              self.preview_channel.exposure_time))
        
    def spinBox_aspect_ratio_value_changed(self):
        self.experiment.aspect_ratio = self.spinBox_aspect_ratio.value()
    
    def spinBox_slit_aperture_value_changed(self):
        self.experiment.slit_aperture = self.spinBox_slit_aperture.value
    
        #
        # Channels settings
        #
        
            ### Enable / disable laser tool depending on DAC connection
    def sync_laser_interface(self):
        """
        Updates the laser interface and channels based on the connection status to the DAQ.
        
        This function iterates over each laser and checks its connection status
        to the DAQ (Data Acquisition) system. If a laser is not connected, the
        corresponding UI elements (checkbox and power spinbox) are disabled and
        reset. If a laser is connected, the UI elements are enabled, allowing
        the user to interact with them.
        
        This ensures that the user interface accurately reflects the current
        state of the laser connections, providing a seamless user experience.
        """
        
        for laser in self.checkBox_laser.keys():
            self.channel = copy.deepcopy(self.default_channel)
            if self.microscope.daq_channels[laser] is None :
                self.checkBox_laser[laser].setDisabled(True)
                self.checkBox_laser[laser].setChecked(False)
                self.spinBox_laser_power[laser].setDisabled(True)
                self.spinBox_laser_power[laser].setValue(0)
                self.slider_laser_power[laser].setDisabled(True)
                for channel in self.channel.keys():
                    self.channel[channel].laser_is_active[laser] = False
                    self.channel[channel].laser_power[laser] = 0 
            else:
                self.checkBox_laser[laser].setDisabled(False)
                self.spinBox_laser_power[laser].setDisabled(False)
                self.slider_laser_power[laser].setDisabled(False)

            ### channel creation and save
    def comboBox_channel_name_set_indexes(self):
        "set the options of the comboBox_channel_names depending on self.channel dictionnary options"
        self.comboBox_channel_name.blockSignals(True)
        self.comboBox_channel_name.clear()
        self.comboBox_channel_name.addItems(list(self.channel.keys()))
        self.comboBox_channel_name.blockSignals(False)
    
    def comboBox_channel_name_index_changed(self):
        "Configures the interface elements when changing the comboBox_channel from selected channel object."
        functions_ui.channel_set_interface(self.list_channel_interface,
                                           self.channel[self.comboBox_channel_name.currentText()])
        
        self.preview_channel = self.channel[self.comboBox_channel_name.currentText()] # Change the current name of the channel used for preview
        
    def pb_channel_save_clicked_connect(self):
        "Saves the settings from the interface elements into the specified channel object."
        functions_ui.save_channel_from_interface(self.list_channel_interface,
                                                 self.channel[self.comboBox_channel_name.currentText()])
    
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
            
            ### Functions called when changing the parameters of lasers
            "These functions are triggered when the corresponding laser spin-box or check-box is changed."
    def state_laser_405_changed(self):
        self.state_laser_changed('405')
            
    def state_laser_488_changed(self):
        self.state_laser_changed('488')
        
    def state_laser_561_changed(self):
        self.state_laser_changed('561')
        
    def state_laser_640_changed(self):
        self.state_laser_changed('640')

    def state_laser_changed(self, laser):
        "Updates the laser output signal via the DAQ if laser emission is active."
        if self.laser_emission:
            if self.microscope.daq_channels[laser] is not None:
                if self.checkBox_laser[laser].isChecked():
                        # Sets the analog output voltage based on the laser power percentage (scaled to 5V max).
                        functions_daq.analog_out(self.spinBox_laser_power[laser].value()*self.microscope.volts_per_laser_percent[laser],
                                                 self.microscope.daq_channels[laser])
                else:
                    # Turns off the laser by setting the output to 0V.
                    functions_daq.analog_out(0,self.microscope.daq_channels[laser])
        
    def pb_laser_emission_clicked(self):
        if self.pb_laser_emission.isChecked():
            self.label_laser_icon.setPixmap(self.Red_Light_Icon_On)
            self.label_laser.setText("ON ")
            self.laser_emission = True
            functions_daq.digital_out(True, self.microscope.daq_channels['laser_blanking'])
            for laser in self.lasers:
                self.state_laser_changed(laser)
        else:
            self.label_laser_icon.setPixmap(self.Red_Light_Icon_Off)
            self.label_laser.setText("OFF")
            self.laser_emission = False
            functions_daq.digital_out(False, self.microscope.daq_channels['laser_blanking'])
            for laser in self.checkBox_laser.keys():
                if self.microscope.daq_channels[laser] is not None:
                    functions_daq.analog_out(0,self.microscope.daq_channels[laser])
                    
    def sync_filter_interface(self):
        """
        Updates the interface and channels based on the avaliable filters
        """
        
        options = copy.deepcopy(self.microscope.filters)
        
        options.insert(0, '-None-')
        
        self.channel = copy.deepcopy(self.default_channel)
        
        self.comboBox_channel_filter.blockSignals(True) # Pas utile, peut-être plus tard ?
        self.comboBox_channel_filter.clear()
        self.comboBox_channel_filter.addItems(options)

        for channel in self.channel.keys():
            if self.channel[channel].filter not in options:
                self.channel[channel].filter = None
        
        self.comboBox_channel_filter.blockSignals(False)
        
        self.comboBox_channel_name_index_changed()
        
    def spinBox_channel_exposure_time_value_changed(self):
        pass
    
    def comboBox_channel_filter_index_changed(self):
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

        #
        # Preview
        #
        
            ### Changement min / max grayscales
    
    def checkBox_show_saturation_value_changed(self):
        """see Function_ui => show_saturation"""
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
            
    def comboBox_preview_zoom_index_changed(self):
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
        
        file_path = os.path.join(self.data_path, f"{self.exp_name}.tiff")
                
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
        
        if not self.is_preview: # If preview is not already running
            
            self.status_bar.showMessage("Displaying Preview")
            
            self.is_preview = True
            
            # Disable different parameters modifications while preview is running
            self.preview_tools_desactivation()
            
            # Retrieve the exposure time from the corresponding spinBox, default to 10ms if not availables
            self.camera[self.preview_channel.camera].exposure_time = self.preview_channel.exposure_time/1000
            
            # Initialize the camera object
            self.hcam = HamamatsuCamera()
            
            
            
            # Create and configure the acquisition thread
            self.camera_thread = CameraThread(self.hcam, self.preview_channel.camera)
            self.camera_thread.new_frame.connect(self.store_frame) # Get the frame from camera thread process
            
            # Set camera acquisition mode and parameters
            functions_camera.configure_camera_for_preview(self.hcam, self.camera[self.preview_channel.camera])
            
            # Start the camera acquisition and turn on laser
            self.hcam.startAcquisition(self.preview_channel.camera)
            self.pb_laser_emission.setChecked(True)
            self.pb_laser_emission_clicked()
            
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
            
        else:
            self.is_preview_paused = True
            self.status_bar.showMessage("Displaying Preview Paused")
        
        # Eteint ou allume les lasers
        self.pb_laser_emission.setChecked(not self.is_preview_paused)
        self.pb_laser_emission_clicked()
            
    def pb_stop_preview_clicked(self):
        """Arrête l'acquisition et l'affichage et ferme proprement les processus."""
        self.is_preview = False
        self.preview_tools_desactivation()
        
        # Stop preview
        self.preview_timer.stop()
        self.camera_thread.stop()
        self.camera_thread.wait()
        self.hcam.stopAcquisition(self.preview_channel.camera)
        self.hcam.closeCamera(self.preview_channel.camera)
        
        # Turn off lasers
        self.pb_laser_emission.setChecked(False)
        self.pb_laser_emission_clicked()
        
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
        "start the generation of a new histogram"
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
        self.comboBox_channel_name.setDisabled(active)
        self.pb_channel_add.setDisabled(active)
        self.pb_channel_remove.setDisabled(active)
            #Preview

        #
        # Acquisition
        #
        
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
    
    def save_config(self):
        "save cnfigurations of the microscope"
        reply = QMessageBox.question(
            self, 'Confirm changes',
            """"Are you sure you want to save changes?
            If ou press Yes, orriginal settings will be erased""",
            QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.save_channels()
            self.save_variables()
        elif reply == QMessageBox.No:
            pass
        
    def openDAQEditor(self):
        "display window to eddit DAC channels"
        self.DAQ_editor = setDAQWindow(self.microscope.daq_channels,self)
        self.DAQ_editor.show()
    
    def openFiltersEditor(self):
        self.filters_editor = filtersEditionWindow(self.microscope.filters,self)
        self.filters_editor.show()
        
    def openAlign_O2_O3(self):
        "display window to aligne O2 and O3 using the piezzo stage"
        pass
        
    def openPreserROIEditor(self):
        "display window to eddit preset ROI that can be used"
        self.presetROI_editor = PresetROIWindow(self.preset_size ,
                                                [self.camera[self.camera_id].hchipsize ,
                                                 self.camera[self.camera_id].vchipsize],
                                                self)
        self.presetROI_editor.show()
    
    def openChannelEditor(self):
        "display window to eddit default channels of the microscope"
        self.channel_editor = ChannelEditorWindow(self.default_channel, self.channel_names, self)
        self.channel_editor.show()
        pass
    
    ################################################################
    ## Fonctions appelées pour sauvegarder et changer l'interface ##
    ################################################################
    
    #
    # different simples varibles .json
    #
    
    def load_variables(self):
        self.loaded_variables = False
        config_dir = 'configs'
        file_path = os.path.join(config_dir, 'saved_variables.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.saved_variables = json.load(file)
                self.loaded_variables = True
    
    def save_variables(self):
        config_dir = 'configs'
        os.makedirs(config_dir, exist_ok=True)  # Crée le dossier s'il n'existe pas
        file_path = os.path.join(config_dir, 'saved_variables.json')
        
        saved_variables = {'preset_size' : self.preset_size}
        
        with open(file_path, 'w') as file:
            json.dump(saved_variables, file)
        
    #
    # Channels
    #
    
    def load_channels(self):
        config_dir = 'configs'
        file_path = os.path.join(config_dir, 'channels_data.pkl')
        
        self.loaded_channels = False # est-ce que le channel sera chargé ?
        
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                data = pickle.load(file)
                self.channel_names = data['channel_names']
                self.default_channel = data['channel']
                
            self.loaded_channels = True
            
        return self.loaded_channels
    
    def save_channels(self):
        config_dir = 'configs'
        os.makedirs(config_dir, exist_ok=True)  # Crée le dossier s'il n'existe pas
        file_path = os.path.join(config_dir, 'channels_data.pkl')
        
        channels_data = {'channel' : self.default_channel,
                         'channel_names' : self.channel_names
                         }
        
        with open(file_path, 'wb') as file:
            pickle.dump(channels_data, file)
        
###############################################################################

if __name__ == '__main__':
    APP = QtWidgets.QApplication(sys.argv)
    FEN = GUI_Microscope()
    FEN.activateWindow()
    sys.exit(APP.exec())