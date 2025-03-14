# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 15:22:11 2025

@author: tbrugiere
"""
import json
import os
from .functions_acquisition import functions_acquisition as fa

def send_to_snoutscope_acquisition(camera, channel, experiment, microscope, filename='GUI_parameters.json'):
    """
    Save parameters in a fichier JSON file.
    
    Parameters:
    - camera : parameters of the first camera of the system, as define in config.py, modified from UI
    - channel : paremeters of the fisrt active channel in the interface, as define in config.py, modified from UI
    - experiment: parameters of the experiment, as define in config.py, modified from UI
    - microscope : parameters of the microscope, as define in config.py, modified from UI
    - filename (str): Nom du fichier JSON.
    """
    # Permet d'ajuster le pourcentage de laser à la tension nécessaire au DAC
    for laser in channel.laser_power.keys():
        channel.laser_power[laser] = channel.laser_power[laser] * microscope.volts_per_laser_percent[laser]
    
    camera_parameters = {'camera_id' : camera.camera_id,
              'subarray_hpos' : camera.hpos,
              'subarray_hsize' : camera.hsize,
              'subarray_vpos' : camera.vpos,
              'subarray_vsize' : camera.vsize,
              'line_readout_time' : camera.line_readout_time
              }
    
    channel_parameters = {'channel_id' : channel.channel_id,
               'is_active' : True,
               'camera' : channel.camera,
               'exposure_time' : channel.exposure_time,
               'laser_is_active' : channel.laser_is_active,
               'laser_power' : channel.laser_power,
                }
    
    experiment_parameters = {'ASPECT_RATIO' : experiment.aspect_ratio,
                  'SCAN_RANGE_UM' : experiment.scan_range,
                  'SLIT_APERTURE' : experiment.slit_aperture,
                  'TIME_INTERVAL' : experiment.time_intervals,
                  'NUM_TIMEPOINTS' : experiment.timepoints,
                  }
    
    microscope_parameters = {'EXP_NAME' : experiment.exp_name,
                  'DATA_PATH' : experiment.data_path,
                  'TILT_ANGLE' : microscope.tilt_angle,
                  'MAG_TOTAL' : microscope.mag_total,
                  'CAMERA_PIXELSIZE' : camera.pixel_size,
                  'VOLTS_PER_UM' : microscope.volts_per_um,
                  'GALVO_RESPONSE_TIME' : int(microscope.galvo_response_time * 1000), # should be in µs
                  'GALVO_FLYBACK_TIME' : int(microscope.galvo_flyback_time * 1000), # should be in µs
                  'DAQ_CHANNELS' : microscope.daq_channels,
                  }
    
    parameters = {'camera' : camera_parameters,
                  'channel' : channel_parameters,
                  'experiment' : experiment_parameters,
                  'microscope' : microscope_parameters
                  }
    
    config_dir = 'snoutscopev3/config'
    file_path = os.path.join(config_dir, filename)  # filename définit en entrée de la fonction
    
    with open(file_path, 'w') as json_file:
        json.dump(parameters, json_file, indent = 4)

def send_to_multidimensionnal_acquisition(camera_list, channel_list, experiment, microscope,
                                          dirname = 'acquisition', filename = 'GUI_parameters.json'):
    """
    Save parameters in a fichier JSON file.

    Parameters:
    - camera_list : parameters of the first camera of the system, as define in config.py, modified from UI
    - channel_list : paremeters of the fisrt active channel in the interface, as define in config.py, modified from UI
    - experiment: parameters of the experiment, as define in config.py, modified from UI
    - microscope : parameters of the microscope, as define in config.py, modified from UI
    - dirname (str) : folder where the file is saved
    - filename (str): Nom du fichier JSON.
    """

    cameras = {}
    channels = {}
    
    #
    # Cameras
    #

    for camera in camera_list :
        camera.sample_pixel_size = camera.pixel_size / microscope.mag_total
        
        camera_parameters = {'camera_id': camera.camera_id,
                             'subarray_hpos': camera.hpos,
                             'subarray_hsize': camera.hsize,
                             'subarray_vpos': camera.vpos,
                             'subarray_vsize': camera.vsize,
                             'sample_pixel_size' : camera.sample_pixel_size,
                             'line_readout_time' : camera.line_readout_time
                            }

        cameras.update({f'camera_{camera.camera_id}': camera_parameters})
        
    #
    # Channels
    #

    for channel in channel_list :
        # Permet d'ajuster le pourcentage de laser à la tension nécessaire au DAC
        for laser in channel.laser_power.keys():
            channel.laser_power[laser] = channel.laser_power[laser] * microscope.volts_per_laser_percent[laser]

        channel_parameters = {'channel_id': channel.channel_id,
                              'is_active': True,
                              'camera': channel.camera,
                              'exposure_time': channel.exposure_time,
                              'laser_is_active': channel.laser_is_active,
                              'laser_power': channel.laser_power,
                              }
        channels.update({f'channel_{channel.channel_id}': channel_parameters})
        
    #
    # Experiment
    #
    
    experiment.n_steps, experiment.step_size, experiment.scan_range = fa.calculate_size_Z(experiment.scan_range,
                                                                                          camera_list[0].sample_pixel_size,
                                                                                          experiment.aspect_ratio,
                                                                                          microscope.tilt_angle)
    experiment_parameters = {'aspect_ration': experiment.aspect_ratio,
                             'scan_range': experiment.scan_range,
                             'slit_aperture': experiment.slit_aperture,
                             'time_intervals': experiment.time_intervals,
                             'num_timepoints': experiment.timepoints,
                             'n_steps' : experiment.n_steps,
                             'step_size' : experiment.step_size
                             }
    
    #
    # Mocroscope
    #

    microscope_parameters = {'exp_name': experiment.exp_name,
                             'data_path': experiment.data_path,
                             'tilt_angle': microscope.tilt_angle,
                             'mag_total': microscope.mag_total,
                             'camera_pixelsize': camera.pixel_size,
                             'volts_per_um': microscope.volts_per_um,
                             'galvo_response_time' : microscope.galvo_response_time,
                             'galvo_flyback_time' : microscope.galvo_flyback_time,
                             'laser_response_time' : microscope.laser_response_time,
                             'daq_channels': microscope.daq_channels,
                             }
    #
    # Final dictionnary
    #

    parameters = {'cameras': cameras,
                  'channels': channels,
                  'experiment': experiment_parameters,
                  'microscope': microscope_parameters
                  }

    #
    # Saving
    #

    file_path = os.path.join(dirname, filename)  # filename définit en entrée de la fonction

    with open(file_path, 'w') as json_file:
        json.dump(parameters, json_file, indent=4)