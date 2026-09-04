# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 10:55:10 2025

@author: tbrugiere
"""

import atexit
import serial
from threading import RLock
import time as t

from LS3_acquisition.Hardware.functions_serial_ports import functions_serial_ports as serial_port

serial_port.list_serial_ports()


class StageCommunicationError(RuntimeError):
    "Communication error with the controller"
    
class StageTimeoutError(StageCommunicationError):
    "The controller did not respond in time."
    
class StageProtocolError(StageCommunicationError):
    "Stage response is invalid or unexpected"
    
class StageStateError(KeyError):
    "Stage state is unexpected"
    
class StageControllerError(RuntimeError):
    "Controller reported and error"
    
class StageExecutionError(RuntimeError):
    "Controller accepted the command, but the result is incorrect"
    
class StageMotionError(StageControllerError):
    "Mouvement could not be performed"
    
class Stage_ASI:
    def  __init__ (self,
                   port = 'COM10',
                   model = 'ASI-MS2000-XYBR-ZAR-USB'):
        self.port = port
        self.model = model
        self._serial : serial.Serial | None = None
        self._comm_lock = RLock()
        self._motion_lock = RLock()
        
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
        Change the COM port of the stage controller

        Parameters
        ----------
        port : str
            Name of the COM port of the stage controller 
        """
        if not self.connected :
            self.port = port
            self._serial = None
        else :
            raise StageStateError(f'Stage should not be connexted before changing port connected: {self.connected}')
    
    def get_port(self) -> str:
        """
        Return the port of the stage

        Returns
        -------
        TYPE
            str

        """
        return self.port
    
    @property
    def connected(self):
        """Return whether the serial connection to the stage controller is open."""
        return self._serial is not None and self._serial.is_open
    
    def connect(self) -> None:
        """
        Open and maintain the serial connection to the stage controller.
        
        Any existing serial connection is closed before opening the new one.
        
        Raises
        ------
        StageCommunicationError
            If the serial connection to the controller cannot be opened.
        """
        self.close()
        try :
            self._serial = serial.Serial(
                self.port,
                9600,
                timeout=1,
            )
                
        except OSError as exc:
            raise StageCommunicationError(
                'Error during stage connexion') from exc
            
        if not self.test_port() :
            self.close()
            raise StageCommunicationError(
            f"Device on port {self.port!r} is not the expected "
            f"stage controller ({self.model!r})."
        )
            
    def close(self) -> None:
        """
        Close the serial connection to the stage controller.
        
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
        Check if the port connected is really the stage
        """
        return self.query("WHO")[3:] == self.model
        
    def set_scan(self, SPEED:float, SCANR_start:float, SCANR_stop:float, SCANV_start:float,
                 SCANV_stop:float, SCANV_number_of_lines:float = 1, axis:str = 'X', retrace = 100):
        """
        For the OPM, the sxis MUST be 'X'.
        
        Parameters
        ----------
        SPEED : float
            speed of the fast axis of the stage during scanning in mm/s
        SCANR_start : float
            Start position for the fast axis
        SCANR_stop : float
            stop position for the fast axis
        SCANV_start : float
            Start position for the slow axis
        SCANV_stop : float
            Stop position for the slow axis
        SCANV_number_of_lines : float, optional
            Number of lines of the fast axis
        axis : str, optional
            set the fast axis for scanning, default 'X'

        Returns
        -------
        None.

        """
        if axis not in ("X", "Y"):
            raise ValueError("Stage scanning axis not X or Y : {axis}")
        
        speed = f'{SPEED:.6f}'
        
        commands = ['SCAN X=0 Y=0 Z=0 F=0',
                    f'SCAN X={1 if axis == "X" else 2} Y={1 if axis == "Y" else 2} Z=0 F=0',
                    f'SCANR X={SCANR_start:.6f} Y={SCANR_stop:.6f}  R={retrace}', # Set the start and stop position and the speed for the fast scanning axis
                    f'SCANV X={SCANV_start:.6f} Y={SCANV_stop:.6f} Z={SCANV_number_of_lines:.6f}', # same for the slow axis
                    f'SPEED X={speed if axis == "X" else 5.745920} Y={speed if axis == "Y" else 5.745920}']
        
        for command in commands:
            response = self.query(command)
            if response[0:2] == ':A':
                pass
            else:
                raise StageProtocolError(f"Error command {command}, message {response}")
                
    def start_scan(self):
        """
        Start the scan if it is not running
        """
        if not self.is_moving() :
            response = self.query('SCAN')
            if not response == ":A" :
                raise StageProtocolError(f"ASI stage: scan didn't start: {response}")
        else :
            raise StageStateError("ASI stage is actually moving")
            
    def stop_scan(self):
        """
        Stop the scan if it is running
        """
        
        if self.is_moving():
            response = self.query('SCAN')
            if not response == ":A" :
                raise StageProtocolError(f"ASI stage: scan stop didn't work: {response}")
        else:
            raise StageStateError("ASI stage is not actually moving")
        
    def stop(self):
        """Stop any ongoing stage motion."""
        if not self.connected:
            return
        
        response = self.query('HALT')
        if response not in (":A", ":N-21"):
            raise StageProtocolError(
                f"Unexpected HALT response: {response!r}"
            )
        
    def set_speed(self, x:float=5.745920, y:float=5.745920, z:float=1.286400) :
        """
        Set speed in mm/s of the axis movement (not during scanning)
        Defaults speeds are speeds from factory

        Parameters
        ----------
        x : float, optional
            Speed in mm/s for the X axis, The default is 5.745920.
        y : float, optional
            Speed in mm/s for the Y axis, The default is 5.745920.
        z : float, optional
            Speed in mm/s for the Z axis, The default is 1.286400.
        """
        command = f'S X={x} Y={y} Z= {z}'
        response = self.query(command)
        if response != ":A" :
            raise StageProtocolError(f"Response : {response}")
    
    def get_speed(self):
        """
        Get speed in mm/s of the axis movement (set in set_speed function)

        Raises
        ------
        StageProtocolError
            DESCRIPTION.

        Returns
        -------
        float
            Speed of the X axis in mm/s.
        float
            Speed of the Y axis in mm/s.
        float
            Speed of the Z axis in mm/s.

        """
        response = self.query('S X? Y? Z?')
        str_param = response.split()
        param = [None,None,None]
        if str_param[0] ==":A" :
            try :
                for k in range(3) :
                    param[k] = float(str_param[k+1][2:])
            except :
                raise StageProtocolError(f"Response not expected from the stage: {response}")
        else :
            raise StageProtocolError(f"Response not expected from the stage: {response}, {str_param[0]}")
            
        return param[0], param[1], param[2]
    
    def set_acceleration(self, x:int=100, y:int=100, z:int=70) :
        """
        sets the amount of time in milliseconds that it takes an axis motor speed to go from stopped to the maximum
        (self.set_speed function)
        Defaults speeds are ok defaults from the stage with speed from factory

        Parameters
        ----------
        x : int, optional
            Time in ms fot the X axis, The default is 100.
        y : int, optional
            Time in ms fot the Y axis, The default is 100.
        z : int, optional
            Time in ms fot the Z ais, The default is 70.
        """
        command = f'AC X={x} Y={y} Z= {z}'
        response = self.query(command)
        if response != ":A" :
            raise StageProtocolError(f"Response : {response}")
    
    def get_acceleration(self):
        """
        Get amount of time in milliseconds that it takes an axis motor speed to go from stopped to the maximum
        (set in set_acceleration function)

        Raises
        ------
        StageProtocolError
            DESCRIPTION.

        Returns
        -------
        float
            Time for the X axis in ms.
        float
            Time for the X axis in ms.
        float
            Time for the X axis in ms.

        """
        response = self.query('AC X? Y? Z?')
        response = ":A " + response[1:] # Acceleration starts with ":", not with ":A "
        str_param = response.split()
        param = [None,None,None]
        if str_param[0] ==":A" :
            try :
                for k in range(3) :
                    param[k] = int(str_param[k+1][2:])
            except :
                raise StageProtocolError(f"Response not expected from the stage: {response}")
        else :
            raise StageProtocolError(f"Response not expected from the stage: {response}, {str_param[0]}")
            
        return param[0], param[1], param[2]
    
    def set_backlash(self, x:float = 0.04, y:float = 0.04, z:float = 0.02):
        """
        Sets the amount of distance in millimeters of the anti-backlash move which absorbs the lash
        in the axis' gearing at the end of commanded moves.
        A value of zero (0) disables the anti-backlash algorithm for that axis
        Defaults backlash are ok defaults from factory

        Parameters
        ----------
        x : float, optional
            amount of distance in millimeters for X axis. The default is 0.04.
        y : float, optional
            amount of distance in millimeters for Y axis. The default is 0.04.
        z : float, optional
            amount of distance in millimeters for Z axis. The default is 0.02.

        Raises
        ------
        StageProtocolError
        """
        command = f'B X={x} Y={y} Z= {z}'
        response = self.query(command)
        if response != ":A" :
            raise StageProtocolError(f"Response : {response}")
            
    def get_backlash(self,):
        """
        Get amount of distance in millimeters of the anti-backlash move which absorbs the lash
        in the axis' gearing at the end of commanded moves.
        (set in set_backlash function)

        Raises
        ------
        StageProtocolError
            DESCRIPTION.

        Returns
        -------
        float
            Amount of distance in mm for the X axis.
        float
            Amount of distance in mm for the Y axis.
        float
            Amount of distance in mm for the Z axis.

        """
        response = self.query('B X? Y? Z?')
        response = ":A " + response[1:] # Backlash starts with ":", not with ":A "
        str_param = response.split()
        param = [None,None,None]
        if str_param[0] ==":A" :
            try :
                for k in range(3) :
                    param[k] = float(str_param[k+1][2:])
            except :
                raise StageProtocolError(f"Response not expected from the stage: {response}")
        else :
            raise StageProtocolError(f"Response not expected from the stage: {response}, {str_param[0]}")
            
        return param[0], param[1], param[2]
        
    def go_to_position(self, position = [0.0,0.0,0.0]):
        """
        Go the defined position in µm

        Parameters
        ----------
        position : list of float, optional
            Position to set in X Y Z coordinates in µm. The default is [0.0,0.0,0.0].
        """
        if self._test_positions(position):
            stage_pos = position
            for k in range(3) : stage_pos[k]*= 10 # The command is in 1/10th of microns
            self.send_command(f"M X={stage_pos[0]:.6f} Y={stage_pos[1]:.6f} Z={stage_pos[2]:.6f}", wait_for_motion=True)
        else:
            raise ValueError("[ASI stage]: wrong position argument : {position}")
            
    def move_relative(self, distance = [0.0,0.0,0.0]):
        """
        Move of a relative distance in µm

        Parameters
        ----------
        diatance : list of float, optional
            distance to set in X Y Z coordinates in µm. The default is [0.0,0.0,0.0].
        """
        if self._test_positions(distance):
            stage_dist = distance
            for k in range(3) : stage_dist[k] *= 10 # The command is in 1/10th of microns
            self.send_command(f"R X={stage_dist[0]:.6f} Y={stage_dist[1]:.6f} Z={stage_dist[2]:.6f}", wait_for_motion=True)
        else:
            raise ValueError("[ASI stage]: wrong position argument")
    
    def _test_positions(self, positions):
        """
        Test if the posistions argument is the right type and length

        Parameters
        ----------
        positions : TYPE
            positions argument to test, should be list of 3 float of int

        Returns
        -------
        bool

        """
        """Check that positions contains three numeric coordinates."""
        if not isinstance(positions, (list, tuple)) or len(positions) != 3:
            return False
        
        return all(isinstance(value, (int, float)) for value in positions)
            
    def get_position(self):
        """
        Return the actual position X Y Z of the stage in µm

        Raises
        ------
        NameError
            If the response from the stage is not in the proper format

        Returns
        -------
        TYPE tuple of float
            list of the position in X Y Z order

        """
        response = self.query("W X Y Z")
        str_param = response.split()
        param = [None,None,None]
        if str_param[0] ==":A" :
            try :
                for k in range(3) :
                    param[k] = float(str_param[k+1]) / 10
            except :
                raise StageProtocolError(f"Response not expected from the stage: {response}")
        else :
            raise StageProtocolError(f"Response not expected from the stage: {response}, {str_param[0]}")
            
        return [param[0], param[1], param[2]]
    
    def is_moving(self) -> bool:
        """
        Test if the stage is moving

        Raises
        ------
        StageProtocolError

        Returns
        -------
        bool
            True if the stage is moving

        """
        motion = self.query('STATUS')
        if motion == "B" :
            return True
        elif motion == "N" :
            return False
        else :
            raise StageProtocolError(f"Command STATUS should return MS1 or MS0, actual message : {motion}")
    
    
    def query(self, command: str) -> str:
        """
        Send a command to the Stage Controller and get response.

        Parameters
        ----------
        command : str
            The command to send to the device

        Raises
        ------
        StageCommunicationError
        StageTimeoutError
        StageProtocolError
            
        Returns
        -------
        str
            Message returned by the stage

        """
        if not self.connected :
            raise StageStateError(f'Stage should be connected before sending command, connected: {self.connected}')
        with self._comm_lock:
            try:
                self._serial.write(command.encode('ascii') + b'\r\n')
                t.sleep(0.01)
                response = self._serial.readline()
                t.sleep(0.01)
            except OSError as exc:
                raise StageCommunicationError(
                    f'Communication failure for the command: {command}') from exc
                
            if not response :
                raise StageTimeoutError(
                    f'No response for command {command}')
        
            try :
                return response.decode('ascii').strip()
            except UnicodeDecodeError as exc :
                raise StageProtocolError(
                    f"Response not decodable for {command!r}: {response!r}") from exc
            
    def send_command(self,
                command: str,
                wait_for_motion: bool =  True,
                timeout_s: float = 10.0 ) -> None:
        
        """
        Send a command to the stage controller.
        
        Parameters
        ----------
        command : str
            Command to send to the controller.
        wait_for_motion : bool, optional
            Wait until the stage stops moving after the command.
            The default is True.
        timeout_s : float, optional
            Maximum time in seconds to wait for motion completion.
            The default is 10.0.
        
        Raises
        ------
        StageStateError
            If the controller is not connected.
        StageCommunicationError
            If communication with the controller fails.
        StageControllerError
            If the controller rejects the command.
        StageMotionError
            If the motion does not finish before `timeout_s`.
        """
        if not self.connected :
            raise StageStateError(f'Stage should be connected before sending command, connected: {self.connected}')
        with self._comm_lock:
            try:
                self._serial.write(command.encode('ascii') + b'\r\n')
                t.sleep(0.01)
                response = self._serial.readline().decode('ascii').strip()
                if response != ':A' :
                    # print(f"[Stage] Controller reported and error: {response}")
                    raise StageControllerError(f'Controller reported and error: {response}')
            except OSError as exc:
                raise StageCommunicationError(
                    f'Communication failure for the command: {command}') from exc  
                    
        if wait_for_motion :
            self.wait_for_motion(timeout_s)

            
    def wait_for_motion(self, timeout_s:float = 10.0) -> None:
        """
        Freese the program during the motion

        Parameters
        ----------
        timeout_s : float, optional
            Maximum time that the program wait. The default is 10.0.

        Raises
        ------
        StageMotionError
            
        """
        time_start = t.time()
        while True:
            if not self.is_moving():
                break
            
            if t.time() > (time_start + timeout_s):
                raise StageMotionError(f"Mouvement could not be performed in time {timeout_s}")
                
            t.sleep(0.01)
            
    def __enter__(self):
        self.connect()
        return self
            
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
            
    def __del__(self):
        try:
            self.close()
        except Exception:
            pass