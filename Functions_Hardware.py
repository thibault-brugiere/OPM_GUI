# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 17:19:56 2025

@author: tbrugiere
"""
import numpy as np
import serial
import serial.tools.list_ports
import time as t

from PySide6.QtCore import QThread, Signal

# Camera

#DAQ
import nidaqmx
from nidaqmx.constants import AcquisitionType

class functions_camera():
    
    def configure_camera_for_preview(hcam, camera):
        """Configure les paramètres de la caméra."""
        camera_id = camera.camera_id
        
        hcam.setACQMode("run_till_abort", 20, camera.camera_id) #5 correspond au nombre d'images dans le buffer
        
        hcam.setPropertyValue("subarray_hsize", camera.hsize, camera_id)
        hcam.setPropertyValue("subarray_vsize", camera.vsize, camera_id)
        hcam.setPropertyValue("subarray_hpos", camera.hpos, camera_id)
        hcam.setPropertyValue("subarray_vpos", camera.vpos, camera_id)
        
        hcam.setPropertyValue("binning", camera.binning, camera_id)
        
        hcam.setPropertyValue("exposure_time", camera.exposure_time, camera_id)
       
class CameraThread(QThread):
    """Thread qui acquiert en continu la dernière image de la caméra."""
    new_frame = Signal(np.ndarray)  # Signal émis à chaque nouvelle image

    def __init__(self, hcam, camera_id):
        super().__init__()
        self.camera_id = camera_id
        self.hcam = hcam
        self.running = True  # Permet de contrôler l'arrêt propre du thread

    def run(self):
        """Boucle d'acquisition d'images en continu."""
        while self.running:
            frames, dims, [w, h] = self.hcam.getFrames(self.camera_id)
            if frames:
                aframe = frames[-1]  # On prend la dernière image disponible
                frame = aframe.getData()
                frame.shape = (h, w)
                self.new_frame.emit(frame)  # Émettre l'image pour l'affichage

    def stop(self):
        """Arrête proprement l'acquisition."""
        self.running = False
        self.quit()
        self.wait()
        
class functions_daq():
    
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

class functions_super_agilis():
    
    def list_serial_ports():
        """
        List all available serial ports.
        """
        ports = serial.tools.list_ports.comports()
        devices = []
        for port in ports:
            # print(f"Device: {port.device}, Description: {port.description}")
            devices.append(port.device)
            
        return devices
    
    def send_command(command, port = 'COM3'):
        """
        Send a command to the Super Agilis Controller.
    
        Parameters:
        - port (str): The serial port to which the device is connected.
        - command (str): The command to send to the device.
        """
        try:
            # Ouvrir la connexion série
            with serial.Serial(port, 9600, timeout=1) as ser:
                # Envoyer la commande
                ser.write(command.encode('ascii') + b'\r\n')
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
    
    def send_command_response(command, port = 'COM3'):
        """
        Send a command to the Super Agilis Controller and get response.
    
        Parameters:
        - port (str): The serial port to which the device is connected.
        - command (str): The command to send to the device.
        """
        try:
            # Ouvrir la connexion série
            with serial.Serial(port, 9600, timeout=1) as ser:
                # Envoyer la commande
                ser.write(command.encode('ascii') + b'\r\n')
                # Lire la réponse
                response = ser.readline().decode('ascii').strip()
                # print(f"Response: {response}")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            
        return response
            
    """
    Command list:
    note : query the current value when the command name is followed by a “?”
    
    XF1000 : set step frequancy to 1000 Hz
    XR1 : Move of 1 step
    XU-21,21 : set the step size at 21% in negative and positive direction (seems to be the minimum) (step frequency should be <1000)
    tp : Get current position
    JA : move jogging (1 : 50/s steps, 2 : 1000 steps/s)
    """