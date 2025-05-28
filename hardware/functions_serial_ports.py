# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 14:28:45 2025

@author: tbrugiere
"""

import serial
import serial.tools.list_ports

#
# Functions command serial ports - piezzo
#

class functions_serial_ports():
    
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
        Send a command to the Controller.
    
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
        Send a command to the Controller and get response.
    
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
