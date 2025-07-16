# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 14:19:15 2025

@author: tbrugiere
"""
import nidaqmx
import numpy as np

class NIDAQ_Acquisition:
    
    """
    Class to control signal generation and synchronization for volumetric image acquisition 
    using a National Instruments DAQ device.
    
    This class manages:
    - Analog outputs (AO) for galvanometer and lasers
    - Digital outputs (DO) for camera trigger and laser blanking
    - Counter outputs (CO) to generate periodic TTL pulses for volume triggering
    
    Workflow:
    1. Call send_signals_to_daq_single_channel_progress(...) to configure the DAQ tasks.
    2. Call arm_task() to start AO/DO tasks and prepare them to wait for the trigger.
    3. Call trigger_acquisition() to begin volume acquisition via TTL pulse train.
    4. Use stop() to interrupt acquisition.
    5. Use close() to fully release all DAQ resources.
    
    State transitions:
        'idle'   --> after initialization or closing tasks
        'ready'  --> after DAQ configuration
        'armed'  --> after AO/DO tasks are started
        'running'--> during active acquisition
    """

    def __init__(self):
        """
        Initializes the acquisition controller.
        
        Sets the internal state to 'idle' and placeholders for the DAQ tasks.
        Actual DAQ tasks must be configured by calling send_signals_to_daq_single_channel_progress().
        """
        self.state = "idle"
        self.task_ao = None
        self.task_do = None
        self.task_co = None
    
    def send_signals_to_daq_single_channel(self, tensions_library, timepoints, time_intervals,
                                                    daq_channels, frequency = 1e4):
        """
        Prepares and sends analog and digital control signals to the NI-DAQ for a 
        single-channel volumetric acquisition.
    
        This function sets up:
        - Analog output channels (AO) for controlling the galvanometer and lasers
        - Digital output channels (DO) for triggering the camera and laser blanking
        - Counter output channel (CO) to generate periodic TTL pulses that trigger each volume acquisition
    
        The signals are synchronized so that each volume is triggered by a rising edge
        of the TTL signal, and the DAQ replays the appropriate AO and DO waveforms 
        at the defined sampling frequency.
    
        Parameters
        ----------
        tensions_library : dict
            Dictionary containing the precomputed voltage signals to send. Must include:
            - 'tensions_galvo' : Galvo control voltage (1D array)
            - 'tensions_lasers' : Laser control voltages (2D array: shape [N_lasers, N_samples])
            - 'cameras' : Digital signal to trigger camera (1D bool array)
            - 'laser_blanking' : Digital signal for laser blanking (1D bool array)
        
        time_intervals : float
            Time interval between two volume acquisitions (in seconds). Used to define 
            the period of the trigger TTL signal (CO output).
        
        timepoints : int
            Number of volumes to acquire (i.e., number of repetitions of the TTL trigger).
        
        daq_channels : dict
            Dictionary mapping signal names to their corresponding NI-DAQ channel names:
            - Analog: 'galvo', '405', '488', '561', '640'
            - Digital: 'camera_0', 'laser_blanking'
            - Counter: 'co_channel', 'co_terminal'
        
        frequency : float, optional
            Sampling frequency (in Hz) for analog and digital waveform outputs. Default is 10 kHz.
    
        Notes
        -----
        The laser control currently supports only 3 channels due to a limited number of analog outputs.
        The analog and digital outputs are synchronized and triggered by the same CO pulse signal.
        """
        
        # Store the provided parameters as instance variables
        self.tensions_library = tensions_library
        self.timepoints = timepoints
        self.time_intervals = time_intervals
        self.daq_channels = daq_channels
        self.frequency = frequency
        
        #
        # Create outputs
        #
        self.task_ao = nidaqmx.Task() # galvo
        self.task_do = nidaqmx.Task() # Camera + lasers
        self.task_co = nidaqmx.Task() # trigger start of each volume
        
        self.volume_duration = len(self.tensions_library['tensions_galvo'])
        
        #
        # Analog outputs
        #
        
        # Create AO channels: galvo + 3 laser channels (405, 488, 561)
        # NOTE: Limited to 3 lasers due to available DAQ channels
        # TODO : find a solution to use 4 lasers
        
            # Create all the analog channels
        self.task_ao.ao_channels.add_ao_voltage_chan(self.daq_channels["galvo"], min_val=-5.0, max_val=5.0)
        self.task_ao.ao_channels.add_ao_voltage_chan(self.daq_channels["405"], min_val=-5.0, max_val=5.0)
        self.task_ao.ao_channels.add_ao_voltage_chan(self.daq_channels["488"], min_val=-5.0, max_val=5.0)
        self.task_ao.ao_channels.add_ao_voltage_chan(self.daq_channels["561"], min_val=-5.0, max_val=5.0)
        # self.task_ao.ao_channels.add_ao_voltage_chan(self.daq_channels["561"], min_val=-5.0, max_val=5.0)
        
        
            # Set timing (sample clock) for AO output
        self.task_ao.timing.cfg_samp_clk_timing(self.frequency, samps_per_chan = self.volume_duration)
        
            # Configure trigger: AO task starts on rising edge of CO terminal signal, and is retriggerable
        self.task_ao.triggers.start_trigger.retriggerable = True
        self.task_ao.triggers.start_trigger.cfg_dig_edge_start_trig(self.daq_channels["co_terminal"],
                                                                    trigger_edge=nidaqmx.constants.Edge(10280)) #10280 => Rising Edge
            # Send analog waveforms (stack galvo + first 3 lasers)
        self.task_ao.write(np.vstack([self.tensions_library["tensions_galvo"],
                                      self.tensions_library['tensions_lasers'][:3]])) #Can only get the 3 first 
        
        #
        # Digital outputs
        #
        
            # Create DO channels: camera trigger + laser blanking
        self.task_do.do_channels.add_do_chan(self.daq_channels["camera_0"])
        self.task_do.do_channels.add_do_chan(self.daq_channels["laser_blanking"])
        
            # Set timing and synchronization identical to AO
        self.task_do.timing.cfg_samp_clk_timing(self.frequency, samps_per_chan=self.volume_duration)
        
            # Configure trigger: AO task starts on rising edge of CO terminal signal, and is retriggerable
        self.task_do.triggers.start_trigger.retriggerable = True
        self.task_do.triggers.start_trigger.cfg_dig_edge_start_trig(self.daq_channels["co_terminal"],
                                                                    trigger_edge=nidaqmx.constants.Edge(10280)) #10280 => Rising Edge
        
            # Send digital waveforms (camera trigger and laser blanking signals)
        self.task_do.write(np.vstack([self.tensions_library['tensions_camera'],
                                      self.tensions_library['tensions_laser_blanking']]))
        
        #
        # Number of volumes counter
        #
        
            # Configure CO (Counter Output) to emit periodic TTL pulses
            # Pulse frequency = 1 / time_intervals
            # low_ticks = duration of LOW state (100 ticks = 1 ms at 100 kHz)
            # high_ticks = duration of HIGH state (rest of the interval)

        self.channel_co = self.task_co.co_channels.add_co_pulse_chan_ticks( # co : Counter Output
            counter=self.daq_channels["co_channel"],
            source_terminal="/Dev1/100kHzTimebase",
            low_ticks=int(100),
            high_ticks=int((self.time_intervals * 1e5 )-100))
        
            # Specify where the TTL pulse is sent
        self.channel_co.co_pulse_term = self.daq_channels["co_terminal"]
        
            # Set implicit timing to repeat the pulse signal for the number of timepoints
        self.task_co.timing.cfg_implicit_timing(samps_per_chan = self.timepoints)
        
        self.state = "ready"
        
    def arm_task(self):
        """Prepare AO and DO tasks. They will wait for a trigger to begin output."""
        if self.state != "ready":
            raise RuntimeError(f"Cannot start acquisition from state '{self.state}'. Must be 'armed'.")
            
        self.task_ao.start()
        self.task_do.start()
        
        self.state = "armed"
        
    def trigger_acquisition(self):
        """Start the CO task that triggers all other tasks periodically."""
        if self.state != "armed":
            raise RuntimeError(f"Cannot start acquisition from state '{self.state}'. Must be 'armed'.")
            
        self.task_co.start()
        
        self.state = "running"
        
    def stop(self):
        """
        Stops all tasks. Can be restarted by calling arm_task again.
        """
        if self.state != "running" and self.state != "armed":
            print(f"DAQ not running or armed. Current state: '{self.state}'. Nothing to stop.")
            return

        self.task_ao.stop()
        self.task_do.stop()
        self.task_co.stop()

        self.state = "ready"

    def close(self):
        """
        Fully closes all DAQ tasks and releases resources.
        Must be re-armed before reuse.
        """
        if self.task_ao:
            self.task_ao.close()
        if self.task_do:
            self.task_do.close()
        if self.task_co:
            self.task_co.close()

        self.task_ao = None
        self.task_do = None
        self.task_co = None

        self.state = "idle"