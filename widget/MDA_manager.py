# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 16:30:29 2025

@author: tbrugiere

pyside6-uic widget/ui_mda.ui -o widget/ui_mda.py
"""
import cv2
import numpy as np
import os
import sys
import time
import threading

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer, QObject, Signal, Slot, QThread, Qt

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

from image_analysis.Deskew_Numpy import deskew_numpy, compute_px_shift, mean_projection_ignore_zeros
from multidimensional_acquisition.Live_Viewer.mda_manager_functions import update_timelapse_strip
from multidimensional_acquisition.Live_Viewer.mda_manager_functions import auto_contrast
from multidimensional_acquisition.Live_Viewer.mda_manager_functions import get_timeline_frame_width
from multidimensional_acquisition.Live_Viewer.mda_manager_functions import LookUpTables

from widget.ui_mda import Ui_Form

class mda_mannager(QWidget, Ui_Form):
    """
    Show the window to follow rhe multidimensionnal acquisition.
    """
    channel_received = Signal(tuple)
    
    def __init__(self, mda, parent=None):
        
        super().__init__(parent)
        self.setupUi(self)
        self.mda = mda
        self.on_init()
        
    def on_init(self):
        self.setWindowTitle('Multidimensionnal Acquisition')
        self.setWindowFlag(Qt.Window) 
        
        ###############################
        ## Creation of the Variables ##
        ###############################
    
        
        self.info_timer = QTimer() # Timer to update informations
        self.info_timer.timeout.connect(self.update_infos) # Connected to update informations
        
        #
        # Values for displaying, calculation
        #
        
        self.total_timepoints = self.mda.config.experiment.timepoints
        self.total_images = self.total_timepoints * self.mda.config.experiment.n_steps * len(self.mda.config.channels)
        self.total_channels = len(self.mda.config.channels)
        self.channel_names = [ch.channel_id for ch in self.mda.config.channels]
        self.channel_display = self.channel_names[0]
        
        self._cb_image_channel_set()
        
        self.images_acquired = 0
        self.frames_acquired = 0
        self.frames_dropped = 0
        self.channel_saved = 0
        self.volumes_recived = 0
        
            # Pixel shift between two images of the volume for deskewing
        self.pixel_shift = compute_px_shift(self.mda.config.experiment.aspect_ratio,
                                            self.mda.config.microscope.tilt_angle,
                                            unit = "deg")
        
        self.ellapsed_time = time.time()
        
        #
        # Images to display
        #
        
        self.project_max_front = {key: None for key in self.channel_names}
        self.project_max_side  = {key: None for key in self.channel_names}
        self.project_mean_front = {key: None for key in self.channel_names}
        self.project_mean_side  = {key: None for key in self.channel_names}
        self.strip_max = {key: None for key in self.channel_names}
        self.strip_mean = {key: None for key in self.channel_names}
        
        #
        # Values for the interface
        #
        
        self.LUT = {key : "Grayscale" for key in self.channel_names}
        self.min_grayscale = {key : 0 for key in self.channel_names}
        self.max_grayscale = {key : 65535 for key in self.channel_names}
        
        self.zoom = 1
        self.projection = "max"
        self.timeline_position = 1
        self.timeline_frame_width = 128 # width of an image for the
        self.palettes = LookUpTables().palettes
        
        #
        # Set different parts of the interface
        #
        
        self._set_progress_bar()
        self._cb_lut_set()
        
        #
        # Connect to the parallel thread that calculate projections
        #
        
        self.processor_thread = QThread()
        self.channel_processor = ChannelProcessor(self.pixel_shift)
        self.channel_processor.moveToThread(self.processor_thread)
        self.channel_processor.processed.connect(self.receive_projections)
        self.processor_thread.start()
        self.channel_received.connect(self.channel_processor.process)
        
        ##############################################
        ## Connection between functions and buttons ##
        ##############################################
        
        self.cb_projection.currentIndexChanged.connect(self.cb_projection_index_changed)
        self.cb_lut.currentIndexChanged.connect(self.cb_lut_index_changed)
        self.cb_image_channel.currentIndexChanged.connect(self.cb_image_channel_index_changed)
        
        self.pb_grayscale_min_max.clicked.connect(self.pb_grayscale_min_max_clicked)
        self.pb_grayscale_auto.clicked.connect(self.pb_grayscale_auto_clicked)
        self.pb_grayscale_reset.clicked.connect(self.pb_grayscale_reset_clicked)
        self.sb_grayscale_min.valueChanged.connect(self.sb_grayscale_value_changed)
        self.sb_grayscale_max.valueChanged.connect(self.sb_grayscale_value_changed)
        
        self.sb_timeline.valueChanged.connect(self.sb_timeline_value_changed)
        
        #####################################
        ## Functions called by the buttons ##
        #####################################
        
    def _cb_image_channel_set(self):
        self.cb_image_channel.clear()
        self.cb_image_channel.addItems(self.channel_names)
        self.cb_image_channel.setCurrentIndex(0)
        self.channel_display = self.cb_image_channel.currentText()
        
    def _cb_lut_set(self):
        self.cb_lut.clear()
        self.cb_lut.addItems(list(self.palettes.keys()))
        self.cb_lut.setCurrentIndex(0)
        self.LUT[self.channel_display] = self.cb_lut.currentText()
        
    def _set_interface_channel(self):
        self.slider_grayscale_max.blockSignals(True)
        self.slider_grayscale_max.setValue(self.max_grayscale[self.channel_display])
        self.slider_grayscale_max.blockSignals(False)
        self.sb_grayscale_max.blockSignals(True)
        self.sb_grayscale_max.setValue(self.max_grayscale[self.channel_display])
        self.sb_grayscale_max.blockSignals(False)
        self.slider_grayscale_min.blockSignals(True)
        self.slider_grayscale_min.setValue(self.min_grayscale[self.channel_display])
        self.slider_grayscale_min.blockSignals(False)
        self.sb_grayscale_min.blockSignals(True)
        self.sb_grayscale_min.setValue(self.min_grayscale[self.channel_display])
        self.sb_grayscale_min.blockSignals(False)
        self.cb_lut.blockSignals(True)
        self.cb_lut.setCurrentText(self.LUT[self.channel_display])
        self.cb_lut.blockSignals(False)
        
    def cb_projection_index_changed(self):
        if self.cb_projection.currentText() == "Mean":
            self.projection = "mean"
        elif self.cb_projection.currentText() == "Maximum":
            self.projection= "max"
            
        self.update_preview()
        
    def cb_lut_index_changed(self):
        self.LUT[self.channel_display] = self.cb_lut.currentText()
        self.update_preview()
        
    def cb_image_channel_index_changed(self):
        self.channel_display = self.cb_image_channel.currentText()
        self._set_interface_channel()
        self.update_preview()

    def pb_grayscale_min_max_clicked(self):
        if self.project_mean_front[self.channel_display] is not None and self.project_max_front[self.channel_display] is not None :
            if self.projection == "mean" :
                self.slider_grayscale_min.setValue(np.min(self.project_mean_front[self.channel_display]))
                self.slider_grayscale_max.setValue(np.max(self.project_mean_front[self.channel_display]))
                
            elif self.projection == "max" :
                self.slider_grayscale_min.setValue(np.min(self.project_max_front[self.channel_display]))
                self.slider_grayscale_max.setValue(np.max(self.project_max_front[self.channel_display]))
                
    def pb_grayscale_auto_clicked(self):
        if self.project_mean_front[self.channel_display] is not None and self.project_max_front[self.channel_display] is not None :
            if self.projection == "mean" :
                min_gray, max_gray = auto_contrast(self.project_mean_front[self.channel_display])
                
            elif self.projection == "max" :
                min_gray, max_gray = auto_contrast(self.project_max_front[self.channel_display])
                
            self.slider_grayscale_min.setValue(min_gray)
            self.slider_grayscale_max.setValue(max_gray)

    
    def pb_grayscale_reset_clicked(self):
        self.slider_grayscale_min.setValue(0)
        self.slider_grayscale_max.setValue(65535)
        
    def sb_grayscale_value_changed(self):
        """
        Updates the grayscale min and max values used for image display, ensuring 
        that min_grayscale is always less than max_grayscale. Also updates the 
        coefficient for grayscale conversion and refreshes the UI elements accordingly.
        """
        
        # Retrieve the current values from the spin boxes
        self.min_grayscale[self.channel_display] = self.sb_grayscale_min.value()
        self.max_grayscale[self.channel_display] = self.sb_grayscale_max.value()
        
        # Ensure that min_grayscale is always strictly less than max_grayscale
        if self.min_grayscale[self.channel_display] >= self.max_grayscale[self.channel_display]:
            self.min_grayscale[self.channel_display] = self.max_grayscale[self.channel_display] - 1 # Adjust min_grayscale
            
            # Update the spin box value while blocking signals to avoid infinite loops
            self.sb_grayscale_min.blockSignals(True)
            self.sb_grayscale_min.setValue(self.min_grayscale[self.channel_display])
            self.sb_grayscale_min.blockSignals(False)
            
            # Update the slider value similarly
            self.slider_grayscale_min.blockSignals(True)
            self.slider_grayscale_min.setValue(self.min_grayscale[self.channel_display])
            self.slider_grayscale_min.blockSignals(False)
            
        self.update_preview()
        
    def sb_timeline_value_changed(self):
        self.timeline_position = self.sb_timeline.value()
        
        if self.projection == "max":
            self.display_timelapse_strip(self.strip_max[self.channel_display], self.label_timeline)
            
        elif self.projection == "mean":
            self.display_timelapse_strip(self.strip_mean[self.channel_display], self.label_timeline)
        
        
        ###########################################
        ## Functions for displaying informations ##
        ###########################################
        
    def start_acquisition(self):
        self.mda.initialize_cameras()
        self.mda.initialize_acquisition_workers()
        self.set_controller()
        self.mda.configure_daq()
        
        # Lancer l'acquisition dans un thread à part
        threading.Thread(target=self.mda.run, daemon=True).start()
        self.info_timer.start(30)
        
        #
        # Get informations and update the progress bar
        #
        
    def update_infos(self):
        if self.mda.acquisition_workers[0].camera.start_time is not None :
            if self.mda.state["daq"] == "idle":
                pass
            else:
                self.ellapsed_time = time.time() - self.mda.acquisition_workers[0].camera.start_time
        else:
            self.ellapsed_time = 0
            
        self.images_acquired = self.mda.acquisition_workers[0].total_images
        self.frames_acquired = self.mda.acquisition_workers[0].total_frames
        self.frames_dropped = self.mda.acquisition_workers[0].total_dropped
        self.channels_saved = self.mda.acquisition_workers[0].total_volumes
        self.label_informations.setText(f"""
