# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 10:46:15 2025

@author: tbrugiere
"""
import numpy as np
import time as t

#DAQ
import nidaqmx
from nidaqmx.system import System
from nidaqmx.constants import AcquisitionType

class functions_daq():

    def get_connected_daq_devices():
        """
        Check for connected National Instruments DAQ devices and return a list of their names.

        Returns:
        - List[str]: A list of names of connected DAQ devices.
        """
        try:
            # Créez une instance du système NI-DAQmx
            system = System.local()

            # Obtenez la liste des dispositifs DAQ connectés
            devices = system.devices

            # Retournez une liste des noms des dispositifs
            return [device.name for device in devices]

        except Exception as e:
            print(f"Error detecting DAQ devices: {e}")
            return []
    
    def analog_out(tension=0, output_channel='Dev1/ao0'):
        """
        Generates an analog voltage output to the specified channel.
        
        This function writes a voltage value to the specified output channel, ensuring
        the voltage is constrained within the range of -5V to 5V.
        
        Parameters
        ----------
        output_channel : str, optional
            The name of the output channel to send the voltage to. 
            Default is "Dev1/ao0".
        tension : float, optional
            The voltage to be output. The value will be clamped between -5V and 5V.
            Default is 0V.
        Notes
        -----
        The output voltage will be clamped to the range of -5V to 5V, as these are the
        limits of the specified output channel.
        """
        if tension > 5:
            tension = 5
        if tension < -5:
            tension = -5
        #print("tension from "+out+" set to "+ str(tension)+"V\n")
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan(output_channel, min_val=-5.0, max_val=5.0)
            task.write(tension)
            
    def digital_out (signal = True, line_name = 'Dev1/port0/line3'):
        with nidaqmx.Task() as task:
            task.do_channels.add_do_chan(line_name)
            task.write(signal)
    
    def voltages(
            voltage_start = -5,
            voltage_end = 5,
            n_step = 21
            ):
        """
        Generates an array between a specified start and end value.
    
        This function creates a voltage array from the start voltage to the end voltage,
        evenly spaced over the specified number of steps.
        Parameters
        ----------
        voltage_start : float, optional
            The starting voltage of the sequence. Default is `variables.voltage_start`.
        voltage_end : float, optional
            The ending voltage of the sequence. Default is `variables.voltage_end`.
        n_step : int, optional
            The number of steps (or voltage levels) in the sequence. Default is `variables.n_step`.
        Returns
        -------
        numpy.ndarray
            An array of voltage values evenly spaced between `voltage_start` and `voltage_end`.
        """
        voltages=np.linspace(voltage_start, voltage_end, n_step)
        return voltages
            
    def steps_out(wait_function=t.sleep,
                  wait_instruction=2,
                  output_channel = "AO0",
                  voltages=voltages(),
                  frequency=10):
        """
        Generates a sequence of voltage steps to a specified channel on the DAQ device.
        
        Parameters:
        ----------
        wait_function : Callable, optional
            The function used to introduce a delay or pause the execution.
            Defaults to `time.sleep`.
        wait_instruction : Any, optional
            The argument passed to the `wait_function`. Defines the delay duration
            in seconds or custom behavior depending on the function.
            If `False`, the `wait_function` will be called without arguments.
            Defaults to 2.
        output_channel : str, optional
            The name of the DAQ device's output channel where the voltage steps 
            are sent (e.g., "Dev1/ao0").Defaults to `variables.ao_galvo`.
        voltages : list or numpy.ndarray, optional
            The sequence of voltages to output.
            Defaults to the output of the `voltages()` function.
        frequency : float, optional
            The sampling rate for the output signal in samples per second. 
            Defaults to `variables.frequency`.
        
        Notes
        -----
        - This function configures and starts a NI-DAQmx task to generate analog 
          output signals.
        - After writing the voltages, it uses the provided `wait_function` to pause 
          execution before stopping the task.
        - The `wait_function` and `wait_instruction` allow flexible behavior, such 
          as waiting for a user input or introducing a delay.
        
        Example
        -------
        steps_out(wait_function=input, wait_instruction="Press Enter to stop")
        """
        
        with nidaqmx.Task() as task:
            
            task.ao_channels.add_ao_voltage_chan(output_channel, min_val=-5.0, max_val=5.0)
            task.timing.cfg_samp_clk_timing(frequency, sample_mode=AcquisitionType.CONTINUOUS)
            
            task.write(voltages)
            
            task.start()
            
            if not wait_instruction:
                wait_function()
            else:
                wait_function(wait_instruction)
            
            task.stop()
