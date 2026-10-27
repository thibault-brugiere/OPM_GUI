# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 10:36:24 2026

@author: tbrugiere
"""
import atexit
import serial
import serial.tools.list_ports
from threading import RLock
import time as t

# from functions_serial_ports import functions_serial_ports as serial_port

# serial_port.list_serial_ports()

class WaterDispenserCommunicationError(RuntimeError):
    "Communication error with the controller"
    
class WaterDispenserTimeoutError(WaterDispenserCommunicationError):
    "The controller did not respond in time."
    
class WaterDispenserProtocolError(WaterDispenserCommunicationError):
    "WaterDispenser response is invalid or unexpected"
    
class WaterDispenserStateError(KeyError):
    "WaterDispenser state is unexpected"

class WaterDispenser():
    
    def  __init__ (self,
                   port = 'COM8',
                   model = 'TB-Microscope-Water-Dispenser-V1',
                   ul_per_step = 0.09227):
        self.port = port
        self.model = model
        self._serial : serial.Serial | None = None
        self._comm_lock = RLock()
        self._motion_lock = RLock()
        
        self.ul_per_step = ul_per_step
        if self.ul_per_step <= 0:
            raise ValueError(f"ul_per_step value should be >0 : {self.ul_per_step}")
        
        atexit.register(self.stop)
        
    def list_serial_ports(self) -> list:
        """
        List all available serial ports.
        """
        ports = serial.tools.list_ports.comports()
        devices = []
        for port in ports:
            devices.append(port.device)
            
        return devices
        
    def change_port(self, port: str) -> None:
        """
        Change the COM port of the WaterDispenser controller

        Parameters
        ----------
        port : str
            Name of the COM port of the WaterDispenser controller 
        """
        if not self.connected :
            self.port = port
            self._serial = None
        else :
            raise WaterDispenserStateError(f'WaterDispenser should not be connexted before changing port connected: {self.connected}')
    
    def get_port(self) -> str:
        """
        Return the port of the WaterDispenser

        Returns
        -------
        TYPE
            str

        """
        return self.port
    
    @property
    def connected(self):
        """Return whether the serial connection to the WaterDispenser controller is open."""
        return self._serial is not None and self._serial.is_open
    
    def connect(self) -> None:
        """
        Open and maintain the serial connection to the WaterDispenser controller.
        
        Any existing serial connection is closed before opening the new one.
        
        Raises
        ------
        WaterDispenserCommunicationError
            If the serial connection to the controller cannot be opened.
        """
        self.close()
        try :
            self._serial = serial.Serial(
                self.port,
                115200,
                timeout=1.0,
                )
                
        except OSError as exc:
            raise WaterDispenserCommunicationError(
                'Error during WaterDispenser connexion') from exc
            
        # Nano restarts during serial port opening
        t.sleep(2.0)
        
        message = self._serial.readline()
        if message == "READY":
            print(f"Water Dispenser {message}")
            
        if not self.test_port() :
            self.close()
            raise WaterDispenserCommunicationError(
            f"Device on port {self.port!r} is not the expected "
            f"Controller ({self.query('who')})."
        )
            
    def close(self) -> None:
        """
        Close the serial connection to the WaterDispenser controller.
        
        If no connection is currently open, this method has no effect.
        The serial object is released after closing the connection.
        """
        if self._serial is not None:
            try:
                if self._serial.is_open:
                    self._serial.close()
            finally:
                self._serial = None
                
    def test_port(self) -> bool:
        """
        Check if the port connected is really the WaterDispenser
        """
        return self.query("who") == self.model
    
    def blink(self, nb:int, delay_ms:int) -> None:
        """
        Blink the Arduino status LED.
    
        Parameters
        ----------
        nb : int
            Number of LED blinks.
        delay_ms : int
            Duration of the ON and OFF states, in milliseconds.
    
        Raises
        ------
        WaterDispenserProtocolError
            If the Arduino does not acknowledge the command correctly.
        """
        message = self.query(f"led {nb} {delay_ms}")
        
        if message != "LED BLINKING" :
            raise WaterDispenserProtocolError(f"blink didn't woark : {message}")
        
    def stop(self) -> int:
        """
        Stop the current motor movement.
    
        Returns
        -------
        int
            Motor position, in microsteps, when the movement was stopped.
    
        Raises
        ------
        WaterDispenserProtocolError
            If the Arduino does not return a valid stop acknowledgement.
        """
        if not self.connected :
            return
        
        message = self.query("stop")
        
        if not message.startswith("STOP DONE") :
            raise WaterDispenserProtocolError(f"run didn't work : {message}")
        
        split_message = message.split()
        
        if len(split_message) != 3:
            raise WaterDispenserProtocolError(
                f"invalid stop response: {message}"
            )
            
        return int(split_message[2])
        
        
    def run(self, speed, direction):
        """
        Start a continuous motor movement.
    
        Parameters
        ----------
        speed : int
            Motor speed, in microsteps per second.
            Values above 1000 are limited to 1000.
        direction : int
            Motor direction. Must be 0 or 1.
    
        Raises
        ------
        ValueError
            If `direction` is not 0 or 1.
        WaterDispenserProtocolError
            If the Arduino does not acknowledge the command correctly.
        """
        if direction not in (0, 1):
            raise ValueError("direction must be 0 or 1")
            
            
        speed = max(1, min(speed, 40000))
        message = self.query(f"run {speed} {direction}")
        
        if message != "RUN STARTED" :
            raise WaterDispenserProtocolError(f"run didn't work : {message}")
        
    def move(self, distance, speed, direction):
        """
        Move the motor by a specified number of microsteps.
    
        Parameters
        ----------
        distance : int
            Number of microsteps to move.
        speed : int
            Motor speed, in microsteps per second.
            Values above 1000 are limited to 1000.
        direction : int
            Motor direction. Must be 0 or 1.
    
        Raises
        ------
        ValueError
            If `direction` is not 0 or 1.
        WaterDispenserProtocolError
            If the Arduino does not acknowledge the command correctly.
        """
        if direction not in (0, 1):
            raise ValueError("direction must be 0 or 1")
            
        speed = max(1,min(speed, 40000))
        message = self.query(f'move {distance} {speed} {direction}')
        
        if message != "MOVE STARTED"  :
            raise WaterDispenserProtocolError(f"move didn't work : {message}")
            
    def crawl(self, interval_ms, direction):
        if direction not in (0, 1):
            raise ValueError("direction must be 0 or 1")
            
        interval = int(interval_ms)
        message = self.query(f'crawl {interval} {direction}')
        
        if message != "CRAWL STARTED"  :
            raise WaterDispenserProtocolError(f"move didn't work : {message}")
        
    def get_motion(self):
        """
        Return the current motor movement.
    
        Returns
        -------
        list
            Current movement parameters.
    
            The returned list has one of the following forms::
    
                ["STOP"]
                ["RUN", speed, direction]
                ["MOVE", distance, speed, direction]
    
        Raises
        ------
        WaterDispenserProtocolError
            If the Arduino returns an invalid or malformed response.
        """
        message = self.query("motion")
        split_message = message.split()
        if not split_message[0] == "MOTION" or len(split_message) < 2 :
            raise WaterDispenserProtocolError(f"get_motion didn't return proper message : {message}")
        
        motion = split_message[1]
        
        if motion == "STOP" :
            if len(split_message) != 2:
                raise WaterDispenserProtocolError(
                    f"invalid motion response: {message}"
                )
            return [motion]
        
        elif motion ==  "MOVE" :
            if len(split_message) != 5:
                raise WaterDispenserProtocolError(
                    f"invalid motion response: {message}"
                )
            return [motion,
                    int(split_message[2]),
                    int(split_message[3]),
                    int(split_message[4])]
        
        elif motion == "RUN" :
            if len(split_message) != 4:
                raise WaterDispenserProtocolError(
                    f"invalid motion response: {message}"
                )
            return [motion,
                    int(split_message[2]),
                    int(split_message[3])]
        
        elif motion == "CRAWL":
            if len(split_message) != 4:
                raise WaterDispenserProtocolError(
                    f"invalid motion response: {message}"
                )
            return [motion,
                    int(split_message[2]),
                    int(split_message[3])]
        
        else :
            raise WaterDispenserProtocolError(f"get_motion didnt return proper message : {message}")
            
    def get_pos(self) -> int:
        """
       Return the current motor position.
    
       Returns
       -------
       int
           Current motor position, in microsteps.
    
       Raises
       ------
       WaterDispenserProtocolError
           If the Arduino does not return a valid position response.
       """
        message = self.query("pos")
        
        split_message = message.split()
        
        if not split_message[0] == "POS" or len(split_message) != 2:
            raise WaterDispenserProtocolError(f"get_pos didnt return proper message : {message}")
        
        return int(split_message[1])
    
    
    def query(self, command: str) -> str:
        """
        Send a command to the WaterDispenser Controller and get response.

        Parameters
        ----------
        command : str
            The command to send to the device

        Raises
        ------
        WaterDispenserCommunicationError
        WaterDispenserTimeoutError
        WaterDispenserProtocolError
            
        Returns
        -------
        str
            Message returned by the WaterDispenser

        """
        if not self.connected :
            raise WaterDispenserStateError(f'WaterDispenser should be connected before sending command, connected: {self.connected}')
        with self._comm_lock:
            try:
                # self._serial.reset_input_buffer() # ADD if desynchronisation of answers
                self._serial.reset_output_buffer() # ADD if desynchronisation of answers
                # t.sleep(0.01)
                self._serial.write(command.encode('ascii') + b'\r\n')
                self._serial.flush()
                response = self._serial.readline()
            except OSError as exc:
                raise WaterDispenserCommunicationError(
                    f'Communication failure for the command: {command}') from exc
                
            if not response :
                raise WaterDispenserTimeoutError(
                    f'No response for command {command}')
        
            try :
                return response.decode('ascii').strip()
            except UnicodeDecodeError as exc :
                raise WaterDispenserProtocolError(
                    f"Response not decodable for {command!r}: {response!r}") from exc
                
                
"""
commandes :
    led nb delayMS
    who
    move distance speed direction
    run speed direction
    stop
    pos
    motion
"""