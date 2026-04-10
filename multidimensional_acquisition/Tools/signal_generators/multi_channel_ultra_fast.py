# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 11:31:14 2025

@author: tbrugiere
"""
import numpy as np
import matplotlib.pyplot as plt

def generate_channel_signals(cameras, channels, experiment, microscope, frequency = 1e5):
    """
    Generate voltage and logic signals required to control volume acquisition with a microscope.
    Using a ultra-fast algorythme

    The function simulates one volumetric acquisition, which includes:
        1) Galvo positioning (with response time and flyback delay)
        2) Laser activation
        3) Camera exposure
        4) Camera readout
        5) Filter changing
        6) Step repetition for each plane

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
            - filter_changing_time (float): in milliseconds.
            - volts_per_laser_percent (dict): scaling from % to volts for each laser.

    frequency : float, optional
        Sampling rate in Hz (default: 10,000 Hz). Determines the time resolution of generated signals.

    Returns
    -------
    tensions_library : dict
        A dictionary of time-resolved signals for the volume acquisition:
            - 'tensions_galvo' (np.ndarray): analog signal for galvo control (in volts).
            - 'tensions_camera' (np.ndarray): digital signal to trigger camera exposure (boolean).
            - 'tensions_laser_blanking' (np.ndarray): digital laser blanking signal (boolean), shape (4, N),
                                                        one per laser.
            - 'tensions_lasers' (np.ndarray): analog laser power signals, shape (4, N), one per laser.
            - 'tensions_filters' (np.ndarray): digital signal to trigger the filter well, shape = (2, N),
                                                one per trigering 

    Notes
    -----
    - All durations are internally converted to time units based on the sampling frequency.
    """
    
    #
    # Get values
    #
    
    """Get all the values from dictionnary, time is converted in seconds"""
    
        # ---- Camera parameters ----
    image_readout_time_s = cameras[0].image_readout_time
    
        # Get laser calibration factors (V per % of power)
    volts_per_laser_percent = [microscope.volts_per_laser_percent['405'],
                               microscope.volts_per_laser_percent['488'],
                               microscope.volts_per_laser_percent['561'],
                               microscope.volts_per_laser_percent['640'],
                               ]
    
        # --- Experiment parameters ----
    n_steps = experiment.n_steps # Number of image per channel
        
    filterseq = [chan.filter for chan in channels]
    filters_mouve = mouvement_sequence(microscope.filters , filterseq)
    
    scan_range_um = experiment.scan_range
    
        # ---- Microscope parameters ----
    volts_per_um = microscope.volts_per_um
    galvo_response_time_s = microscope.galvo_response_time /1000 # To get response_time in seconds
    galvo_flyback_time_s = microscope.galvo_flyback_time /1000
    laser_response_time_s = microscope.laser_response_time /1000
    filter_changing_time = [time / 1000 for time in microscope.filter_changing_time]
    
    #
    # Time calculation in unit of time
    #
    
        # Convert times to sample units based on the sampling frequency
    pre_volume_wait = int(max(galvo_flyback_time_s,laser_response_time_s)*frequency) # Time before the volume in unit of time

    galvo_response_time = int(np.ceil(galvo_response_time_s * frequency)) # en unité de temps
    image_readout_time = int(np.ceil(image_readout_time_s * frequency)) # en unité de temps
    
        # --- Pre_Create output arrays ---
    tensions_galvo = np.zeros(0)
    tensions_camera = np.zeros(0 , dtype='bool')
    tensions_laser_blanking = np.zeros([4,0], dtype='bool') # Laser is On for all volume
    tensions_lasers = np.zeros([4,0])
    tensions_filters = np.zeros([2,0], dtype='bool')
    
    #
    # Values that will be use to calculate vectors
    #
    
        # --- Galvo scanning positions in volts ---
    
    galvo_tensions_amplitude = volts_per_um * scan_range_um
    
    for index, channel in enumerate(channels):
        
        """Get all the values from dictionnary the the actual channel, time is converted in seconds"""
        
        # calculate the time to change the filter at the end of the channel
        if len(channels) == 1:
            post_volume_wait = int(max(galvo_flyback_time_s,laser_response_time_s)*frequency) # Time after the volume in unit of time
        else:
            fm = abs(filters_mouve[index])
            t = filter_changing_time[fm - 1] if fm > 0 else 0
            post_volume_wait = int(max(galvo_flyback_time_s,laser_response_time_s, t)*frequency) # Time after the volume in unit of time
        
        filter_triger_duration = min(int(np.ceil(10 / 1000 * frequency)),post_volume_wait) # en unité de temps
            
            
            # ---- Camera / channel parameters ----
        camera_id = channel.camera
        image_readout_time_s = cameras[camera_id].image_readout_time
        exposure_time_s = channel.exposure_time / 1000 # To get exposure_time in seconds
        exposure_time = int(np.ceil(exposure_time_s * frequency))
        
            # Get laser powers in % for each laser channel (405, 488, 561, 640), and laser active
            
        laser_power = [channel.laser_power['405'],channel.laser_power['488'],
                       channel.laser_power['561'],channel.laser_power['640']] # Get all laser power in percent
        
        laser_active = [channel.laser_is_active['405'],channel.laser_is_active['488'],
                        channel.laser_is_active['561'],channel.laser_is_active['640']]
        
        # Duration of a single step = galvo settle + exposure + readout
        step_duration = exposure_time
    
        # Total number of timepoints in the signal
        channel_duration = int(pre_volume_wait + post_volume_wait + n_steps * step_duration + image_readout_time)
        
        #
        # Create vectors
        #
        
            # --- Preallocate output arrays ---
        tensions_galvo_channel = np.zeros(channel_duration)
        tensions_camera_channel = np.zeros(channel_duration , dtype='bool')
        tensions_laser_blanking_channel = np.zeros([4,channel_duration], dtype='bool') # Laser is On for all volume
        tensions_lasers_channel = np.zeros([4,channel_duration])
        tensions_filters_channel = np.zeros([2,channel_duration], dtype='bool')
        
        #
        # fill vectors
        #
        
        # Convert laser powers in % to voltages
        laser_volts = []
        
        for k in range(len(laser_power)) :
            # Turn on laser during all acquisition
            laser_volts.append(laser_power[k] * volts_per_laser_percent[k]) # Get all laser power in volts
            tensions_lasers_channel[k,:channel_duration - post_volume_wait] = laser_volts[k] # set laser power for all volume
            
        # Turn laser for allthe volume
        for i in range(len(laser_active)):
            if laser_active[i]:
                tensions_laser_blanking_channel[i,:channel_duration - post_volume_wait] = True
        
        # set tensions galvo
        
        tensions_galvo_channel[0:pre_volume_wait] = -galvo_tensions_amplitude / 2
        tensions_galvo_channel[pre_volume_wait:channel_duration - post_volume_wait] = np.linspace(-galvo_tensions_amplitude / 2,
                                                                               galvo_tensions_amplitude / 2,
                                                                               len(tensions_galvo_channel[pre_volume_wait:channel_duration - post_volume_wait]))
        tensions_galvo_channel[channel_duration - post_volume_wait:] = - galvo_tensions_amplitude / 2
        
        # --- Step loop ---
        for step in range(n_steps + 1) : # one step more for last reading
            
            start_index = pre_volume_wait + step * step_duration

            
            # Trigger camera during exposure window
            tensions_camera_channel[start_index : start_index + int(100e-6 * frequency) ] = True # To get a trigger of 100µs
        
            # send signal to move the filter to the next position
        wheel_trigger = 0
        
        if len(channels) != 1 :
    
            tensions_filters_channel[wheel_trigger,channel_duration - post_volume_wait : channel_duration - post_volume_wait + filter_triger_duration] = True
        
        else:  # Est- utilisé pour le comptage des channels depuis l'ordinateur
            tensions_filters_channel[wheel_trigger,channel_duration - post_volume_wait : channel_duration -1 ] = True 
        
        tensions_galvo = np.append(tensions_galvo, tensions_galvo_channel)
        tensions_camera = np.append(tensions_camera, tensions_camera_channel)
        tensions_laser_blanking = np.concat((tensions_laser_blanking, tensions_laser_blanking_channel), axis = 1)
        tensions_lasers = np.concat((tensions_lasers, tensions_lasers_channel), axis = 1)
        tensions_filters = np.concat((tensions_filters, tensions_filters_channel), axis = 1)
    
    tensions_library = {'tensions_galvo' : tensions_galvo,
                       'tensions_camera' : tensions_camera,
                       'tensions_filters' : tensions_filters,
                       'tensions_lasers' : tensions_lasers,
                       'tensions_laser_blanking' : tensions_laser_blanking,
                       }

    return tensions_library

def mouvement_sequence(filters, filterseq):
    """
    Calcule les mouvements cycliques à faire sur la roue de filtres.

    Args:
        filters : Liste complète des positions de la roue (ordre physique).
        filterseq: Liste des filtres à utiliser (ordre acquisition).

    Returns:
        liste_de_mouvements: Liste des déplacements cycliques entre chaque filtre (en slots, positifs ou négatifs).
    """
    n = len(filters)
    positions = [filters.index(filtre) for filtre in filterseq]
    positions.append(positions[0])
    mouvements = []
    for i in range(1, len(positions)):
        pos_actuelle = positions[i-1]
        pos_voulue = positions[i]
        # Mouvement minimal (cyclique)
        delta_plus = (pos_voulue - pos_actuelle) % n
        if delta_plus <= n/2:
            mouvement = delta_plus
        else:
            mouvement = delta_plus - n
        mouvements.append(mouvement)
    return mouvements

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
        if key == 'tensions_camera'or key == 'tensions_laser_blanking' or key == 'tensions_filters':
            # Convert boolean values to integers for plotting
            value = value.astype(int)

        if key == 'tensions_lasers' or key == 'tensions_laser_blanking':
            # Plot each laser channel separately
            for j in range(value.shape[0]):
                axs[i].plot(value[j], label=f'Laser {j+1}')
            axs[i].legend()
            
        elif key == "tensions_filters":
            for j in range(value.shape[0]):
                axs[i].plot(value[j], label=f'Filter trig {j+1}')
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
        
    microscope_config = config(filename = 'GUI_parameters_double.json')
        
    frequency = 1e5
    print(microscope_config.experiment.exp_name)
    tension_library = generate_channel_signals(microscope_config.cameras,
                                                   microscope_config.channels,
                                                   microscope_config.experiment,
                                                   microscope_config.microscope,
                                                   frequency = frequency)
    
    end_time = time.time()

    print(f"Temps pour créer le vecteur : {end_time - start_time:.6f} secondes")
    
    time = len(tension_library['tensions_galvo'])/frequency
    
    print(f'Temps / volume = {time} secondes')
        
    plot_tension_vectors(tension_library)