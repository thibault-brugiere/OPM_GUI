# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 11:10:19 2025

@author: tbrugiere
"""

import numpy as np

class functions_acquisition():
    
    def calculate_size_Z(scan_range, sample_pixel_size, aspect_ratio, tilt_angle):
        """
        

        Parameters
        ----------
        scan_range :  Float
            Dimension of the total volume (in µm).
        sample_pixel_size : Float
            Size of a pixel of the camera in the sample (in µm).
        aspect_ratio : Int
        
        tilt_angle : Float
            Angle of the lightsheet of the microscope.

        Returns
        -------
        n_steps : Int
            Number of steps per volume.
        step_size : Float
            size of one scan step (in µm).
        scan_range : Float
            Dimension of the total volume (in µm).
        """
        step_size = aspect_ratio * sample_pixel_size / np.sin(tilt_angle)
        n_steps = 1 + int(round(scan_range / step_size))
        scan_range = step_size * (n_steps - 1)
        
        step_size = step_size.item()
        scan_range = scan_range.item()

        return n_steps, step_size, scan_range
    
    def legalize_aspect_ratio(sample_pixel_size, aspect_ratio, tilt_angle):
        """
        Return a value of the aspect ratio that leads to en integer number of
        pixel shift between two images

        Parameters
        ----------
        sample_pixel_size : Float
            Size of a pixel of the camera in the sample (in µm).
        aspect_ratio : Int or Float
            Ratio between the z and x axis of the voxel
        tilt_angle : Float
            Angle of the lightsheet of the microscope.

        Returns
        -------
        aspect_ratio : Float
        
            """
        step = aspect_ratio / np.tan(tilt_angle)
        step = int(np.round(step , 0))
        aspect_ratio = np.tan(tilt_angle) * step
        return aspect_ratio