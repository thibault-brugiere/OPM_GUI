# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 16:30:29 2025

@author: tbrugiere

pyside6-uic widget/ui_ls3.ui -o widget/ui_ls3.py
"""
from collections import deque
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

from image_analysis.Deskew_Numpy import deskew_numpy, compute_px_shift
from LS3_acquisition.Live_Viewer.ls3_manager_functions import auto_contrast
from LS3_acquisition.Live_Viewer.ls3_manager_functions import LookUpTables
from LS3_acquisition.Live_Viewer.ls3_manager_functions import create_ls3_image, add_image, crop_zoom_image

from widget.ui_ls3 import Ui_Form


# TODO : ajouter le zoom dans l'interface
# TODO : ajouterun cache 8 bits pour la navigation

class ls3_mannager(QWidget, Ui_Form):
    """
    Show the window to follow rhe multidimensionnal acquisition.
    """
    channel_received = Signal(tuple)
    
    def __init__(self, ls3, parent=None, max_preview_size = 2):
        
        super().__init__(parent)
        self.setupUi(self)
        self.ls3 = ls3
        self.max_preview_size = max_preview_size # Maximum size of preview image in gigabite 
        self.on_init()
        
    def on_init(self):
        
        self.setWindowTitle('Multidimensionnal Acquisition')
        self.setWindowFlag(Qt.Window) 
        
        
        ###############################
        ## Creation of the Variables ##
        ###############################
        
        # -------------------------------
        # "Latest-only" preview pipeline
        # -------------------------------
        # We keep at most ONE pending volume (the latest received).
        # If processing is busy when a new volume arrives, the older pending one is dropped.
        self._pending_lock = threading.Lock()
        self._pending_payload = None      # type: tuple[np.ndarray, dict] | None
        self._dropped_meta = deque()      # store metadata of dropped items for UI placeholders
        self._processor_busy = False      # guarded by lock usage pattern (UI thread only writes it)
        
        # Count dropped preview volumes (debug / UI info)
        self.preview_dropped = 0
        
        # Maximum volume size allowed for live processing (bytes).
        # Volumes larger than this are dropped (black placeholder in timeline).
        self.max_preview_bytes = int(self.max_preview_size * 1024**3)  # 2 GiB
        self.preview_message = "Displaying live preview"
        self.button_message = ""
    
        
        self.info_timer = QTimer() # Timer to update informations
        self.info_timer.timeout.connect(self.update_infos) # Connected to update informations
        
        #
        # Values for displaying, calculation
        #
        
        self.total_timepoints = self.ls3.config.experiment.timepoints
        self.total_images = self.total_timepoints * self.ls3.config.experiment.n_steps * len(self.ls3.config.channels)
        self.total_channels = len(self.ls3.config.channels)
        self.channel_names = [ch.channel_id for ch in self.ls3.config.channels]
        self.channel_display = self.channel_names[0]
        
        self._cb_image_channel_set()
        
        self.images_acquired = 0
        self.frames_acquired = 0
        self.frames_dropped = 0
        self.channel_saved = 0
        self.volumes_recived = 0
        
            # Pixel shift between two images of the volume for deskewing
        self.pixel_shift = compute_px_shift(self.ls3.config.experiment.aspect_ratio,
                                            self.ls3.config.microscope.tilt_angle,
                                            unit = "deg")
        
        self.ellapsed_time = time.time()
        
        #
        # Images to display
        #
        
        self.create_preview_image()
        
        #
        # Values for the interface
        #
        
        self.LUT = {key : "Grayscale" for key in self.channel_names}
        self.min_grayscale = {key : 0 for key in self.channel_names}
        self.max_grayscale = {key : 65535 for key in self.channel_names}
        
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
        
        self.cb_lut.currentIndexChanged.connect(self.cb_lut_index_changed)
        # self.sb_image_zoom.currentValueChanged.connect(self.sb_image_zoom_value_changed) # TODO à corriger ici
        
        self.cb_image_channel.currentIndexChanged.connect(self.cb_image_channel_index_changed)
        
        self.pb_grayscale_min_max.clicked.connect(self.pb_grayscale_min_max_clicked)
        self.pb_grayscale_auto.clicked.connect(self.pb_grayscale_auto_clicked)
        self.pb_grayscale_reset.clicked.connect(self.pb_grayscale_reset_clicked)
        self.sb_grayscale_min.valueChanged.connect(self.sb_grayscale_value_changed)
        self.sb_grayscale_max.valueChanged.connect(self.sb_grayscale_value_changed)
        
        self.slider_x_position.valueChanged.connect(self.slider_x_position_value_changed)
        self.slider_y_position.valueChanged.connect(self.slider_y_position_value_cganged)
        self.label_mainImage.wheelScrolled.connect(self.label_mainImage_scrolled)
        
        self.pb_stop.clicked.connect(self.pb_stop_clicked)
        self.pb_hold.clicked.connect(self.pb_hold_clicked)
        self.pb_pause.clicked.connect(self.pb_pause_clicked)
        
        # Make the preview image updating only after the user finished the change
        self.update_preview_timer = QTimer(self)
        self.update_preview_timer.setSingleShot(True)
        self.update_preview_timer.timeout.connect(self.update_preview)
        
        
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
        
    def cb_lut_index_changed(self):
        self.LUT[self.channel_display] = self.cb_lut.currentText()
        self.update_preview()
        
    def image_zoom_value_changed(self):
        self.update_preview_timer.start(50)
        
    def cb_image_channel_index_changed(self):
        self.channel_display = self.cb_image_channel.currentText()
        self._set_interface_channel()
        self.update_preview()

    def pb_grayscale_min_max_clicked(self):
            self.slider_grayscale_min.setValue(np.min(self.preview_images[self.channel_display]))
            self.slider_grayscale_max.setValue(np.max(self.preview_images[self.channel_display]))
            
            # image = self.preview_images[self.channel_display]

            # min_val = np.min(image)
            # max_val = np.max(image)
            
            # print(type(min_val), min_val)
            # print(type(max_val), max_val)
            
            # self.slider_grayscale_min.setValue(int(min_val))
            # self.slider_grayscale_max.setValue(int(max_val))
                
    def pb_grayscale_auto_clicked(self):
        if self.preview_images[self.channel_display] is not None :
            min_gray, max_gray = auto_contrast(self.preview_images[self.channel_display])
                
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
            
        self.update_preview_timer.start(50)
        
    def slider_x_position_value_changed(self):
        self.update_preview_timer.start(50)
    
    def slider_y_position_value_cganged(self):
        self.update_preview_timer.start(50)
        
    def label_mainImage_scrolled(self, delta, x, y):
        print(f'{delta} {x} {y}')
            
    def pb_stop_clicked(self):
        self.ls3.stop_all()
        
    def pb_hold_clicked(self):
        self.button_message = "Hold button hasen't been implemented yet"
    
    def pb_pause_clicked(self):
        self.button_message = "Pause button hasen't been implemented yet"
        
        ###########################################
        ## Functions for displaying informations ##
        ###########################################
        
    def start_acquisition(self):
        self.ls3.initialize_cameras()
        self.ls3.initialize_laser()
        self.ls3.initialize_filterwheel()
        self.ls3.configure_daq()
        self.ls3.configure_stage()
        self.ls3.initialize_acquisition_workers()
        # self.ls3.initialize_count_worker() # TODO ajouter le count_worker
        self.set_controller()
        
        # Lancer l'acquisition dans un thread à part
        threading.Thread(target=self.ls3.run_acquisition, daemon=True).start()
        self.info_timer.start(100)
        
        #
        # Get informations and update the progress bar
        #
        
    def update_infos(self):
        # try:
        if self.ls3.acquisition_workers[0].start_time is not None :
            if self.ls3.state["daq"] == "idle":
                pass
            else:
                self.ellapsed_time = time.time() - self.ls3.acquisition_workers[0].start_time
        else:
            self.ellapsed_time = 0
        # except:
        #     return
            
        self.images_acquired = self.ls3.acquisition_workers[0].total_images
        self.frames_acquired = self.ls3.acquisition_workers[0].total_frames
        self.frames_dropped = self.ls3.acquisition_workers[0].total_dropped
        self.channels_saved = self.ls3.acquisition_workers[0].total_volumes
        self.label_informations.setText(f"""
