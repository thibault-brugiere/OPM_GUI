# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 10:48:47 2025

@author: tbrugiere
"""

import serial
import serial.tools.list_ports

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