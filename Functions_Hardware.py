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

from configs.config import camera

# Camera
from pylablib.devices import DCAM
# from mock.hamamatsu_DAQ import DCAM

#DAQ
import nidaqmx
from nidaqmx.system import System
from nidaqmx.constants import AcquisitionType

#
# Functions camera
#

class functions_camera():
    
    def initialize_cameras(n_camera):
        """
        Initialize a list of camera objects based on the number of detected cameras.
        
        Returns:
        - List[DCAM.DCAMCamera]: A list of initialized camera objects.
        - list[camera]: A list of camera objects from config
        """
        
        hcams = []
        cameras = []
        
        for camera_id in range(n_camera):
            hcam =DCAM.DCAMCamera(camera_id)
            hcams.append(hcam)
            
            cam = camera(camera_id)
            
            # Automatically get the parameters from the camera
            cam.hchipsize, cam.vchipsize = hcam.get_detector_size()
            cam.pixel_size = hcam.get_attribute_value('image_detector_pixel_width')
            
            cameras.append(cam)
            
        return hcams, cameras
    
    def close_cameras(hamamatsu_cameras):
        n_camera = len(hamamatsu_cameras)
        
        for camera_id in range(n_camera) :
            hamamatsu_cameras[camera_id].close()
    
    def configure_camera_for_preview(hcam, camera):
        """Configure les paramètres de la caméra."""

        hcam.cav["SUBARRAY MODE"]=2
        hcam.cav["EXPOSURE TIME"] = camera.exposure_time
        hcam.cav["subarray_hpos"] =  0 # Needed to avoid "INVALIDSUBARRAY"
        hcam.cav["subarray_vpos"] =  0 # Needed to avoid "INVALIDSUBARRAY"
        hcam.cav["subarray_hsize"] =  camera.hsize
        hcam.cav["subarray_vsize"] = camera.vsize
        hcam.cav["subarray_hpos"] =  camera.hpos
        hcam.cav["subarray_vpos"] =  camera.vpos
        hcam.cav["binning"] = camera.binning

class CameraThread(QThread):
    """Thread qui acquiert en continu la dernière image de la caméra."""
    new_frame = Signal(np.ndarray)  # Signal émis à chaque nouvelle image

    def __init__(self, hcam):
        super().__init__()
        self.hcam = hcam
        self.running = True  # Permet de contrôler l'arrêt propre du thread

    def run(self):
        """Boucle d'acquisition d'images en continu."""
        while self.running:
            frames = self.hcam.read_multiple_images()
            if frames:
                frame = frames[-1]  # On prend la dernière image disponible

                self.new_frame.emit(frame)  # Émettre l'image pour l'affichage

    def stop(self):
        """Arrête proprement l'acquisition."""
        self.running = False
        self.quit()
        self.wait()

#
# Functions DAQ
#
        
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

#
# Functions command serial ports - piezzo
#

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
    Note : ce n'est paspossible de bloquer la position dans l'absolue car si on éteint le piezzo,
    la position relative est perdue et le 0 correspond à la position lors de l'allumage.
    Pour avoir de nouveau la position il faut faire la commande RFH qui refait le référencing
    (et replace le piezzo sur le 0 absolue)
    De même il est impossible de faire un déplacement "absolu" sans référencement préalable.
    Ce qui nécessiterai de bouger le piezzo vers sa position 0.
    Utiliser la commande RFP qui permet de revenir à la position actuelle ?
        
    Command list:
    --------------
    note : query the current value when the command name is followed by a “?”
    
    RFH/RFP/RFM : start referencing of the positions, avant d'avoir accés à la position absolue (RFMnn to set position)
    OL : Open loop state (needed for the interface)
    OR : Cycle Loop state
    PA : move absolute (PA1 move to 1mm)
    PR : move relative (PR-1 move backward of 1mm)
    XF : set step frequancy to (XF1000 to set to 1000 Hz)
    XRn : Move of n steps (XR10 move of 10 steps)
    XU-n,n : set the step size at n% in negative and positive direction step frequency should be <1000 Hz
        (XU-1,21 change step size to 1% in negative axis and 21% in positive axis)
    TP? : Get current position
    JA : move jogging (1 : 50/s steps, 2 : 1000 steps/s 3: 5000 steps/s and 4:10000steps/s), needs ST to stop the motion
    ST : stop the current motion
    """