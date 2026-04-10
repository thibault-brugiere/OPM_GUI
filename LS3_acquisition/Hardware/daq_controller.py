# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 14:19:15 2025

@author: tbrugiere
"""
import nidaqmx
from nidaqmx.constants import Edge, CountDirection
import numpy as np

class NIDAQ_Acquisition_ls3:
    
    """
    Class to control signal generation and synchronization for volumetric image acquisition
    during ls3 scanning protocol
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
    
    def send_signals_to_daq_single_channel(self, tensions_library,
                                           timepoints,
                                           time_intervals,
                                           daq_channels,
                                           daq_channels_laser_analog_out,
                                           daq_channels_laser_digital_out,
                                           frequency = 1e5):
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
            - 'tensions_cameras' : Digital signal to trigger camera (1D bool array)
            - 'tensions_lasers' : Laser control voltages (4D array: shape [N_lasers, N_samples])
            - 'tensions_laser_blanking' : Digital signal for laser blanking (4D bool array)
            - 'tensions_filters' : Digital signal for laser blanking (4D bool array)
        
        time_intervals : float
            Time interval between two volume acquisitions (in seconds). Used to define 
            the period of the trigger TTL signal (CO output).
        
        timepoints : int
            Number of volumes to acquire (i.e., number of repetitions of the TTL trigger).
        
        daq_channels : dict
            Dictionary mapping signal names to their corresponding NI-DAQ channel names:
            => daq_channels : general daq channels including :
                - Analog : 'camera_0', 'camera_1', "galvo"
                - Digital : "filter_wheel_1" and "filter_wheel_1"
            => daq_channels_laser_analog_out : daq channels used fot analog laser controll
                must take in account the number of analog output avaliable (others should be set as Null)
                if there are more, only 3 firsts will be tanken in account.
            => daq_channels_laser_digital_out : daq channels used fot digital laser controll
        
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
        self.daq_channels_laser_analog_out = daq_channels_laser_analog_out
        self.daq_channels_laser_digital_out = daq_channels_laser_digital_out
        self.frequency = frequency
        
        #
        # Create outputs
        #
        self.task_ao = nidaqmx.Task() # galvo
        self.task_do = nidaqmx.Task() # Camera + lasers
        self.task_di = nidaqmx.Task() # Signal à la fin de chaque volume
        
        self.volume_duration = len(self.tensions_library['tensions_galvo'])
        
        #
        # Analog outputs
        #
        
        # Create AO channels: galvo + 3 laser channels (405, 488, 561)
        # NOTE: Limited to 3 lasers due to available DAQ channels
        
            # Create all the analog channels
        self.task_ao.ao_channels.add_ao_voltage_chan(self.daq_channels["galvo"], min_val=-5.0, max_val=5.0)
        
        idx = 0 # use to know which 'tensions_lasers' line will be used
        self.tensions_lasers = None # to get the # use to know which 'tensions_lasers' line will be used
        for laser, out in self.daq_channels_laser_analog_out.items() :
            if out is not None :
                self.task_ao.ao_channels.add_ao_voltage_chan(out, min_val=-5.0, max_val=5.0)
                if self.tensions_lasers is None :
                    self.tensions_lasers = self.tensions_library['tensions_lasers'][idx]
                else:
                    self.tensions_lasers = np.vstack((self.tensions_lasers,
                                                      self.tensions_library['tensions_lasers'][idx]))
            idx +=1

            # Set timing (sample clock) for AO output
        self.task_ao.timing.cfg_samp_clk_timing(self.frequency, samps_per_chan = self.volume_duration)
        
            # Configure trigger: AO task starts on rising edge of CO terminal signal, and is retriggerable
        self.task_ao.triggers.start_trigger.retriggerable = True
        self.task_ao.triggers.start_trigger.cfg_dig_edge_start_trig(
            self.daq_channels["stage_triger"],
            trigger_edge=nidaqmx.constants.Edge.RISING)
            # Send analog waveforms (stack galvo + first 3 lasers)
        self.task_ao.write(np.vstack([self.tensions_library["tensions_galvo"],
                                      self.tensions_lasers]))
        
        #
        # Digital outputs
        #
        
            # Create DO channels: camera trigger + laser blanking
        self.task_do.do_channels.add_do_chan(self.daq_channels["camera_0"])
        self.task_do.do_channels.add_do_chan(self.daq_channels["filter_wheel_1"])
        self.task_do.do_channels.add_do_chan(self.daq_channels["filter_wheel_2"])
        for laser, out in self.daq_channels_laser_digital_out.items() :
            self.task_do.do_channels.add_do_chan(out)
        
            # Set timing and synchronization identical to AO
        self.task_do.timing.cfg_samp_clk_timing(self.frequency,
                                                source = "/Dev1/ao/SampleClock",
                                                samps_per_chan=self.volume_duration)
        
            # Configure trigger: AO task starts on rising edge of CO terminal signal, and is retriggerable
        self.task_do.triggers.start_trigger.retriggerable = True
        self.task_do.triggers.start_trigger.cfg_dig_edge_start_trig(
            self.daq_channels["stage_triger"],
            trigger_edge=nidaqmx.constants.Edge.RISING)
        
            # Send digital waveforms (camera trigger and laser blanking signals)
        self.task_do.write(np.vstack([self.tensions_library['tensions_camera'],
                                      self.tensions_library['tensions_filters'],
                                      self.tensions_library['tensions_laser_blanking']]))
        
        #
        # Digital input for volume measurement
        #
        
        self.task_di.ci_channels.add_ci_count_edges_chan(counter='Dev1/ctr1', 
                                                         edge = Edge.RISING,
                                                         initial_count = 0,
                                                         count_direction=CountDirection.COUNT_UP
                                                         )
        
        ch =  self.task_di.ci_channels[0]
        
        ch.ci_count_edges_term = self.daq_channels["channel_finished"]
        
        try:
            ch.ci_count_edges_dig_fltr_enable = True
            ch.ci_count_edges_dig_fltr_min_pulse_width = 5e-6  # 5 µs (ajuste si besoin: 10–50 µs)
            
        except AttributeError:
            print("⚠️ Filtre numérique non disponible via ces propriétés (ou non supporté par le device).")
        
        self.state = "ready"
        
        self._last_count = 0
        
    def read_count(self):
        val = self.task_di.read()
        return val
        
        
    def arm_task(self):
        """Prepare AO and DO tasks. They will wait for a trigger to begin output."""
            
        self.task_ao.start()
        self.task_do.start()
        self.task_di.start()
        
        self.state = "running"
        
    def stop(self):
        """
        Stops all tasks. Can be restarted by calling arm_task again.
        """
        if self.state != "running" and self.state != "armed":
            # print(f"DAQ not running or armed. Current state: '{self.state}'. Nothing to stop.")
            return

        self.task_ao.stop()
        self.task_do.stop()
        self.task_di.stop()

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
        if self.task_di:
            self.task_di.close()

        self.task_ao = None
        self.task_do = None
        self.task_di = None

        self.state = "idle"