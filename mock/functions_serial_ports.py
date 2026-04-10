# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 16:24:07 2025

@author: tbrugiere
"""

import threading

#
# Functions command serial ports - piezzo
#

class functions_serial_ports():
    
    def list_serial_ports():
        """
        List all available serial ports.
        """
        
        return ["COM"]
    
    def send_command(command, port = 'COM3'):
        """
        Send a command to the Controller.
    
        Parameters:
        - port (str): The serial port to which the device is connected.
        - command (str): The command to send to the device.
        """
        return f"send: {command}"
    
    def send_command_response(command, port = 'COM3'):
        """
        Send a command to the Controller and get response.
    
        Parameters:
        - port (str): The serial port to which the device is connected.
        - command (str): The command to send to the device.
        """
        if command == "HID?":
            response = "L4CC"
        else :
            response = f"send: {command} - response: ok"
            
        return response

class DebouncedSetter:
    """
    Calls a function (e.g., set_power) with a delay, canceling previous calls
    if a new command is received before the delay expires.

    Useful to avoid flooding slow hardware (e.g., serial ports) with rapid commands.
    Note: this version does NOT return the result of the command (e.g., from send_command_response).
    """

    def __init__(self, delay_sec=0.1):
        """
        Parameters:
        - delay_sec : Time to wait (in seconds) after the last command before executing it.
        """
        self.delay_sec = delay_sec
        self._timers = {}  # Dictionary: {port -> active Timer}

    def set_power(self, command, port, setter_func):
        """
        Schedules a command to be executed after a delay. If a new command is sent
        to the same port before the delay expires, the previous one is canceled.

        Parameters:
        - command : The command to send (e.g., "PPL1 30")
        - port : Target port (e.g., "COM5")
        - setter_func : The function to execute → e.g., functions_serial_ports.send_command
        """

        # Cancel any pending timer for the same port
        if port in self._timers:
            self._timers[port].cancel()

        # This inner function will be called after delay_sec
        def _apply():
            setter_func(command, port)   # Actual command execution
            del self._timers[port]       # Clean up the timer entry

        # Start a new timer for this port
        timer = threading.Timer(self.delay_sec, _apply)
        self._timers[port] = timer
        timer.start()