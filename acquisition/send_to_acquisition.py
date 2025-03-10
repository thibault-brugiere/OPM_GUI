# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 15:22:11 2025

@author: tbrugiere
"""
import json
import os

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
                  'DAQ_CHANNELS' : microscope.daq_channels,
                  }
    
    parameters = {'camera' : camera_parameters,
                  'channel' : channel_parameters,
                  'experiment' : experiment_parameters,
                  'microscope' : microscope_parameters
                  }
    
    config_dir = 'D:/EqSibarita/Python/snoutscopev3-main/config'
    file_path = os.path.join(config_dir, filename)  # filename définit en entrée de la fonction
    
    with open(file_path, 'w') as json_file:
        json.dump(parameters, json_file)

def send_to_multidimensionnal_acquisition(camera_list, channel_list, experiment, microscope, dirname = 'acquisition', filename = 'GUI_parameters.json'):
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

    for camera in camera_list :
        camera_parameters = {'camera_id': camera.camera_id,
                             'subarray_hpos': camera.hpos,
                             'subarray_hsize': camera.hsize,
                             'subarray_vpos': camera.vpos,
                             'subarray_vsize': camera.vsize,
                            }

        cameras.update({f'camera_{camera.camera_id}': camera_parameters})

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

    experiment_parameters = {'ASPECT_RATIO': experiment.aspect_ratio,
                             'SCAN_RANGE_UM': experiment.scan_range,
                             'SLIT_APERTURE': experiment.slit_aperture,
                             'TIME_INTERVAL': experiment.time_intervals,
                             'NUM_TIMEPOINTS': experiment.timepoints,
                             }

    microscope_parameters = {'EXP_NAME': experiment.exp_name,
                             'DATA_PATH': experiment.data_path,
                             'TILT_ANGLE': microscope.tilt_angle,
                             'MAG_TOTAL': microscope.mag_total,
                             'CAMERA_PIXELSIZE': camera.pixel_size,
                             'VOLTS_PER_UM': microscope.volts_per_um,
                             'DAQ_CHANNELS': microscope.daq_channels,
                             }

    parameters = {'cameras': cameras,
                  'channels': channels,
                  'experiment': experiment_parameters,
                  'microscope': microscope_parameters
                  }

    file_path = os.path.join(dirname, filename)  # filename définit en entrée de la fonction

    with open(file_path, 'w') as json_file:
        json.dump(parameters, json_file)