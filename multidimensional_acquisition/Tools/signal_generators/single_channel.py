# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 10:45:10 2025

@author: tbrugiere
"""
import numpy as np
import matplotlib.pyplot as plt
 
def generate_single_channel_signals(cameras, channels, experiment, microscope, frequency = 1e4):
    """
    Generate voltage and logic signals required to control a single-channel, single-camera
    volume acquisition with a microscope.

    The function simulates one volumetric acquisition, which includes:
        1) Laser activation
        2) Galvo positioning (with response time and flyback delay)
        3) Camera exposure
        4) Camera readout
        5) Step repetition for each plane
        6) Galvo return to 0 and laser deactivation

    Signals are returned as time-resolved arrays sampled at the given frequency. These signals
    control galvanometer motion, laser modulation, camera triggering, and blanking.

    Parameters
    ----------
    cameras : list of camera objects
        A list of camera configurations. The relevant camera is selected via the `channels[0].camera` index.
        Each camera object should include:
            - image_readout_time (float): time to read one image, in seconds.

    channels : list of channel_config objects
        The imaging channels. Only the first channel (channels[0]) is used.
        Each channel must define:
            - camera (int): index of the associated camera in `cameras`.
            - exposure_time (float): camera exposure time in milliseconds.
            - laser_power (dict): laser powers as percentage (keys: '405', '488', '561', '640').

    experiment : experiment object
        Contains volume scan parameters, including:
            - n_steps (int): number of planes in the volume.
            - scan_range (float): scan depth in micrometers.

    microscope : microscope object
        Describes the hardware setup. Must include:
            - volts_per_um (float): galvanometer scale in V/µm.
            - galvo_response_time (float): in milliseconds.
            - galvo_flyback_time (float): in milliseconds.
            - laser_response_time (float): in milliseconds.
            - volts_per_laser_percent (dict): scaling from % to volts for each laser.

    frequency : float, optional
        Sampling rate in Hz (default: 10,000 Hz). Determines the time resolution of generated signals.

    Returns
    -------
    tensions_library : dict
        A dictionary of time-resolved signals for the volume acquisition:
            - 'tensions_galvo' (np.ndarray): analog signal for galvo control (in volts).
            - 'tensions_camera' (np.ndarray): digital signal to trigger camera exposure (boolean).
            - 'tensions_laser_blanking' (np.ndarray): digital laser blanking signal (boolean).
            - 'tensions_lasers' (np.ndarray): analog laser power signals, shape (4, N), one per laser.

    Notes
    -----
    - All durations are internally converted to time units based on the sampling frequency.
    - Laser power is set constant across the entire volume acquisition.
    - Only one channel and one camera are used.
    """
    
    #
    # Get values
    #
    
    """Get all the values from dictionnary, time is converted in seconds"""
    
        # ---- Camera parameters ----
    camera_id = channels[0].camera
    image_readout_time_s = cameras[camera_id].image_readout_time 
    
        # ---- Channel parameters ----
    exposure_time_s = channels[0].exposure_time / 1000 # To get exposure_time in seconds
    
        # Get laser powers in % for each laser channel (405, 488, 561, 640)
    laser_power = [channels[0].laser_power['405'],channels[0].laser_power['488'],
                   channels[0].laser_power['561'],channels[0].laser_power['640']] # Get all laser power in percent
    
        # Get laser calibration factors (V per % of power)
    volts_per_laser_percent = [microscope.volts_per_laser_percent['405'],
                               microscope.volts_per_laser_percent['488'],
                               microscope.volts_per_laser_percent['561'],
                               microscope.volts_per_laser_percent['640'],
                               ]
        # Convert laser powers in % to voltages
    laser_volts = []
    
    for k in range(len(laser_power)) :
        laser_volts.append(laser_power[k]/volts_per_laser_percent[k]) # Get all laser power in volts
    
        # --- Experiment parameters ----
    n_steps = experiment.n_steps
    scan_range_um = experiment.scan_range
    
        # ---- Microscope parameters ----
    volts_per_um = microscope.volts_per_um
    galvo_response_time_s = microscope.galvo_response_time /1000 # To get response_time in seconds
    galvo_flyback_time_s = microscope.galvo_flyback_time /1000
    laser_response_time_s = microscope.laser_response_time /1000
    
    #
    # Time calculation in unit of time
    #
    
        # Convert times to sample units based on the sampling frequency
    pre_post_volume_wait = int(max(galvo_flyback_time_s,laser_response_time_s)*frequency) # Time before and after the volume in seconds
    galvo_response_time = int(np.ceil(galvo_response_time_s * frequency)) # en unité de temps
    image_readout_time = int(np.ceil(image_readout_time_s * frequency)) # en unité de temps
    exposure_time = int(np.ceil(exposure_time_s * frequency)) # en unité de temps
    
        # Duration of a single step = galvo settle + exposure + readout
    step_duration = exposure_time + image_readout_time + galvo_response_time
    
        # Total number of timepoints in the signal
    total_duration = int(pre_post_volume_wait * 2 + n_steps * step_duration)

    
    #
    # Create vectors
    #
    
        # --- Preallocate output arrays ---
        
    tensions_galvo = np.zeros(total_duration)
    tensions_camera = np.zeros(total_duration , dtype='bool')
    tensions_laser_blanking = np.full(total_duration, True) # Laser is On for all volume
    tensions_lasers = np.zeros([4,total_duration])
    
        # Apply laser voltages during the entire volume acquisition
    for i in range(4):
        tensions_lasers[i] = laser_power[i] # Laser is On for all volume
    
        
    #
    # fill vectors
    #
    
        # --- Galvo scanning positions in volts ---
    
    galvo_tensions_amplitude = volts_per_um * scan_range_um
    galvo_positions = np.linspace(-galvo_tensions_amplitude / 2,
                              galvo_tensions_amplitude / 2,
                              n_steps)
    
        # Initial hold position before starting the scan
    tensions_galvo[0:pre_post_volume_wait] = - galvo_tensions_amplitude / 2
    
        # --- Step loop ---
    for step in range(n_steps) :
        
        start_index = pre_post_volume_wait + step * step_duration

        # Set galvo position
        tensions_galvo[start_index : start_index + step_duration] = galvo_positions[step]
               
        # Trigger camera during exposure window
        tensions_camera[start_index : start_index + exposure_time] = True

    
    #
    # Put everything back to original position
    #
    
    
        # Return galvo to neutral (0V), stop lasers and blank them
    tensions_galvo[pre_post_volume_wait + n_steps * step_duration:] = 0
    
        # Turn off laser blanking
    tensions_laser_blanking[pre_post_volume_wait + n_steps * step_duration:] = False
    
        # Turn off all lasers
    for i in range(4):
        tensions_lasers[i][pre_post_volume_wait + n_steps * step_duration:] = 0
    
    #
    # Return all signals
    #
    
    tensions_library = {'tensions_galvo' : tensions_galvo,
                       'tensions_camera' : tensions_camera,
                       'tensions_laser_blanking' : tensions_laser_blanking,
                       'tensions_lasers' : tensions_lasers,
    
                       }

    return tensions_library

###############################################################################
def plot_tension_vectors(tensions_library):
    """
    Plot each vector in the tensions library as a graph.

    Parameters:
    - tensions_library (dict): A dictionary containing tension vectors.
                               Expected keys: 'tensions_galvo', 'tensions_camera',
                               'tensions_laser_blanking', 'tensions_lasers'.

    Returns:
    - None: Displays the plots.
    """
    # Plot settings
    fig, axs = plt.subplots(len(tensions_library), 1, figsize=(10, 8), sharex=True)
    fig.suptitle('Tension Vectors Visualization')

    # Plot each vector
    for i, (key, value) in enumerate(tensions_library.items()):
        if key == 'tensions_camera' or key == 'tensions_laser_blanking':
            # Convert boolean values to integers for plotting
            value = value.astype(int)

        if key == 'tensions_lasers':
            # Plot each laser channel separately
            for j in range(value.shape[0]):
                axs[i].plot(value[j], label=f'Laser {j+1}')
            axs[i].legend()
        else:
            axs[i].plot(value)

        axs[i].set_title(key)
        axs[i].set_ylabel('Amplitude')

    axs[-1].set_xlabel('Time (units)')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# Exemple d'utilisation créant un graphique

if __name__ == '__main__':
    import os
    import sys 
    import time
    
    # Ajoute le dossier parent du dossier Tools au path
    current_dir = os.path.dirname(__file__)  # .../Tools/signal_generators
    parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))  # va à la racine du projet
    config_dir = os.path.join(parent_dir, 'Config')
    
    if config_dir not in sys.path:
        sys.path.insert(0, config_dir)
    
    from MDA_config import config
    
    start_time = time.time()
        
    microscope_config = config()
        
    frequency = 1e4
        
    tension_library = generate_single_channel_signals(microscope_config.cameras,
                                                   microscope_config.channels,
                                                   microscope_config.experiment,
                                                   microscope_config.microscope,
                                                   frequency = frequency)
    
    end_time = time.time()

    print(f"Temps pour créer le vecteur : {end_time - start_time:.6f} secondes")
    
    time = len(tension_library['tensions_galvo'])/frequency
    
    print(f'Temps / volume = {time} secondes')
        
    plot_tension_vectors(tension_library)