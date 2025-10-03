# -*- coding: utf-8 -*-
"""
Created on Fri Oct  3 10:01:31 2025

@author: tbrugiere
"""

def microscope_settings_to_dict(microscope):
    
    microscope_dict = {
        "tilt_angle" : microscope.tilt_angle,
        "mag_total" : microscope.mag_total,
        # scanning galvo
        "volts_per_um" : microscope.volts_per_um,
        "galvo_response_time" : microscope.galvo_response_time,  # A mesure in ms
        "galvo_flyback_time" : microscope.galvo_flyback_time, # A mesurer in ms
        
        # stage
        "stage_port" : microscope.stage_port,
        
        # Filters
        "filter_changing_time" : microscope.filter_changing_time, # in ms
        "filters" : microscope.filters, #should be 6 options
        
        # Lasers
        "lasers" : microscope.lasers, # ["405","488","561","640"]
        "volts_per_laser_percent" : microscope.volts_per_laser_percent, # 5v max
        "laser_response_time" : microscope.laser_response_time, # in ms
        "OxxiusCombiner_port" : microscope.OxxiusCombiner_port,
        "OxxiusCombiner_command" : microscope.OxxiusCombiner_command,
        
        # NiDAQ
        "daq_channels" : microscope.daq_channels,
        "daq_channels_laser_analog_out" : microscope.daq_channels_laser_analog_out,
        "daq_channels_laser_digital_out" : microscope.daq_channels_laser_digital_out
        }
    
    return microscope_dict
    
def dict_to_microscope_settings(microscope, microscope_dict):

    microscope.tilt_angle = microscope_dict["tilt_angle"]
    microscope.mag_total = microscope_dict["mag_total"]
    microscope.volts_per_um = microscope_dict["volts_per_um"]
    microscope.galvo_response_time = microscope_dict["galvo_response_time"]
    microscope.galvo_flyback_time = microscope_dict["galvo_flyback_time"]
    microscope.stage_port = microscope_dict["stage_port"]
    microscope.filter_changing_time = microscope_dict["filter_changing_time"]
    microscope.filters = microscope_dict["filters"]
    microscope.lasers = microscope_dict["lasers"]
    microscope.volts_per_laser_percent = microscope_dict["volts_per_laser_percent"]
    microscope.laser_response_time = microscope_dict["laser_response_time"]
    microscope.OxxiusCombiner_port = microscope_dict["OxxiusCombiner_port"]
    microscope.OxxiusCombiner_command = microscope_dict["OxxiusCombiner_command"]
    microscope.daq_channels = microscope_dict["daq_channels"]
    microscope.daq_channels_laser_analog_out = microscope_dict["daq_channels_laser_analog_out"]
    microscope.daq_channels_laser_digital_out = microscope_dict["daq_channels_laser_digital_out"]
    
    return microscope
    
    
    