Camera : {self.ls3.state["camera"]}, DAQ : {self.ls3.state["daq"]}
Frames Acquired: {self.frames_acquired}/{self.total_images}
Frames Dropped: {self.frames_dropped}/{self.total_images}
Channels Saved: {self.channels_saved}/{self.total_timepoints * self.total_channels}
Volumes Recived: {self.volumes_recived}
Time Ellapsed: {self.format_time(self.ellapsed_time)} s

Preview volumes dropped: {self.preview_dropped}
{self.preview_message}
{self.button_message}
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
        Connect the main acquisition worker to the GUI preview.
        """
        worker = self.ls3.acquisition_workers[0]
        worker.new_volume_ready.connect(self.handle_new_channel)
        worker.set_preview_callback()
        
    def handle_new_channel(self, channel: np.ndarray, metadata: dict):
        """
        Receive a new 3D volume from the acquisition thread.
    
        IMPORTANT:
        - This slot runs in the GUI thread (Qt queued connection).
        - We MUST avoid accumulating volumes here, otherwise RAM explodes.
        - Strategy: keep only the latest pending volume (max 1), drop older pending.
        """
        self.volumes_recived = metadata["volume_id"]
        self.update_infos()
        
        # -----------------------------
        # Safety guard: size-based drop
        # -----------------------------
        nbytes = self._volume_nbytes(channel)
        if nbytes >= self.max_preview_bytes:
            # Drop immediately: too risky to deskew / process in RAM.
            self.preview_dropped += 1
            self.preview_message = f"Preview skipped: volume size {nbytes/1024**3:.1f} GiB exceeds limit ({self.max_preview_bytes/1024**3:.1f} GiB)"
        
            # Add one black placeholder to timeline (debug-friendly).
            # We append to "dropped meta" queue so placeholders appear on next processed frame.
            with self._pending_lock:
                self._dropped_meta.append(metadata)
        
            return
        else:
            self.preview_message = "Displaying live preview"
    
        with self._pending_lock:
            # If there is already a pending volume waiting for processing, we drop it.
            # We keep its metadata to create a "black placeholder" in the timeline.
            if self._pending_payload is not None:
                dropped_vol, dropped_meta = self._pending_payload
                self._dropped_meta.append(dropped_meta)
                self._pending_payload = None
                self.preview_dropped += 1
    
            # Store the latest payload (channel volume + metadata)
            self._pending_payload = (channel, metadata)
            
        # Try to start processing if the worker thread is idle
        self._try_dispatch_processing()
        
    def _volume_nbytes(self, vol: np.ndarray) -> int:
        """
        Return the memory footprint in bytes of a numpy array.
    
        Notes
        -----
        - For a contiguous ndarray, nbytes is the true payload size.
        - For views, nbytes reflects the view's element count * itemsize,
          not necessarily the base allocation. In practice your volumes are contiguous.
        """
        try:
            return int(vol.nbytes)
        except Exception:
            # Fallback if something weird is passed
            return 0
        
    def _try_dispatch_processing(self):
        """
        Dispatch one pending volume to the processing thread if it is idle.
    
        We never send more than one volume at a time to the processing thread.
        This prevents Qt queued signals from piling up with huge ndarray payloads.
        """
        # Only the GUI thread should call this method.
        if self._processor_busy:
            return
    
        with self._pending_lock:
            if self._pending_payload is None:
                return
            payload = self._pending_payload
            self._pending_payload = None
    
        # Mark busy BEFORE emitting (avoid race if another volume arrives immediately)
        self._processor_busy = True
        self.channel_received.emit(payload)  # queued to ChannelProcessor thread
    
        # Drain dropped meta queue
        drained = 0
        with self._pending_lock:
            while self._dropped_meta:
                _ = self._dropped_meta.popleft()
                drained += 1
    
        if drained == 0:
            return
        
    def receive_projections(self, data):
        # Update UI preview
        self.update_image(data)
    
        # Mark processor idle and immediately process the latest pending volume (if any)
        self._processor_busy = False
        self._try_dispatch_processing()
        
        self.update_preview()
        
    def update_preview(self):
        qimg = self.create_qimage()
        self.label_mainImage.setPixmap(QPixmap.fromImage(qimg))
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.label_mainImage is not None :
                self.update_preview_timer.start(50)
    
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
    
    def create_preview_image(self):
        preview_image, self.px_shift, self.scanV_overlap_px = create_ls3_image(self.ls3)
        self.preview_images = {key: preview_image.copy() for key in self.channel_names}
    
    def update_image(self, data):
        
        channel = data["metadata"]["channel"]
            
        self.preview_images[channel] = add_image(self.preview_images[channel],
                                                        data["max_front"],
                                                        data["metadata"],
                                                        self.px_shift,
                                                        self.scanV_overlap_px)

    def create_qimage(self):
        h_label = self.label_mainImage.height()
        w_label = self.label_mainImage.width()
        
        #Remove grey value bellow and above a certain value
        frame = np.clip(self.preview_images[self.channel_display], self.min_grayscale[self.channel_display] , self.max_grayscale[self.channel_display] )

        #Change values between 0 and 255 for displaying

        frame = ((frame - self.min_grayscale[self.channel_display] )* (255/(self.max_grayscale[self.channel_display] - self.min_grayscale[self.channel_display])) ).astype(np.uint8)
        frame = crop_zoom_image(frame, # Create the image fitting in the window
                                self.slider_x_position.value(),
                                100 - self.slider_y_position.value(), # To inverse the axis
                                0.1, #self.sb_image_zoom.value() / 100, # TODO rempler ici quand la sb sera bonne
                                h_label,
                                w_label)
        
        qt_image = QImage(frame.data, w_label, h_label, w_label, QImage.Format_Indexed8)
        qt_image.setColorTable(self.palettes[self.LUT[self.channel_display]])
        return qt_image.copy()
    
    
class ChannelProcessor(QObject):
    processed = Signal(dict)

    def __init__(self, pixel_shift):
        super().__init__()
        self.pixel_shift = pixel_shift

    @Slot(np.ndarray)
    def process(self, images):
        channel, metadata = images
        deskewed_channel = deskew_numpy(channel, px_shift_y=self.pixel_shift)
        data = {"max_front" : np.max(deskewed_channel, axis = 0),
                "metadata" : metadata,
                }
        
        self.processed.emit(data)
        
"""
metadata = {
    "file_id" : file_id,
    "volume_id": volume_id,
    "channel": current_channel,
    "shape": current_buffer.shape
}
"""
        
        
###############################################################################
        
if __name__ == '__main__':
    "To test the window"
    
    # set multidimensional_acquisition importable
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "multidimensional_acquisition"))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        
    from LS3_acquisition.main_LS3 import Light_sheet_stabilized_scanning

        
    LS3 = Light_sheet_stabilized_scanning()
    app = QApplication(sys.argv)
    
    editor = ls3_mannager(LS3)

    editor.show()
    
    editor.start_acquisition()
    sys.exit(app.exec())