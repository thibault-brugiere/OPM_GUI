# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 14:25:14 2025

@author: tbrugiere
"""
from pylablib.devices import DCAM

class camera_acquisition():
    """
    Handles the initialization, configuration, and control of a Hamamatsu camera 
    using the DCAM interface (pylablib). 
    
    Supports sequence acquisition mode triggered externally by a DAQ device.
    
    Attributes
    ----------
    camera : object
        Camera configuration object from config.
    hcam : DCAMCamera or None
        Low-level camera object from pylablib (initialized by initialize_camera()).
    state : str
        Current state of the camera: 'idle', 'initialized', 'configured', or 'acquiring'.
    """
    
    def __init__(self, camera, hcam = None, channels=None, experiment=None, microscope=None):
        """
        Initialize the camera acquisition.
        
        Parameters
        ----------
        camera : object
            Camera config object loaded from configuration.
        hcam : DCAMCamera or None
            Optional pre-initialized camera object.
        others parameters are only needed for simulation
        """
        
        self.camera = camera
        self.hcam = hcam
        
        self.state = "idle"
        if self.hcam is not None :
            self.state = "initialized"   
        
    def initialize_camera(self):
        """
        Connects to the hardware camera and checks that hardware parameters 
        match the config object. Applies corrections if mismatches are found.
        """
        
        if self.hcam is not None:
            raise RuntimeError("Camera already initialized")
            
        self.hcam = DCAM.DCAMCamera(self.camera.camera_id)
        
        # Get hardware parameters
        hchipsize, vchipsize = self.hcam.get_detector_size()
        pixel_size = self.hcam.get_attribute_value('image_detector_pixel_width')
        line_readout_time = self.hcam.get_attribute_value('internal_line_interval')
        
        errors = []
        
        # Check chip size
        if self.camera.hchipsize != hchipsize:
            errors.append(f"Corrected hchipsize: {self.camera.hchipsize} → {hchipsize}")
            self.camera.hchipsize = hchipsize
        if self.camera.vchipsize != vchipsize:
            errors.append(f"Corrected vchipsize: {self.camera.vchipsize} → {vchipsize}")
            self.camera.vchipsize = vchipsize
            
        # Check pixel size
        if abs(self.camera.pixel_size - pixel_size) > 1e-3:
            errors.append(f"Corrected pixel size: {self.camera.pixel_size} → {pixel_size}")
            self.camera.pixel_size = pixel_size
    
        # Check line readout time
        if abs(self.camera.line_readout_time - line_readout_time) > 1e-3:
            errors.append(f"Corrected line readout time: {self.camera.line_readout_time} → {line_readout_time}")
            self.camera.line_readout_time = line_readout_time
            # Check and legalize ROI
        corrected = self.legalize_roi()
        if corrected:
            errors.extend(corrected)
            
        if errors:
            print("(!) Camera parameters were not matching hardware and have been corrected:")
            for e in errors:
                print("   -", e)
                
        self.state = "initialized"
    
    def configure_camera_for_acquisition(self):
        """
        Configures the hardware camera using values from the config object.
        Includes subarray (ROI), exposure time, binning, and external trigger mode.
        """
        
        if self.hcam is None:
            raise RuntimeError("Camera is not initialized. Call initialize_camera() first.")

        # Set subarray mode (cropped acquisition)
        self.hcam.cav["SUBARRAY MODE"] = 2
        
        # Exposure and binning
        self.hcam.cav["EXPOSURE TIME"] = self.camera.exposure_time
        self.hcam.cav["binning"] = self.camera.binning
        
        # Avoid invalid ROI by setting pos before size
        self.hcam.cav["subarray_hpos"] =  0 # Needed to avoid "INVALIDSUBARRAY"
        self.hcam.cav["subarray_vpos"] =  0 # Needed to avoid "INVALIDSUBARRAY"
        
        self.hcam.cav["subarray_hsize"] = self.camera.hsize
        self.hcam.cav["subarray_vsize"] = self.camera.vsize
        self.hcam.cav["subarray_hpos"] =  self.camera.hpos
        self.hcam.cav["subarray_vpos"] =  self.camera.vpos
        
        # Trigger settings
        self.hcam.cav["trigger_source"] = 2 # 1=internal, 2=external, 3=software, 4=master pulse
        self.hcam.cav["trigger_mode"] = 1 # 1=normal, 2=start
        self.hcam.cav["trigger_active"] = 2 # 1=edge, 2=level, 3=syncreadout
        # self.hcam.cav["trigger_global_exposure"] = 1 # 1=delayed, 2=global reset
        # self.hcam.cav["trigger_time"] = 1 # in µs
        self.hcam.cav["trigger_polarity"] = 2 # 1=negative, 2=positive
        self.hcam.cav["trigger_delay"] = 0 # in µs
        
        self.state = "configured"
        self.read_count = 0
        
    def start_acquisition(self):
        """
        Starts a sequence acquisition on the camera.
        Camera must be configured before this call.
        """
        
        if self.state != "configured" :
            raise RuntimeError("Camera not configured. Call configure_camera_for_acquisition() first.")
            
        self.hcam.setup_acquisition(mode='sequence',nframes=1000)
        self.hcam.start_acquisition()
        
        self.state = "acquiring"
        
    def stop_acquisition(self):
        """
        Stops acquisition and clears camera buffers.
        Camera must be in acquiring state.
        """
        
        if self.state != "acquiring" :
            raise RuntimeError("Camera not initialized. Call initialize_camera() first.")
        
        self.hcam.clear_acquisition() # Not using stop_acquisition beacause it doesn't relese buffer
        
        self.state = "configured"
        
    def release_camera(self):
        """
        Fully releases the camera and resets the state to idle.
        """
        if self.hcam is not None:
            self.hcam.close()
            self.hcam = None
            self.state = "idle"

    def read_camera(self):
        """
        Reads all available images from the camera buffer.
        Returns empty list if no image is available.
        """
        
        if self.state != "acquiring":
            # raise RuntimeError("Camera not acquiring. start acquisition first.")
            return []
            
        try:
            images = self.hcam.read_multiple_images()
            self.read_count = self.read_count + len(images)
            if len(images) > 0 :
                pass
                # print(f"[CAMERA] total read: {self.read_count} images", end='\r')
            return images  # Can be an empty list if no images available yet
        except Exception as e:
            print(f"Error reading from camera: {e}")
            return []
        
    def legalize_roi(self):
        """
        Validates and corrects the ROI (region of interest) to stay within chip bounds.
        
        Returns
        -------
        list of str
            List of corrections that were made.
        """
        
        corrections = []
    
        if self.camera.hpos + self.camera.hsize > self.camera.hchipsize:
            new_hpos = max(0, self.camera.hchipsize - self.camera.hsize)
            corrections.append(f"Corrected hpos: {self.camera.hpos} → {new_hpos}")
            self.camera.hpos = new_hpos
        
        if self.camera.vpos + self.camera.vsize > self.camera.vchipsize:
            new_vpos = max(0, self.camera.vchipsize - self.camera.vsize)
            corrections.append(f"Corrected vpos: {self.camera.vpos} → {new_vpos}")
            self.camera.vpos = new_vpos
    
        if self.camera.hsize > self.camera.hchipsize:
            corrections.append(f"Corrected hsize: {self.camera.hsize} → {self.camera.hchipsize}")
            self.camera.hsize = self.camera.hchipsize
    
        if self.camera.vsize > self.camera.vchipsize:
            corrections.append(f"Corrected vsize: {self.camera.vsize} → {self.camera.vchipsize}")
            self.camera.vsize = self.camera.vchipsize
    
        return 
    
    def get_image_shape(self):
        hstart, hend, vstart, vend, hbin, vbin = self.hcam.get_roi()
        hsize = (hend - hstart) // hbin
        vsize = (vend - vstart) // vbin
        
        return vsize, hsize