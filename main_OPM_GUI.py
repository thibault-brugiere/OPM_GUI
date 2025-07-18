# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:00:36 2025

@author: tbrugiere
"""

"""
Convert file.ui to file.py

pyside6-uic ui_Control_Microscope_Main.ui -o ui_Control_Microscope_Main.py

# TODO : Present preview size should be limited by camera parameters
# TODO : ouvrir laser_GUI depuis l'interface
# TODO : Widget pour modifier tous les paramétres du microscope
# TODO : faire un dictionnaire.json dans config pour toute la description du microscope
        Pour qu'elle soit enregistrée lors de l'acquisition

Resolved FTDI DLL issue by copying ftd2xx64.dll from Thorlabs software to C:\Windows\System32 and renaming it to ftd2xx.dll
"""

import copy
import json
import numpy as np
import os
import pickle
# from pylablib.devices import DCAM # A remplacer aussi dans hardware functions_camera
import sys
import tifffile

from PySide6 import QtWidgets
from PySide6.QtCore import QTimer #, QCoreApplication, QEventLoop
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QFileDialog, QMessageBox, QComboBox

from acquisition.send_to_acquisition import send_to_snoutscope_acquisition
from acquisition.send_to_acquisition import send_to_multidimensionnal_acquisition
from acquisition.z_stack import z_stack
from configs.config import channel_config, microscope, experiment #, camera
from display.histogram import HistogramThread
from Functions_UI import functions_ui
from hardware.functions_camera import CameraThread, functions_camera
# from hardware.functions_DAQ import functions_daq
from mock.hamamatsu import DCAM # A remplacer aussi dans hardware functions_camera
from mock.DAQ import functions_daq

from ui_Control_Microscope_Main import Ui_MainWindow

from widget.Alignement_O2_O3_Window import alignement_O2_O3_Window
from widget.Channel_Editor_Window import ChannelEditorWindow
from widget.Microscope_Settings_Window import microscope_settings_window
from widget.Preset_ROI_Window import PresetROIWindow
from widget.set_DAQ_Window import setDAQWindow
from widget.Set_Filters_Window import filtersEditionWindow

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
        
    ###############################
    ## Creation of the Variables ##
    ###############################
        
        self.load_variables() # Load default parameters from the interface if they have been saved
        self.load_channels() # Load defaults channels if they have been saved
        self.load_microscope_settings() # Load default microscopes settings if they have been saved
        
        if self.loaded_microscope_settings == False:
            self.microscope = microscope() # Load default microscopes settings
            
        self.experiment = experiment() # Create experiment object
        
        if self.loaded_variables:
            self.preset_size = self.saved_variables['preset_size'] #for self.comboBox_size_preset
            self.experiment.data_path = self.saved_variables['experiment_data_path']
            self.experiment.slit_aperture = self.saved_variables['slit_aperture']
        else:
            self.preset_size = ['4432 - 0 x 2368 - 0','2048 - 1192 x 2048 - 160']
            
        self.comboBox_size_preset_set_indexes() #set the indexes of self.comboBox_size_preset

        #
        # Initialize all the cameras
        #
        
        self.n_camera = DCAM.get_cameras_number()
        
        self.label_camera_detected.setText(f"Number of cameras detected: {self.n_camera}")
        
        self.hcam , self.camera = functions_camera.initialize_cameras(self.n_camera, self.microscope.mag_total)
        
        if self.n_camera > 1: # Initialize the interface depending on the number of camera connected
            functions_ui.set_comboBox(self.comboBox_camera,
                                      functions_ui.generate_camera_indexes(self.n_camera))
            functions_ui.set_comboBox(self.comboBox_channel_camera,
                                     functions_ui.generate_camera_indexes(self.n_camera))
            self.comboBox_camera.setDisabled(False)
            self.comboBox_channel_camera.setDisabled(False)
            
            self.spinBox_hsize.setValue(self.camera[0].hsize)
            self.spinBox_vsize.setValue(self.camera[0].vsize)
            
        elif self.n_camera == 0:
            self.desactivate_camera_options(True)
        
        self.camera_id = 0 # set selected camera

        #
        # Check the DAQ connection
        #

        self.connected_daq = functions_daq.get_connected_daq_devices()

        if len(self.connected_daq) > 0 :
            self.label_daq_detected.setText(f'{len(self.connected_daq)} ni-DAQ detected : {self.connected_daq[0]}')
        else :
            self.label_daq_detected.setText('WARNING: No ni-DAQ detected ! Please restart the interface.')
        
        #
        # creation of the channels / lasers
        #
        
        self.lasers = ["405","488","561","640"] # = self.microscope.lasers, can not be modified
        
        if self.loaded_channels == False: # If channels haven't been loaded, create default channels
        
            self.default_channel = {} # These are defaults channels that can only be modified via self.action_channel_editor

            self.channel_names = ['BFP','GFP','CY3.5','TexRed']
            
            for channel in self.channel_names:
                self.default_channel[channel] = channel_config(channel, self.lasers)
                
        self.channel = copy.deepcopy(self.default_channel) # These are channels modified by the user
        
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
        
        self.list_channel_interface = {"checkBox_laser" :       self.checkBox_laser,
                                       "spinBox_laser_power" :  self.spinBox_laser_power,
                                       "slider_laser_power" :   self.slider_laser_power,
                                       "filter" :               self.comboBox_channel_filter,
                                       "camera" :               self.comboBox_channel_camera,
                                       "exposure_time" :        self.spinBox_channel_exposure_time
                                       } # Dictionnary used to set all the interface elements for a given channel
        
        self.comboBoxes_channel_order = [] # List of comboBoxes to select active channels
        self.active_channels = [] # List of active channels from self.comboBoxes_channel_order
        
        self.laser_emission = False # No laser actually emmited
        
            ### desable laser settings if not connected to DAQ
            
        self.sync_laser_interface() # Block modification and starting of not connected laser (to the DAQ)
        
        self.comboBox_channel_name_set_indexes() # Put all the channels to the self.comboBox_channel_name
        
        self.sync_filter_interface() # synchronize channels filters to avaliable filters (can be modified via action_Filters)

        #
        # Preview
        #
        
        self.min_grayscale = 0 # Lowest grey value of the preview
        self.max_grayscale = 65535 # Highest grey value of the preview
        self.preview_zoom = 0.25 # rescale factor of the preview
        self.look_up_table = 'grayscale' # The other LUT show the saturation
        
        self.is_preview = False # If there is a preview image displayed
        self.is_preview_paused = False # If preview is paused
        self.preview_frame = None # frame actually displayed
        self.preview_camera = 0 # Camera used for previex (default 0)
        self.preview_channel = self.channel[self.comboBox_channel_name.currentText()] # Dafault channel for previex is the first
        
        self.histogram_greyvalue_thread = None # Thread used to create grayscale graph
        
        self.preview_timer = QTimer() # Timer to show images
        self.preview_timer.timeout.connect(self.update_preview)
        
        self.timer_gray_hystogram = QTimer() # Timer to show grayscale graph
        self.timer_gray_hystogram.timeout.connect(self.update_gray_histogram)
        
        #
        # Petites choses de l'interface
        #

        if self.n_camera > 0 :
            self.label_fov_size_set_text() # Set label of the size of the field of view
            self.label_volume_duration_update() # Set label of the volume duration
        
            # Set icons
        
        self.Red_Light_Icon_On = QPixmap('Icons/Red_Light_Icon_On.png')
        self.Red_Light_Icon_Off = QPixmap('Icons/Red_Light_Icon_Off.png')
        
        self.label_laser_icon.setPixmap(self.Red_Light_Icon_Off)
        
        self.spinBox_aspect_ratio.setValue(self.experiment.aspect_ratio)
        
        ##############################################
        ## Connection between functions and buttons ##
        ##############################################
        
            ## Saving / Setup
        self.pb_data_path.clicked.connect(self.pb_data_path_value_changed)
        self.lineEdit_exp_name.editingFinished.connect(self.lineEdit_exp_name_modified)
        
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
    ## Connection between functions and toolbars ##
    ###############################################
    
            ## Fichier
        self.action_SaveConfig.triggered.connect(self.save_config)
        
            ## Config
        self.action_DAQ.triggered.connect(self.openDAQEditor)
        self.action_Filters.triggered.connect(self.openFiltersEditor)
        self.action_Microscope.triggered.connect(self.openMicroscopeEditor)
        
            ## Tools
        self.action_Align_O2_O3.triggered.connect(self.openAlign_O2_O3)
        self.action_Laser_405.triggered.connect(self.launch_laser_405_program)
        self.action_Laser_561.triggered.connect(self.launch_laser_561_program)
        self.action_Piezo.triggered.connect(self.launch_pizo_program)
        self.action_Z_Stack.triggered.connect(self.acquire_Z_Stack)
        
            ## Parameters
        self.action_channel_editor.triggered.connect(self.openChannelEditor)
        self.action_Preset_ROI_size.triggered.connect(self.openPreserROIEditor)
        
        
    #############################################
    ## Fonctions called when program is closed ##
    #############################################
        
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
                # Stop acquisition if necessary
                self.pb_stop_preview_clicked()
                # Turn of lasers if necessary
                self.pb_laser_emission.setChecked(False)
                self.pb_laser_emission_clicked()
                
            functions_camera.close_cameras(self.hcam)
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
        self.experiment.data_path = QFileDialog.getExistingDirectory(self, "Select Data Directory")
        
        if self.experiment.data_path:  # Si un dossier a été sélectionné
            self.label_data_path.setText(self.experiment.data_path)
        
    def lineEdit_exp_name_modified(self):
        """
        Ensures the experiment name is correctly formatted
        """
        exp_name = self.lineEdit_exp_name.text().strip()

        if not exp_name:
            self.status_bar.showMessage("Experiment name cannot be empty!", 5000)
            self.lineEdit_exp_name.setText(self.experiment.exp_name)
            
            return
            
        name_ok, self.experiment.exp_name = functions_ui.legalize_name(exp_name)
        
        if name_ok :
            self.status_bar.showMessage(f"Experiment name set to: {exp_name}", 2000)
        else:
            self.status_bar.showMessage("Invalid experiment name! Avoid spaces and special characters.", 5000)
            self.lineEdit_exp_name.setText(self.experiment.exp_name)

        #
        # Camera
        #
        
    def desactivate_camera_options(self, desactivation):
        """
        Desactive the options that use the camera if no camera is find in the system
        """
        if desactivation :
            self.label_camera_detected.setText('WARNING: No camera detected ! Please restart the interface.')
        else:
            self.label_camera_detected.setText(f"Number of cameras detected: {self.n_camera}")

        self.spinBox_hsize.setDisabled(desactivation)
        self.spinBox_hpos.setDisabled(desactivation)
        self.spinBox_vsize.setDisabled(desactivation)
        self.spinBox_vpos.setDisabled(desactivation)
        self.comboBox_size_preset.setDisabled(desactivation)
        self.pb_center_FOV.setDisabled(desactivation)
        self.comboBox_binning.setDisabled(desactivation)
        self.spinBox_channel_exposure_time.setDisabled(desactivation)
        self.pb_preview.setDisabled(desactivation)
        self.pb_pause_preview.setDisabled(desactivation)
        self.pb_stop_preview.setDisabled(desactivation)
        self.pb_snap.setDisabled(desactivation)
        self.pb_snoutscope_acquisition.setDisabled(desactivation)
        self.pb_multidimensional_acquisition.setDisabled(desactivation)

    def comboBox_camera_index_changed(self):
        """
        Set the new selected camera and the the interface qt objects depending on the selected camera
        """
        self.camera_id = self.comboBox_camera.currentIndex()
        
        self.spinBox_hsize.setMaximum(self.camera[self.camera_id].hchipsize)
        self.spinBox_hsize.setValue(self.camera[self.camera_id].hsize)
        self.spinBox_hpos.setValue(self.camera[self.camera_id].hpos)

        self.spinBox_vsize.setMaximum(self.camera[self.camera_id].vchipsize)
        self.spinBox_vsize.setValue(self.camera[self.camera_id].vsize)
        self.spinBox_hpos.setValue(self.camera[self.camera_id].vpos)
        
        self.comboBox_binning.setCurrentText(str(self.camera[self.camera_id].binning))
        
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
        self.camera[self.camera_id].calculate_image_readout_time()
        
        #set vpos
        self.spinBox_vpos_value_changed()
        
        self.label_volume_duration_update()
        
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
        self.spinBox_hpos_value_changed()
        
        self.spinBox_vpos.setValue(
            (self.camera[self.camera_id].vchipsize - self.spinBox_vsize.value())/2)
        self.spinBox_vpos_value_changed()
        
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
        'update comboBox_size_preset indexes after modification of preset sizes via specific widget'
        text = self.comboBox_size_preset.currentText()
        self.comboBox_size_preset.clear()
        self.comboBox_size_preset.addItems(self.preset_size)
        
        try:
            self.comboBox_size_preset.setCurrentText(text)
        except:
            pass 
        
    def comboBox_binning_index_changed(self):
        'set the Binning of the camera'
        binning = int(self.comboBox_binning.currentText())

        self.camera[self.camera_id].binning = binning
        
    def label_fov_size_set_text(self):
        'show the size of the fild of view in µm depending on camera settings'
        sample_pixel_size = self.camera[self.camera_id].sample_pixel_size
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
        - spinBox_scanner_position : chage the actual position for previex (not taken in account for exepriment)
        - pb_scanner_center : put the scanner to the central position (not taken in account for exepriment)
        - spinBox_scan_range : set the scan range of the experiment
        - spinBox_aspect_ratio : set the aspect ration between XY and Z axis, default is 3
        - spinBox_slit_aperture : set the value of the slit aperture (readed from the mechanical slit by user)
        - label_volume_duration : display the expected duration of each volume (for 1 color)
        """

    def spinBox_scanner_position_value_changed(self):
        self.experiment.scanner_position = self.spinBox_scanner_position.value()
        functions_daq.analog_out(self.spinBox_scanner_position.value()*self.microscope.volts_per_um,
                                 self.microscope.daq_channels['galvo'])
        
    def pb_scanner_center_clicked_connect(self):
        self.experiment.scanner_position = 0
        self.spinBox_scanner_position.setValue(0)
        
        
    def spinBox_scan_range_value_changed(self):
        self.experiment.scan_range = self.spinBox_scan_range.value()
        self.label_volume_duration_update()

        
    def spinBox_aspect_ratio_value_changed(self):
        self.experiment.aspect_ratio = self.spinBox_aspect_ratio.value()
        self.label_volume_duration_update()
    
    def spinBox_slit_aperture_value_changed(self):
        self.experiment.slit_aperture = self.spinBox_slit_aperture.value
        
    def label_volume_duration_update(self):
        message = functions_ui.label_volume_duration(self.experiment.scan_range,
                                                     self.camera[self.camera_id].sample_pixel_size ,
                                                     self.experiment.aspect_ratio,
                                                     self.microscope.tilt_angle,
                                                     self.preview_channel.exposure_time,
                                                     self.camera[self.camera_id].vsize,
                                                     self.camera[self.camera_id].line_readout_time,
                                                     self.microscope.galvo_response_time)
        
        self.label_volume_duration.setText(message)
    
        #
        # Channels settings
        #
        
            ### Enable / disable laser tool depending on DAC connection
    def sync_laser_interface(self):
        """
        Updates the laser interface and channels based on the connection status to the DAQ.
        It is used when updarting the interface
        
        This function iterates over each laser and checks its connection status
        to the DAQ (Data Acquisition) system. If a laser is not connected, the
        corresponding UI elements (checkbox and power spinbox) are disabled and
        reset. If a laser is connected, the UI elements are enabled, allowing
        the user to interact with them.
        
        This ensures that the user interface accurately reflects the current
        state of the laser connections.
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
        # self.pb_channel_save_clicked_connect() # To save the modification on the channel if it is the case
        
        functions_ui.channel_set_interface(self.list_channel_interface,
                                           self.channel[self.comboBox_channel_name.currentText()])
        
        self.preview_channel = self.channel[self.comboBox_channel_name.currentText()] # Change the current name of the channel used for preview
        
    def pb_channel_save_clicked_connect(self):
        "Saves the settings from the interface elements into the specified channel object."
        functions_ui.save_channel_from_interface(self.list_channel_interface,
                                                 self.channel[self.comboBox_channel_name.currentText()])
        # print(self.channel['BFP'].laser_power['405'])
    
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
        " Start or stop laser emission from actual channel after user click on pb_laser_emission"
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
        """
        Update the exposure time for the preview channel and the associated camera in real-time.
        If the interface is currently displaying a live image preview, the
        exposure time of the camera is also adjusted accordingly.
        """
        self.preview_channel.exposure_time = self.spinBox_channel_exposure_time.value()
        self.camera[self.preview_channel.camera].exposure_time = self.preview_channel.exposure_time /1000
        
        if self.is_preview: # Change exposure time during preview
            self.hcam[self.preview_channel.camera].set_exposure(self.camera[self.preview_channel.camera].exposure_time)
            
    
    def comboBox_channel_filter_index_changed(self):
        """
        This function will allow user to chancge the filter in live when filter weel will be avaliable
        """
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
    
        # Création du chemin de base
        
        base_file_path = os.path.join(self.experiment.data_path , f"{self.experiment.exp_name}_000.tiff")
        
        # Initialiser le suffixe
        suffix = 0
        file_path = base_file_path
        
        # Vérifier si le fichier existe déjà et trouver un nom disponible
        while os.path.exists(file_path):
            suffix += 1
            file_path = os.path.join(self.experiment.data_path, f"{self.experiment.exp_name}_{suffix:03d}.tiff")
                
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

            # Create and configure the acquisition thread
            self.camera_thread = CameraThread(self.hcam[self.preview_channel.camera])
            self.camera_thread.new_frame.connect(self.store_frame) # Get the frame from camera thread process
            
            # Set camera acquisition mode and parameters

            functions_camera.configure_camera_for_preview(self.hcam[self.preview_channel.camera],
                                                          self.camera[self.preview_channel.camera])

            # Start the camera acquisition and turn on laser
            self.hcam[self.preview_channel.camera].start_acquisition('sequence',2) # Not need to put to much or it slows donw the preview
            
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
        self.hcam[self.preview_channel.camera].clear_acquisition() # Not using stop_acquisition beacause it doesn't relese buffer
        
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
        "call a new therad to generate the gray histogram"
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
        " display the latest generated gray histogram"
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
        self.status_bar.showMessage("start Snoutscope acquisition", 10000)
        print("start Snoutscope acquisition")
        if self.is_preview:
            # Eteint l'acquisition si nécessaire
            self.pb_stop_preview_clicked()
            # Eteint les lasers si nécessaire
            self.pb_laser_emission.setChecked(False)
            self.pb_laser_emission_clicked()
            
        functions_camera.close_cameras(self.hcam)
        
        if self.active_channels and self.active_channels[0] != 'None' :
            try:
                send_to_snoutscope_acquisition(self.camera[0],
                                               self.channel[self.active_channels[0]],
                                               self.experiment, self.microscope)
                # Enregistre les données, ne prendra en compre que le premier channel choisi
                functions_ui.start_snoutscope_acquisition(file_path = 'D:/Projets_Python/OPM_GUI/snoutscopev3/Snoutscope.py',
                                                          working_directory = 'D:/Projets_Python/OPM_GUI/snoutscopev3')
            except:
                self.status_bar.showMessage("parameters saving didn't worked!", 5000)
        else:
            self.status_bar.showMessage("First channel shouldn't be None or empty", 5000)
            
        self.hcam , self.cameras = functions_camera.initialize_cameras(self.n_camera, self.microscope.mag_total)
            
    def pb_multidimensional_acquisition_clicked_connect(self):
        """Start acquisition with the Multi Dimentionnal Acquisition protocole from Thibault"""
        if self.is_preview:
            # Eteint l'acquisition si nécessaire
            self.pb_stop_preview_clicked()
            # Eteint les lasers si nécessaire
            self.pb_laser_emission.setChecked(False)
            self.pb_laser_emission_clicked()
        if self.active_channels and self.active_channels[0] != 'None' :
            try:
                channel_acquisition = functions_ui.get_active_channel(self.active_channels, self.channel)
                send_to_multidimensionnal_acquisition(self.camera,
                                                      channel_acquisition,
                                                      self.experiment,
                                                      self.microscope,
                                                      dirname = 'multidimensional_acquisition/Config',
                                                      filename = 'GUI_parameters.json')
                
                self.status_bar.showMessage("start multidimensional acquisition")
                functions_ui.start_multidimensional_acquisition(self.hcam)
            except:
                self.status_bar.showMessage("Multidimensional acquisition didn't worked!", 5000)
        else:
            self.status_bar.showMessage("First channel shouldn't be None or empty", 5000)
        
    ##################################
    ## Fonctions called by toolbars ##
    ##################################
    
        #
        # Fichiers
        #
        
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
            self.save_microscope_settings()
        elif reply == QMessageBox.No:
            pass
        
        #
        # Config
        #
        
    def openDAQEditor(self):
        "display window to eddit DAC channels"
        self.DAQ_editor = setDAQWindow(self.microscope.daq_channels,self)
        self.DAQ_editor.show()
    
    def openFiltersEditor(self):
        self.filters_editor = filtersEditionWindow(self.microscope.filters,self)
        self.filters_editor.show()
        
    def openMicroscopeEditor(self):
        self.microscope_settings_editor = microscope_settings_window(self.microscope, self)
        self.microscope_settings_editor.show()
        
        #
        # Tools
        #
        
    def openAlign_O2_O3(self):
        "display window to aligne O2 and O3 using the piezzo stage"
        self.alignement_O2_O3 = alignement_O2_O3_Window()
        self.alignement_O2_O3.show()
        
    def launch_program(self , shortcut_path):
        try:
            # Launch expernal program from shortcut
            os.startfile(shortcut_path)
        except Exception as e:
            print(f"Erreur lors du lancement du programme : {e}")
        
    def launch_laser_405_program(self):
        pass
    
    def launch_laser_561_program(self):
        pass
        
    def launch_pizo_program(self):
        "launch program for piezo between O2 and O3 : CONEX-SAG_Utility "
        shortcut_path = os.path.join(os.path.dirname(__file__), 'shortcuts', 'CONEX-SAG_Utility')
        self.launch_program(shortcut_path)
        
    def acquire_Z_Stack(self):
        """Start acquisition of a Z-stack.
        It is only in purpose of characterizing microscope,
        nothing is optimized in these functions.
        """
        
        # Get values from the interface for scanning
        scan_range = self.spinBox_scan_range.value()
        step_size = self.doubleSpinBox_step_size.value()
        
        if self.is_preview :
            self.pb_stop_preview_clicked()
        
        if scan_range > 0 and step_size > 0 :
            
            self.status_bar.showMessage("Acquiring Z-Stack")
            
            self.is_preview = True
            self.preview_tools_desactivation()
            
            functions_camera.configure_camera_for_preview(self.hcam[self.preview_channel.camera],
                                                          self.camera[self.preview_channel.camera])
            
            path = os.path.join(self.experiment.data_path, self.experiment.exp_name)
            
            functions_ui.create_directory_if_not_exists(path)
            
            z_stack_acquisition = z_stack(self.hcam[self.preview_channel.camera],path, self.microscope.stage_port)
            
            self.pb_laser_emission.setChecked(True)
            self.pb_laser_emission_clicked()
            
            z_stack_acquisition.acquisition(scan_range,
                                            step_size)
            
            self.is_preview = False
            self.preview_tools_desactivation()
        
        else :
            self.status_bar.showMessage("scan range and step size shouldn't be 0")
                
        #
        # Parameters
        #
        
    def openPreserROIEditor(self):
        "display window to eddit preset ROI that can be used"
        if self.n_camera > 0 :
            self.presetROI_editor = PresetROIWindow(self.preset_size ,
                                                    [self.camera[self.camera_id].hchipsize ,
                                                     self.camera[self.camera_id].vchipsize],
                                                    self)
            self.presetROI_editor.show()
        else:
            self.statusbar.showMessage('No camera connected', 5000)
    
    def openChannelEditor(self):
        "display window to eddit default channels of the microscope"
        self.channel_editor = ChannelEditorWindow(self.default_channel, self.channel_names, self)
        self.channel_editor.show()
        pass
    
    ############################################
    ## Fonctions to save interface variables ##
    ###########################################
    
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
        
        saved_variables = {'preset_size' : self.preset_size,
                           'experiment_data_path' : self.experiment.data_path,
                           'exp_name' : self.experiment.exp_name,
                           'slit_aperture' : self.experiment.slit_aperture}
        
        with open(file_path, 'w') as file:
            json.dump(saved_variables, file, indent = 4)
            
    #
    # Microscope
    #
    
    def load_microscope_settings(self):
        config_dir = 'configs'
        file_path = os.path.join(config_dir, 'microscope_settings.pkl')
        
        self.loaded_microscope_settings = False
        
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                data = pickle.load(file)
                self.microscope = data
                
            self.loaded_microscope_settings = True
        
        return self.loaded_microscope_settings
    
    def save_microscope_settings(self):
        config_dir = 'configs'
        os.makedirs(config_dir, exist_ok=True)  # Crée le dossier s'il n'existe pas
        file_path = os.path.join(config_dir, 'microscope_settings.pkl')
        
        microscope_settings_data = self.microscope
        
        with open(file_path, 'wb') as file:
            pickle.dump(microscope_settings_data, file)
    
    
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