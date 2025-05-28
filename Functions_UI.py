# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 15:50:32 2025

@author: tbrugiere
"""

import cv2
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import os
import re
import subprocess

from PySide6.QtCore import QTime
from PySide6.QtGui import QImage

class functions_ui():
    
    #
    # Saving
    #
    
    def legalize_name(name):
        """
        Ensures the name is correctly formatted (optional).

        Checks if the experiment name is valid:
        - Must not be empty.
        - Must not contain spaces.
        - Must not contain forbidden characters.
        """
        
        forbidden_chars = r'[\\/:*?"<>| ù]'  # Liste des caractères interdits, y compris l'espace

        if re.search(forbidden_chars, name):
            name_ok = False
            NAME = re.sub(forbidden_chars, "_", name)  # Remplace les caractères interdits par '_'
        else:
            name_ok = True
            NAME = name
        
        return name_ok, NAME
    
    def create_directory_if_not_exists(directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    
    #
    # Camera
    #
    
    def generate_camera_indexes(n_camera):
        """
        Generate a list of camera names based on the number of cameras
        to set comboBox options
        
        Parameters:
        - n_camera (int): The number of cameras.
        
        Returns:
        - List[str]: A list of camera names in the format 'camera_1', 'camera_2', etc.
        """
        
        camera_names = [f'camera_{i + 1}' for i in range(n_camera)]
        
        return camera_names
            

    def set_pos(pos,size,chipsize):
        """
    Adjusts the position of a subarray within the camera sensor.
    
    This function ensures that the given position (`pos`) of a subarray respects two constraints:
    1. The position must not exceed the maximum allowed value, which is determined by 
       the difference between the total sensor size (`chipsize`) and the subarray size (`size`).
       If the position is too large, it is set to this maximum value.
    2. The position must be a multiple of 4, as required by the camera constraints.
       If `pos` is not a multiple of 4, it is rounded down to the nearest lower multiple of 4.
    
    Parameters:
    - pos (int): The desired position of the subarray.
    - size (int): The size of the subarray.
    - chipsize (int): The total size of the camera sensor.
    
    Returns:
    - int: The corrected position that meets the constraints.
    """
        if pos >chipsize - size:
            pos = chipsize - size
            
        pos = 4*(math.floor(pos/4))
        
        return(pos)
    
    def set_size(size,chipsize):
        """
        Adjusts the size of a subarray within the camera sensor.
        
        This function ensures that the given subarray size (`size`) of a subarray respects two constraints:
        1. The size must not exceed the total sensor size (`chipsize`).
           If the position is too large, it is set to the total sensor size (`chipsize`).
        2. The size must be a multiple of 4, as required by the camera constraints.
           If `size` is not a multiple of 4, it is rounded down to the nearest lower multiple of 4.
        
        Parameters:
        - size (int): The desired size of the subarray.
        - chipsize (int): The total size of the camera sensor.
        
        Returns:
        - int: The corrected position that meets the constraints.
        """
        if size > chipsize:
            size = chipsize
        size = 4*(math.floor(size/4))
        
        return(size)
    
    #
    # Channels settings
    #
    
    def channel_set_interface(channel_list_interface,channel):
        """
        Configures the interface elements for a given channel based on the provided channel object.
        
        This function updates the state of various UI components defined in the channel_list_interface dictionary
        to reflect the settings of the specified channel. It sets the checkbox states and spinbox values for lasers,
        and updates the filter, camera, and exposure time settings.
        
        Parameters:
        channel_list_interface: A dictionary containing UI elements (checkboxes, spinboxes, etc.) for each channel.
        channel: An object representing the channel with attributes like laser activity, filter, camera, and exposure time.
        """
        for laser in channel_list_interface['checkBox_laser'].keys():
            channel_list_interface['checkBox_laser'][laser].setChecked(channel.laser_is_active[laser])
            channel_list_interface['spinBox_laser_power'][laser].setValue(channel.laser_power[laser])
        
        if channel.filter is not None:
            channel_list_interface['filter'].setCurrentText(channel.filter)
        else:
            channel_list_interface['filter'].setCurrentText('-None-')
        
        channel_list_interface['camera'].setCurrentIndex(channel.camera)
        channel_list_interface['exposure_time'].setValue(channel.exposure_time)
        
    def save_channel_from_interface(channel_list_interface,channel):
        """
        Saves the settings from the interface elements into the specified channel object.
        
        This function updates the channel object's attributes based on the current state of the UI components
        defined in the channel_list_interface dictionary. It retrieves the checkbox states and spinbox values for lasers,
        and updates the filter, camera, and exposure time settings in the channel object.
        
        Parameters:
        channel_list_interface: A dictionary containing UI elements (checkboxes, spinboxes, etc.) for each channel.
        channel: An object representing the channel with attributes to be updated, such as laser activity, filter, camera, and exposure time.
        """
        for laser in channel_list_interface['checkBox_laser'].keys():
            channel.laser_is_active[laser] = channel_list_interface['checkBox_laser'][laser].isChecked()
            channel.laser_power[laser] = channel_list_interface['spinBox_laser_power'][laser].value()
            
        channel.filter = channel_list_interface['filter'].currentText()
        channel.camera = channel_list_interface['camera'].currentIndex()
        channel.exposure_time = channel_list_interface['exposure_time'].value()
    
    #
    # Timelaps settings
    #
    
    def QTime_to_seconds(time):
        """ 
        Convert a QTime object to a duration in seconds.
        
        Args:
            time (QTime): A QTime object containing the time to convert.
        
        Returns:
            float: The total duration in seconds, including milliseconds.
        """
        hours = time.hour()
        minutes = time.minute()
        seconds=time.second()
        milliseconds=time.msec()
        total_seconds = hours * 3600 + minutes * 60 + seconds + 0.001 * milliseconds
        
        return total_seconds
    
    def seconds_to_QTime(seconds):
        """
        Convert a duration in seconds to a QTime object.

        Args:
            seconds (float): The duration in seconds, including fractional parts for milliseconds.

        Returns:
            QTime: A QTime object representing the given duration in hours, minutes, seconds, and milliseconds.
            """
        hours, seconds =  divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        seconds, milliseconds = divmod(seconds, 1)
        milliseconds, _ = divmod(milliseconds, 0.001) #unused variable renamed to "_"
        time=QTime(hours,minutes,seconds,milliseconds)
        
        return time
    
    #
    # Scanner
    #
    
    def label_volume_duration(scan_range, sample_pixel_size, aspect_ratio, tilt_angle,
                              exposure_time, vsize, line_readout_time, galvo_response_time):
        """
        Return a label for the interface containing the number of steps / volume
        as well as the duration of eachvolumes.

        Parameters
        ----------
        scan_range : float
            
        sample_pixel_size : float (µm)
            size of each pixels in the sample
        aspect_ratio : int
            
        tilt_angle : float (°)
            angle of the lightsheet
        exposure_time : float (ms)

        vsize : int
            number of pixels in the vertical size of the camera
        line_readout_time : float (s)
            time to read two lines of the camera 
        galvo_response_time :  (ms)
            time for galvo to move of 1 step

        Returns
        -------
        message : str
        """
        
        step_size = aspect_ratio * sample_pixel_size / np.sin(tilt_angle)
        n_steps = 1 + int(round(scan_range / step_size))
        
        estimated_time = n_steps * (exposure_time + vsize * line_readout_time * 1000 / 2
                                    + galvo_response_time)
        
        message  = f'Number of frames/volume: {str(n_steps)}\n'
        message += f'Step size: {round(step_size,3)}µm\n'
        message += f'Estimated volume duration: {round(estimated_time/1000,3)}s/channel'
        
        return message
    
    #
    # Preview
    #
    
    def show_saturation(frame):
        """
        Convert a grayscale image (uint8) to a colorized image:
        - Black pixels (0) become blue (0, 0, 255).
        - White pixels (255) become red (255, 0, 0).
        - Other pixels remain grayscale (R=G=B=value).
        
        Args:
            frame (np.ndarray): Input grayscale image (uint8).
        
        Returns:
            np.ndarray: Colorized image (h, w, 3) in uint8.
        """
        h, w = frame.shape
    
        # Create an empty RGB image
        color_frame = np.zeros((h, w, 3), dtype=np.uint8)
    
        # Apply grayscale to all pixels (default)
        color_frame[:, :, 0] = frame  # Red channel
        color_frame[:, :, 1] = frame  # Green channel
        color_frame[:, :, 2] = frame  # Blue channel
    
        # Set black pixels (0) to blue (0, 0, 255)
        mask_black = (frame == 0)
        color_frame[mask_black] = [0, 0, 255]
    
        # Set white pixels (255) to red (255, 0, 0)
        mask_white = (frame == 255)
        color_frame[mask_white] = [255, 0, 0]
    
        return color_frame
    
    def create_preview(frame, LUT, min_grayscale, max_grayscale, zoom):
        """
        Processes a grayscale image for preview by adjusting its intensity range and applying optional color mapping.
        
        Parameters:
        - frame (np.ndarray): The input grayscale image.
        - LUT (str): Lookup table selection, used to determine whether to highlight saturated pixels.
        - min_grayscale (int): The minimum grayscale value to consider.
        - max_grayscale (int): The maximum grayscale value to consider.
        - zoom (float) : factor to change the image size before preview (between 0.25 and 2)
        
        Returns:
        - QImage: The processed image, either in grayscale or with a colormap highlighting saturated pixels.
        """
        
        h , w = frame.shape # get dimensions of the image
        
        
        frame = np.clip(frame,min_grayscale , max_grayscale ) #Remove grey value bellow and above a certain value
        # frame = ((frame - min_grayscale ) * coef_grayscale ).astype(np.uint8) #Change values between 0 and 255 for displaying
        frame = ((frame - min_grayscale ) * (255/(max_grayscale - min_grayscale)) ).astype(np.uint8) #Change values between 0 and 255 for displaying
        
        h , w = int(h * zoom ) , int (w * zoom)
        
        frame = cv2.resize(frame, (w, h), interpolation=cv2.INTER_LINEAR)
        
        if  LUT == 'show_saturation':
            color_frame = functions_ui.show_saturation(frame)
            qt_image = QImage(color_frame.data, w, h, w * 3, QImage.Format_RGB888)
        elif LUT == 'grayscale':
            qt_image = QImage(frame.data, w, h, w, QImage.Format_Grayscale8) #create the QT image
        
        return qt_image
        
    def create_gray_hystogram(frame, min_grayscale=10000, max_grayscale=50000,
                              w_px = 1200, h_px=600, dpi=100, line_width=1, font_size=12):
        """Generate a histogram of the grayscale image and display it in a QGraphicsView.
        
        Args:
            frame (ndarray): 16-bit grayscale image.
            w_px (int): Desired width in pixels.
            h_px (int): Desired height in pixels.
            dpi (int): Resolution in dots per inch.
            line_width (int): Thickness of the histogram line.
            font_size (int): Size of the font for axis labels and ticks.
        """
        
        hist, bins = np.histogram(frame, bins=256, range=(0, 65535))
    
        # Création du graphique
        fig = plt.Figure(figsize=(w_px / dpi, h_px / dpi), dpi=dpi)
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        
        # Tracé de l'histogramme
        ax.plot(bins[:-1], hist, color="black", linewidth=line_width)
        ax.set_xlim(0, 65535)
        
        # Set font size for axes labels and ticks
        ax.tick_params(axis='both', which='major', labelsize=font_size)
        ax.set_xlabel('Gray Value', fontsize=font_size)
        ax.set_ylabel('Frequency', fontsize=font_size)
        
        # Ajoute les position des min et max gray value
        ax.axvline(x=min_grayscale, color='red', linestyle='--', linewidth=line_width)
        ax.axvline(x=max_grayscale, color='blue', linestyle='--', linewidth=line_width)
        
        ax.set_yticklabels([])
        
        # Convertir directement en QPixmap
        canvas.draw()
        w, h = canvas.get_width_height()
        image_data = np.frombuffer(canvas.buffer_rgba(), dtype=np.uint8).reshape(h, w, 4)

        qimage = QImage(image_data, w, h, w * 4, QImage.Format_RGBA8888)
        
        return qimage
    
    #
    # Acquisition
    #
    
    def start_snoutscope_acquisition(file_path, working_directory) :
        """
        Lance un fichier Python en utilisant subprocess.
        
        Parameters:
        - file_path (str): Le chemin vers le fichier Python à exécuter.
        """
        try:
            # Exécuter le fichier Python
            subprocess.run(["python", file_path],
                           check=True, text=True,
                           capture_output=True,
                           cwd=working_directory)
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution du fichier : {e}")
            print("Return code:", e.returncode)
            print("Output:", e.stdout)
            print("Error:", e.stderr)

    def get_active_channel(active_channels, channel):
        channel_acquisition = []
        for channel_name in active_channels :
            if channel_name != 'None' :
                channel_acquisition.append(channel[channel_name])
            else:
                print('None channel detected')

        return channel_acquisition

    def start_multidimensional_acquisition(file_path):
        pass

    
    #
    # General functions
    #
    
    def set_comboBox (combo,options_list,index=0):
        """
        Updates the given combo box with a new list of options.
    
        This function clears the current items in the combo box, replaces them with the provided
        options list, and set the selection to the choosen item. Signals are temporarily blocked
        to prevent triggering connected functions during the update.
    
        Parameters:
        - combo (QComboBox): The combo box to update.
        - options_list (list of str): The list of new options to populate the combo box.
        - index (int or str): choosen item or index to select (default = 0)
        """
        combo.blockSignals(True) #blocks signals from `comboBox_camera` while updating its items 
                                                    #to prevent unwanted signal emissions.
        combo.clear()
        combo.addItems(options_list)
        
        try:
            if type(index)==int:
                combo.setCurrentIndex(index)
            elif type(index)==str:
                combo.setCurrentText(index)
        except:
            combo.setCurrentIndex(0)
                    
                    
        combo.blockSignals(False)