Camera : {self.mda.state["camera"]}, DAQ : {self.mda.state["daq"]}
Frames Acquired: {self.frames_acquired}/{self.total_images}
Frames Dropped: {self.frames_dropped}/{self.total_images}
Channels Saved: {self.channels_saved}/{self.total_timepoints * self.total_channels}
Volumes Recived: {self.volumes_recived}
Time Ellapsed: {self.format_time(self.ellapsed_time)} s
                                        """)
        self.update_progress_bar()
                                        
    def _set_progress_bar(self):
        self.progressBar_acquisition.setMaximum(self.total_images)
        self.progressBar_saving.setMaximum(self.total_timepoints * self.total_channels)
    
    def update_progress_bar(self):
        self.progressBar_acquisition.setValue(int(self.images_acquired))
        self.progressBar_saving.setValue(int(self.channels_saved))
        
        
        ####################################################
        ## Functions for processing ans displaying images ##
        ####################################################

    def set_controller(self):
        """
        Branche le contrôleur principal (MultidimensionalAcquisition) à l’interface.
        Connecte les signaux de preview pour affichage en temps réel.
        """
    
        # Pour l’instant, une seule caméra => worker(0)
        worker = self.mda.acquisition_workers[0]
        worker.new_volume_ready.connect(self.handle_new_channel)
        worker.set_preview_callback()
        
    def handle_new_channel(self, channel: np.ndarray, metadata: dict):
        self.volumes_recived = metadata["volume_id"]
        self.update_infos()
        
        # Senf the new volume recievend to the volume_processor thread
        self.channel_received.emit((channel, metadata))
    
    def receive_projections(self, data):
        # Get the four projections
        channel = data["metadata"]["channel"]
        self.project_max_front[channel] = data["max_front"]
        self.project_max_side[channel]  = data["max_side"]
        self.project_mean_front[channel] = data["mean_front"]
        self.project_mean_side[channel]  = data["mean_side"]
        
        if self.volumes_recived == 1:
            self.timeline_frame_width = get_timeline_frame_width(self.project_max_front[channel]) + 2
        
        # Calculate the timelaps strip
        self.strip_max[channel] = update_timelapse_strip(self.strip_max[channel], self.project_max_front[channel])
        self.strip_mean[channel] = update_timelapse_strip(self.strip_mean[channel], self.project_mean_front[channel])
        
        # Mets à jour les réglages de la timeline
            
        self.sb_timeline.setMaximum(int(self.volumes_recived))
        self.slider_timeline.setMaximum(int(self.volumes_recived))
        
        if self.timeline_position == int(self.volumes_recived) - 1:
            self.sb_timeline.setValue(int(self.volumes_recived))
        
        self.update_preview()
        
    def update_preview(self):
        if self.projection == "max":
            self.display_image(self.project_max_front[self.channel_display])
            self.display_side_view(self.project_max_side[self.channel_display])
            self.display_timelapse_strip(self.strip_max[self.channel_display], self.label_timeline)
            
        elif self.projection == "mean":
            self.display_image(self.project_mean_front[self.channel_display])
            self.display_side_view(self.project_mean_side[self.channel_display])
            self.display_timelapse_strip(self.strip_mean[self.channel_display], self.label_timeline)
        
        
    def display_image(self, img: np.ndarray):
        qimg = self.create_preview(img)
        self.label_mainImage.setPixmap(QPixmap.fromImage(qimg))

    def display_side_view(self, img: np.ndarray):
        qimg = self.create_preview(img)
        self.label_Image_side.setPixmap(QPixmap.fromImage(qimg))
    
    def display_timelapse_strip(self, strip: np.ndarray, max_display_width: int = 800):
        """
        Affiche une portion de la frise temporelle centrée autour de self.timeline_position.
    
        strip : np.ndarray
            Frise entière (hauteur fixe, largeur variable)
        """
        if strip is None:
            return
    
        max_display_width = self.label_timeline.width()
        
        h, w = strip.shape
    
        # Taille d'une "image" dans la frise (en px)
        image_width = self.timeline_frame_width  # ou fixe à 10 par exemple
        
        # Position du bord droit en px (clampée)
        right_px = int(round(self.timeline_position * image_width))
        right_px = max(0, min(right_px, w))
        
        # Position du bord gauche en px (clampée)
        left_px = max(0, right_px - max_display_width)
        left_px = min(left_px, w)  # si right_px==w et max_display_width> w
    
        # Tronque la frise à la fenêtre visible
        visible_strip = strip[:, left_px:right_px]
        vis_w = visible_strip.shape[1]
    
        # Si la bande est trop petite, on complète à gauche avec du noir
        if vis_w < max_display_width:
            padded = np.zeros((h, max_display_width), dtype=strip.dtype)
            if vis_w > 0 :
                padded[:, -visible_strip.shape[1]:] = visible_strip
            visible_strip = padded
    
        visible_strip = np.ascontiguousarray(visible_strip)
        qimg = self.create_preview(visible_strip)
    
        pixmap = QPixmap.fromImage(qimg)
        scaled = pixmap.scaled(self.label_timeline.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_timeline.setPixmap(scaled)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.strip_mean[self.channel_display] is not None:
            self.display_timelapse_strip(self.strip_mean[self.channel_display])
    
        #################################
        ## Functions for the interface ##
        #################################
        
    def format_time(self, ellapsed_time):
        # Convertir le temps en millisecondes
        ms = int((ellapsed_time - int(ellapsed_time)) * 1000)
        total_seconds = int(ellapsed_time)
    
        # Calculer les heures, minutes et secondes
        hours = total_seconds // 3600
        remaining_seconds = total_seconds % 3600
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
    
        # Retourner le temps formaté
        return f"{hours:02d}h {minutes:02d}min {seconds:02d}s {ms:02d} ms"
        
    def create_preview(self, frame: np.ndarray, zoom = 1):
                
        h , w = frame.shape # get dimensions of the image
        
        #Remove grey value bellow and above a certain value
        frame = np.clip(frame,self.min_grayscale[self.channel_display] , self.max_grayscale[self.channel_display] )
        #Change values between 0 and 255 for displaying
        frame = ((frame - self.min_grayscale[self.channel_display] )* (255/(self.max_grayscale[self.channel_display] - self.min_grayscale[self.channel_display])) ).astype(np.uint8)
        
        h , w = int(h * zoom ) , int (w * zoom)
        
        frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_LINEAR)

        qt_image = QImage(frame.data, w, h, w, QImage.Format_Indexed8)
        qt_image.setColorTable(self.palettes[self.LUT[self.channel_display]])
        return qt_image
    
    
class ChannelProcessor(QObject):
    processed = Signal(dict)  # front, side

    def __init__(self, pixel_shift):
        super().__init__()
        self.pixel_shift = pixel_shift

    @Slot(np.ndarray)
    def process(self, images):
        channel, metadata = images
        deskewed_channel = deskew_numpy(channel, px_shift_y=self.pixel_shift)
        data = {"max_front" : np.max(deskewed_channel, axis = 0),
            "max_side" : np.max(deskewed_channel, axis = 2),
            "mean_front" : mean_projection_ignore_zeros(deskewed_channel, axis=0),
            "mean_side" : mean_projection_ignore_zeros(deskewed_channel, axis=2),
            "metadata" : metadata,
        }
        
        self.processed.emit(data)
        
        
###############################################################################
        
if __name__ == '__main__':
    "To test the window"
    
    # set multidimensional_acquisition importable
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "multidimensional_acquisition"))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        
    from multidimensional_acquisition.main_MDA import MultidimensionalAcquisition

        
    MDA = MultidimensionalAcquisition()
    app = QApplication(sys.argv)
    
    editor = mda_mannager(MDA)
    editor.show()
    editor.start_acquisition()
    sys.exit(app.exec())