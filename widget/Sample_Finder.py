# -*- coding: utf-8 -*-
"""
Sample Finder GUI for live previewing camera images and controlling illumination.

This widget connects to a Thorlabs camera (TLCamera via pylablib) and allows:
- Live preview display with grayscale LUT, zoom, and auto-contrast
- Snapshots saved to TIFF files
- Real-time histogram visualization of the current frame
- Basic control buttons (mirror, fluorescence, transmission light)
"""

import atexit
import numpy as np
import os
from pylablib.devices import Thorlabs
import sys
import tifffile

from PySide6.QtCore import QTimer, QThread, Signal
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtGui import QPixmap, QImage

import pylablib as pll
pll.par['devices/dlls/thorlabs_tlcam'] = r"C:\Program Files\Thorlabs\ThorImageCAM\Bin\thorlabs_tsi_camera_sdk.dll"

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    
from hardware.functions_DAQ import functions_daq
from widget.ui_sample_finder import Ui_Form

from display.histogram import HistogramThread
from Functions_UI import functions_ui

import warnings

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API"
)

warnings.filterwarnings(
    "ignore",
    message="model number .* doesn't match the device ID prefix"
)

class sample_finder_Window(QWidget, Ui_Form):
    """
    GUI widget for previewing images from a Thorlabs TLCamera device
    and controlling simple illumination/mirror settings.
    """
    
    def __init__(self, experiment = None, microscope = None, parent=None):
        """
        Initialize the sample finder widget.
        
        Args:
            experiment (object): Experiment metadata (name, data path).
            microscope (object): Microscope controller (not used directly here).
            parent (QWidget): Parent widget for Qt hierarchy.
        """
        
        super().__init__(parent)
        self.setupUi(self)
        self.experiment = experiment
        self.microscope = microscope
        self.on_init()
        
        atexit.register(self._on_close)
        
    def on_init(self):
        """Perform all initialization: camera, GUI defaults, timers, connections."""
        
        self.setWindowTitle('Sample Finder')
        
        ###############################
        ## Creation of the Variables ##
        ###############################
        
            #
            # Get informations from microscope
            #
            
        if self.microscope is None :
            self.mff_ser_num = 37009743
        else:
            try:
                self.mff_ser_num = self.microscope.trans_mirror_ser_num
            except:
                self.mff_ser_num = 37009743
                
        if self.microscope is None:
            self.daq_transmission = "Dev1/port0/line12"
            self.daq_fluo = None
        else:
            try :
                self.daq_transmission = self.microscope.daq_channels["transmission_light"]
                self.daq_fluo = self.microscope.daq_channels["fluo_light"]
            except:
                self.daq_transmission = "Dev1/port0/line12"
                self.daq_fluo = None    
                
        self.mirror = Thorlabs.kinesis.MFF(self.mff_ser_num)
        
            #
            # Initialize camera
            #
            
        self.tlcameras_list = Thorlabs.list_cameras_tlcam()
        
        if len(self.tlcameras_list) >=1:
            self.tlcam = Thorlabs.ThorlabsTLCamera(serial=self.tlcameras_list[0])
            self.tlcam.open()
            self.tlcam.set_exposure(10/1000)
        else :
            self.label_message.setText("No camera connected")
            self.desactivate_camera_options()
            self.tlcam = None
        
            #
            # Saving Path
            #
        
        if self.experiment is not None :
            self.exp_name = self.experiment.exp_name
            self.data_path = self.experiment.data_path
        else:
            self.exp_name = 'Image'
            self.data_path = "D:/Projets_Python/OPM_GUI/Images"
            
            #
            # Settingss
            #
            
        self.exposure_time = 10 # in milliseconds
        self.cube = 1
        
            #
            # Preview defaults
            #
        
        self.min_grayscale = 0 # Lowest grey value of the preview
        self.max_grayscale = 4095 # Highest grey value of the preview
        self.preview_zoom = 0.25 # rescale factor of the preview
        self.look_up_table = 'grayscale' # The other LUT show the saturation
        self.preview_zoom = 0.33
        self.is_preview = False # If there is a preview image displayed
        self.is_preview_paused = False # If preview is paused
        self.preview_frame = None # frame actually displayed
        self.histogram_greyvalue = None
        self.histogram_greyvalue_thread = None
        
            #
            # Position saving
            #
            
        self.positions = {} # Will be used to save positions for multi-position immaging
        
            #
            # Interface icons
            #
            
        if __name__ == "__main__": # Si jamais la fenêtre est appelée depuis ce fichier
            self.Red_Light_Icon_On = QPixmap(os.path.join(parent_dir, 'Icons/Red_Light_Icon_On.png'))
            self.Red_Light_Icon_Off = QPixmap(os.path.join(parent_dir, 'Icons/Red_Light_Icon_Off.png'))
            self.Green_Light_Icon_On = QPixmap(os.path.join(parent_dir, 'Icons/Green_Light_Icon_On.png'))
            self.Green_Light_Icon_Off = QPixmap(os.path.join(parent_dir, 'Icons/Green_Light_Icon_Off.png'))
        else:
            self.Red_Light_Icon_On = QPixmap('Icons/Red_Light_Icon_On.png')
            self.Red_Light_Icon_Off = QPixmap('Icons/Red_Light_Icon_Off.png')
            self.Green_Light_Icon_On = QPixmap('Icons/Green_Light_Icon_On.png')
            self.Green_Light_Icon_Off = QPixmap('Icons/Green_Light_Icon_Off.png')
        
        self.label_mirror_icon.setPixmap(self.Green_Light_Icon_Off)
        self.label_fluo_icon.setPixmap(self.Red_Light_Icon_Off)
        self.label_transmission_icon.setPixmap(self.Red_Light_Icon_Off)
        
            #
            # Timers
            #
        
        # self.timer_illuminator = QTimer() # Timer to show the illuminator weel position
        # self.timer_illuminator.timeout.connect(self.update_illuminator)
        # self.timer_illuminator.start(100)
        self.timer_mirror = QTimer()
        self.timer_mirror.timeout.connect(self.update_mirror_position)
        self.timer_mirror.start(200)
        
        self.timer_preview = QTimer() # Timer to show new frame
        self.timer_preview.timeout.connect(self.update_preview)
        
        self.timer_gray_hystogram = QTimer() # Timer to show grayscale graph
        self.timer_gray_hystogram.timeout.connect(self.update_gray_histogram)
        
        ##############################################
        ## Connection between functions and buttons ##
        ##############################################
        
            ## Saving / Setup
        self.pb_data_path.clicked.connect(self.pb_data_path_value_changed)
        self.lineEdit_exp_name.editingFinished.connect(self.lineEdit_exp_name_modified)
        
            ## Mirror, light, exposition, filter
        self.pb_mirror.clicked.connect(self.pb_mirror_clicked)
        self.pb_fluo.clicked.connect(self.pb_fluo_clicked)
        self.pb_transmission.clicked.connect(self.pb_transmission_clicked)
        self.spinBox_channel_exposure_time.valueChanged.connect(self.spinBox_channel_exposure_time_value_changed)
        
            ## Preview visualisation
        self.comboBox_LUT.currentIndexChanged.connect(self.comboBox_LUT_changed)
        self.comboBox_preview_zoom.currentIndexChanged.connect(self.comboBox_preview_zoom_changed)
        self.spinBox_max_grayscale.valueChanged.connect(self.spinBox_grayscale_value_changed)
        self.spinBox_min_grayscale.valueChanged.connect(self.spinBox_grayscale_value_changed)
        self.pb_minmax_grayscale.clicked.connect(self.pb_minmax_grayscale_clicked)
        self.pb_reset_grayscale.clicked.connect(self.pb_resset_grayscale_clicked)
        self.pb_auto_grayscale.clicked.connect(self.pb_auto_grayscale_clicked)
        
             ## Preview controll
        self.pb_preview.clicked.connect(self.pb_preview_clicked)
        self.pb_pause_preview.clicked.connect(self.pb_pause_preview_clicked)
        self.pb_stop_preview.clicked.connect(self.pb_stop_preview_clicked)
        self.pb_snap.clicked.connect(self.pb_snap_clicked)
        
        #####################################
        ## Functions called by the buttons ##
        #####################################
        self.comboBox_illuminator.setEnabled(False)
        self.pb_fluo.setEnabled(False)
        
    def desactivate_camera_options(self):
        """Disable the whole widget when no camera is connected."""
        self.setDisabled(True)
        
            #
            # Saving experiment
            #
            
    def pb_data_path_value_changed(self):
        """
        Opens a dialog to select a directory and updates the pb_data_path field.
        """
        self.data_path = QFileDialog.getExistingDirectory(self, "Select Data Directory")
        
        if self.data_path:  # Si un dossier a été sélectionné
            self.label_data_path.setText(self.data_path)
            
    def lineEdit_exp_name_modified(self):
        """
        Validate and update the experiment name after editing.
        """
        exp_name = self.lineEdit_exp_name.text().strip()

        if not exp_name:
            self.label_message.setText("Experiment name cannot be empty!")
            self.lineEdit_exp_name.setText(self.exp_name)
            return
            
        name_ok, self.exp_name = functions_ui.legalize_name(exp_name)
        
        if name_ok :
            self.label_message.setText(f"Experiment name set to: {exp_name}")
        else:
            self.label_message.setText("Invalid experiment name! Avoid spaces and special characters.")
            self.lineEdit_exp_name.setText(self.exp_name)
            
            #
            # Mirror, light, exposition
            #
            
    def pb_mirror_clicked(self):
        """Toggle the mirror in/out state and update the icon/label."""
        if self.pb_mirror.isChecked():
            self.mirror.move_to_state(0)
        else:
            self.mirror.move_to_state(1)
            
    def pb_fluo_clicked(self):
        """Toggle the fluorescence lamp on/off."""
        if self.pb_fluo.isChecked():
            self.label_fluo_icon.setPixmap(self.Red_Light_Icon_On)
            self.label_fluo.setText("ON ")
        else:
            self.label_fluo_icon.setPixmap(self.Red_Light_Icon_Off)
            self.label_fluo.setText("OFF")
            
    def pb_transmission_clicked(self):
        """Toggle the transmission lamp on/off."""
        if self.pb_transmission.isChecked():
            functions_daq.digital_out(signal = True, line_name = self.daq_transmission)
            self.label_transmission_icon.setPixmap(self.Red_Light_Icon_On)
            self.label_transmission.setText("ON")
        else:
            functions_daq.digital_out(False, self.daq_transmission)
            self.label_transmission_icon.setPixmap(self.Red_Light_Icon_Off)
            self.label_transmission.setText("OFF")
            
    def spinBox_channel_exposure_time_value_changed(self):
        """Update exposure time on the camera when the spin box changes."""
        self.exposure_time = self.spinBox_channel_exposure_time.value()
        self.tlcam.set_exposure(self.exposure_time/1000)
        
        #
        # Preview
        #
        
    def comboBox_LUT_changed(self):
        """Change the look-up table (LUT) used for image display."""
        index = self.comboBox_LUT.currentIndex()
        LUTs = ["grayscale","show_saturation"]
        self.look_up_table = LUTs[index]
        
    def comboBox_preview_zoom_changed(self):
        """Update the preview zoom factor from the combo box."""
        self.preview_zoom = [0.25 , 2 , 1 , 0.5 , 1/3 , 0.25][self.comboBox_preview_zoom.currentIndex()]
        
            ### Changement min / max grayscales
    
    def spinBox_grayscale_value_changed(self):
        """Update grayscale min/max values ensuring min < max."""
        
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
        
    def pb_minmax_grayscale_clicked(self):
        """Set grayscale min/max based on current frame values."""
        if self.preview_frame is not None:
            frame = self.preview_frame
            self.spinBox_min_grayscale.setValue(np.min(frame))
            self.spinBox_max_grayscale.setValue(np.max(frame))
        else:
            pass
    
    def pb_auto_grayscale_clicked(self):
        """Automatically adjust grayscale values using auto contrast."""
        if self.preview_frame is not None :
            frame = self.preview_frame
            min_gray, max_gray = functions_ui.auto_contrast(frame)
            
            self.spinBox_min_grayscale.setValue(min_gray)
            self.spinBox_max_grayscale.setValue(max_gray)
    
    def pb_resset_grayscale_clicked(self):
        """Reset grayscale values to full dynamic range (0–4095)."""
        self.spinBox_min_grayscale.setValue(0)
        self.spinBox_max_grayscale.setValue(4095)
    
        #
        # Preview controll
        #
    
    def pb_preview_clicked(self):
        """Start live preview acquisition if not already running."""
        if not self.is_preview:
            self.label_message.setText("Displaying Preview")
            self.is_preview = True
            
            # Start camera acquisition in separate thread
            self.camera_thread = TLCameraThread(self.tlcam)
            self.camera_thread.new_frame.connect(self.store_frame) # Get the frame from camera thread process
            self.tlcam.start_acquisition(nframes=2)
            self.camera_thread.start()
            
            # Start timers for updating display and histogram
            self.timer_preview.start(30)
            self.timer_gray_hystogram.start(50)
  
        if self.is_preview_paused:
            self.is_preview_paused = False
    
    def pb_pause_preview_clicked(self):
        """Pause or resume preview depending on button state."""
        self.is_preview_paused = self.pb_pause_preview.isChecked()
    
    def pb_stop_preview_clicked(self):
        """Stop preview acquisition and threads."""
        if self.is_preview :
            self.is_preview = False
            self.timer_preview.stop()
            self.timer_gray_hystogram.stop()
            self.camera_thread.stop()
            self.camera_thread.wait()
    
    def pb_snap_clicked(self):
        """Save the current frame to a TIFF file with an incremental filename."""
        
        if self.preview_frame is None:
            self.label_image_preview.setText("No frame available to save.")
            return
    
        # Build file path with increment
        
        base_file_path = os.path.join(self.data_path , f"{self.exp_name}_000.tiff")
        
        # Initialiser le suffixe
        suffix = 0
        file_path = base_file_path
        
        # Vérifier si le fichier existe déjà et trouver un nom disponible
        while os.path.exists(file_path):
            suffix += 1
            file_path = os.path.join(self.data_path, f"{self.exp_name}_{suffix:03d}.tiff")
                
        try:
            tifffile.imwrite(file_path, self.preview_frame)
            self.label_image_preview.setText(f"Frame saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save frame:\n{str(e)}")
            
        #
        # Frame acquisition and display
        #
    def update_illuminator(self):
        """Update the illuminator wheel position randomly (placeholder)."""
        self.cube = 0
        self.comboBox_illuminator.setCurrentIndex(self.cube)
            
    def update_mirror_position(self):
        try :
            position = self.mirror.get_state()
        except:
            print('[Sample Finder] Error during mirror position reading')
            return
        
        if position == 0:
            self.label_mirror_icon.setPixmap(self.Green_Light_Icon_On)
            self.pb_mirror.setChecked(True)
            self.label_mirror.setText("IN ")
        elif position == 1 :
            self.label_mirror_icon.setPixmap(self.Green_Light_Icon_Off)
            self.pb_mirror.setChecked(False)
            self.label_mirror.setText("OUT")
        elif position is None :
            return
            
        
    def store_frame(self, frame):
        """Receive a frame from the camera thread and store it (unless paused)."""
        if not self.is_preview_paused :
            self.preview_frame = frame
    
    def update_preview(self):
        """Display the most recent frame in the GUI."""
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
        """Trigger the histogram update if no thread is currently running."""
        if not self.histogram_greyvalue_thread or not self.histogram_greyvalue_thread.isRunning() :
            self.generate_histogram()

    def generate_histogram(self):
        """Launch a thread to compute the histogram of the current frame."""
        if self.preview_frame is not None:
            size = self.label_histogram_greyvalue.size()
            w , h = size.width() , size.height()
            self.histogram_greyvalue_thread = HistogramThread(self.preview_frame,
                                                              self.min_grayscale,
                                                              self.max_grayscale,
                                                              w_px = w, h_px = h,
                                                              ax_xmax = 4095)
            self.histogram_greyvalue_thread.histogram_ready.connect(self.display_gray_histogram)
            self.histogram_greyvalue_thread.start()
        
    def display_gray_histogram(self, image_data, w, h):
        """Display the latest generated histogram image in the GUI."""
        qimage = QImage(image_data, w, h, w * 4, QImage.Format_RGBA8888)
        self.label_histogram_greyvalue.setPixmap(QPixmap.fromImage(qimage))
    
        #
        # Close
        #
        
    def _on_close(self):
        self.mirror.move_to_state(1)
        functions_daq.digital_out(False, self.daq_transmission)
        
    def closeEvent(self, event):
        """Intercept close event: confirm and release hardware resources."""
        reply = QMessageBox.question(
            self, 'Confirmer changes',
            """"Are you sure you want to close the sample finder window?""",
            QMessageBox.Yes | QMessageBox.No )

        if reply == QMessageBox.Yes:
            self.pb_stop_preview_clicked()
            # self.mirror.move_to_state(1)
            # functions_daq.digital_out(False, self.daq_transmission)
            if self.tlcam is not None :
                self.tlcam.close()
            self.pb_mirror.setChecked(False)
            self.pb_mirror_clicked()
            self.pb_transmission.setChecked(False)
            self.pb_transmission_clicked()
            self.pb_fluo.setChecked(False)
            self.pb_fluo_clicked()
            event.accept()
        elif reply == QMessageBox.No:
            event.ignore()
        else:
            event.accept()
            
class TLCameraThread(QThread):
    """
    Thread dedicated to continuously reading images from the Thorlabs TLCamera.
    Emits the most recent frame via the new_frame signal.
    """
    new_frame = Signal(np.ndarray)  # Signal émis à chaque nouvelle image

    def __init__(self, tlcam):
        super().__init__()
        self.tlcam = tlcam
        self.running = True  # Permet de contrôler l'arrêt propre du thread

    def run(self):
        """Main acquisition loop: read and emit frames continuously."""
        while self.running:
            frames = self.tlcam.read_multiple_images()
            if frames:
                frame = frames[-1]  # On prend la dernière image disponible

                self.new_frame.emit(frame)  # Émettre l'image pour l'affichage
            
            self.msleep(10)

    def stop(self):
        """Stop acquisition loop cleanly."""
        self.running = False
        self.quit()
        self.wait()
            
        
#################################################################
        
if __name__ == '__main__':
    "To test the window"
    app = QApplication(sys.argv)
    
    editor = sample_finder_Window()
    editor.show()
    sys.exit(app.exec())