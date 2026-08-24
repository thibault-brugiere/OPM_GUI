# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 15:38:45 2026

@author: tbrugiere
"""
from enum import Enum, auto
import math
import time as t
import serial
import serial.tools.list_ports
from threading import RLock

class PiezoState(Enum):
    NONE = auto()
    READY_OL = auto()
    READY_CL = auto()
    CONFIGURATION = auto()
    HOMING = auto()
    REFERENCING = auto()
    MOVING = auto()
    DISABLE = auto()
    JOGGING = auto()
    SCANNING = auto()
    HOLDING = auto()
    ERROR = auto()
    

#
# Convert status send by the piezo controller after command ST into PiezoState
#

STATUS_BY_CODE: dict[str, PiezoState] = {
    "0A": PiezoState.READY_OL,
    "0B": PiezoState.READY_OL,
    "0C": PiezoState.READY_OL,
    "0D": PiezoState.READY_OL,
    "0E": PiezoState.READY_OL,
    "0F": PiezoState.READY_OL,
    "10": PiezoState.READY_OL,
    "11": PiezoState.READY_OL,
    "32": PiezoState.READY_CL,
    "33": PiezoState.READY_CL,
    "34": PiezoState.READY_CL,
    "35": PiezoState.READY_CL,
    "36": PiezoState.READY_CL,
    "14": PiezoState.CONFIGURATION,
    "1E": PiezoState.HOMING,
    "1F": PiezoState.REFERENCING,
    "28": PiezoState.MOVING,
    "29": PiezoState.MOVING,
    "3C": PiezoState.DISABLE,
    "3D": PiezoState.DISABLE,
    "46": PiezoState.JOGGING,
    "50": PiezoState.SCANNING,
    "5A": PiezoState.HOLDING,
}

class PiezoCommunicationError(RuntimeError):
    "Communication error with the controller"
    
class PiezoTimeoutError(PiezoCommunicationError):
    "The controller did not respond in time."
    
class PiezoProtocolError(PiezoCommunicationError):
    "Controller response is invalid or unexpected"
    
class PiezoStateError(KeyError):
    "Piezo state is unexpected"
    
class PiezoControllerError(RuntimeError):
    "Controller reported and error"
    
class PiezoExecutionError(RuntimeError):
    "Controller accepted the command, but the result is incorrect"
    
class PiezoMotionError(PiezoControllerError):
    "Mouvement could not be performed"
    

class piezo_SAS() : #SAS for Super Agilis Series
    """
    Control the piezo Super Agilis Series from MKS Newport
    """
    def __init__(self, port = 'COM6',
                 model = 'IDCONEX-SAG-LS16P',
                 min_position = 0.0,
                 max_position = 15.9):
        self.port = port
        self.model = model
        self._serial : serial.Serial | None = None
        self.position = 0.0
        self.min_position:float = min_position
        self.max_position: float = max_position
        self._comm_lock = RLock()
        self._motion_lock = RLock()
        
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
        Change the COM port of the piezo controller

        Parameters
        ----------
        port : str
            Name of the COM port of the piezo controller 
        """
        if not self.connected :
            self.port = port
            self._serial = None
        else :
            raise PiezoStateError(f'Piezo should not be connexted before changing port connected: {self.connected}')
    
    def get_port(self) -> str:
        """
        Return the port of the piezo

        Returns
        -------
        TYPE
            str

        """
        return self.port
    
    @property
    def connected(self) -> bool:
        """Return whether the serial connection to the piezo controller is open."""
        return self._serial is not None and self._serial.is_open
        
    def connect(self) -> None:
        """
        Open and maintain the serial connection to the piezo controller.
        
        Any existing serial connection is closed before opening the new one.
        
        Raises
        ------
        PiezoCommunicationError
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
            raise PiezoCommunicationError(
                'Error during piezo connexion') from exc
            
        if not self.test_port() :
            self.close()
            raise PiezoCommunicationError(
            f"Device on port {self.port!r} is not the expected "
            f"piezo controller ({self.model!r})."
        )
        
    def close(self) -> None:
        """
        Close the serial connection to the piezo controller.
        
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
        Check if the port connected is really the piezo
        """
        return self.query("ID?") == self.model

    def get_status(self) -> PiezoState:
        """
        Get the status of the piezo controller

        Raises
        ------
        PiezoStateError

        Returns
        -------
        PiezoState
            status of the piezo controller
        """
        response = self.query('TS')
        code = response[-2:]
        try :
            return STATUS_BY_CODE.get(code)
        except KeyError as exc:
            raise PiezoStateError(
                f"Unexpected PiezoState: {response!r}") from exc   
        
    def get_position(self) -> float:
        """
        To avoid conflict woth other 
        Raises
        ------
        PiezoExecutionError

        Returns
        -------
        float
            Actual position of the piezo

        """
        response = self.query("TP?")
        try :
            position = float(response[2:])
        except (ValueError, IndexError) as exc:
            raise PiezoExecutionError(
                f"Piezo could not report the position : {response}") from exc
            
        self.position = position
        return position
        
    def try_get_position(self) -> float | None:
        """
        Return the current piezo position if communication is available.
    
        Returns
        -------
        float | None
            Current position, or None if the piezo communication is busy.
        """
        if not self._comm_lock.acquire(blocking=False):
            return None
    
        try:
            return self.get_position()
        finally:
            self._comm_lock.release()
        
    
    def test_position(self, position: float, tolerance: float  = 0.00015) -> bool:
        """
        Compare the actual position of the piezo with another position

        Parameters
        ----------
        position : float
            Position to compare with the position of the piezo (in mm)
        tolerance : float, optional
            Tolerance of the comparision (in mm). The default is 0.0001.

        Returns
        -------
        bool
            Return true if the difference between the positions in less than the
            tolerance

        """
        actual_position = self.get_position()
        return abs(actual_position - position) < tolerance
        
    def open_loop(self) -> None:
        """
        Turn the piezo controller in open_loop mode,
        controller needs to be in close loop mode

        Raises
        ------
        PiezoExecutionError
            
        PiezoStateError

        """
        status = self.get_status()
        if status == PiezoState.READY_CL :
            self.send_command("OL", wait_for_motion = False)
            status =self.get_status()
            if status != PiezoState.READY_OL :
                raise PiezoExecutionError(
                    f"Controller could not set to open loop : {status}")
        else :
            raise PiezoStateError(f"Controller should be in READY_CL state: {status}")
    
    def close_loop(self) -> None:
        """
        Turn the piezo controller in close loop mode,
        controller needs to be in open loop mode

        Raises
        ------
        PiezoExecutionError
            
        PiezoStateError

        """
        status = self.get_status()
        if status == PiezoState.READY_OL :
            self.send_command("OR", wait_for_motion = False)
            status = self.get_status()
            if status != PiezoState.READY_CL :
                raise PiezoExecutionError(
                    f"Controlller cound not set to close loop : {status}")
        else :
            raise PiezoStateError(f"Controller should be in READY_OL state: {status}")
        
    def reference(self, move_back: bool = True) -> None:
        """
        Reference the piezo controller

        Parameters
        ----------
        move_back : bool, optional
            if True, Move to mechanical end of run, take this position as reference,
            and move back to previous position.
            If False, stay to the end of run. The default is True.

        Raises
        ------
        PiezoExecutionError
            
        PiezoStateError
            
        """
        status = self.get_status()
        if status == PiezoState.READY_CL :
            if move_back :
                self.send_command("RFP", timeout_s = 15.0)
                t.sleep(0.01)
                self.wait_for_motion(10.0) # Wait for motion needs to be restarted for proper waiting, I have no idea why
            else :
                self.send_command("RFH")
            
            if not self.is_referenced() :
                raise PiezoExecutionError("Controller not referenced after referencing")
            status = self.get_status()
            if not status == PiezoState.READY_CL:
                raise PiezoExecutionError(f"Controller not in READY_CL after referencing: {status}")
            
        else :
            raise PiezoStateError(f"Controller should be in READY_CL state: {status}")
            
                
    def is_referenced(self) -> bool:
        """
        Check if the controler is already referenced

        Returns
        -------
        bool
            True if the controller is already referenced

        """
        return self.query("RFS?") == "RFS1"

    
    def move_by(self, step: float) -> None:
        """
        Move the piezo by a certan distance. Controler should be in READY_CL mode

        Parameters
        ----------
        step : float
            Distance in mm to move the piezo

        Raises
        ------
        PiezoExecutionError
            
        PiezoStateError
            
        """
        with self._motion_lock:
            position = self.get_position()
            target_position = position+ step
            if not self.min_position <= target_position <= self.max_position:
                raise ValueError(
                    f"Position {target_position} mm outside "
                    f"[{self.min_position}, {self.max_position}] mm"
                )
            status = self.get_status()
            if status == PiezoState.READY_CL:
                step_str = f'{step:.6f}'
                command = f"PR{step_str}"
                self.send_command(command)
                
                if not self.test_position(target_position) :
                    raise PiezoExecutionError(f"Unexpected position after relative movement : {target_position:.6f} / {self.get_position()}")
            else :
                raise PiezoStateError(f"Controller should be in READY_CL state: {status}")
        
        
    def move_to(self, position:float) -> None:
        """
        Move the piezo to a certan position. Controler should be in READY_CL mode

        Parameters
        ----------
        position : float
            Position to move the piezo in mm

        Raises
        ------
        PiezoExecutionError
            DESCRIPTION
        PiezoStateError
            
        """
        with self._motion_lock:
            if not self.min_position <= position <= self.max_position:
                raise ValueError(
                    f"Position {position} mm outside "
                    f"[{self.min_position}, {self.max_position}] mm"
                )
            status = self.get_status()
            if status == PiezoState.READY_CL:
                position_str = f"{position:.6f}"
                command = f"PA{position_str}"
                self.send_command(command)
                
                if not self.test_position(float(position)):
                    raise PiezoExecutionError(f"Unexpected position after movement : {position} / {self.get_position()}")
            else :
                raise PiezoStateError(f"Controller should be in READY_CL state: {status}")
            
    def step_move(self, steps:int) -> None:
        """
        Mothe the piezo by a certain number of steps. Controller should be in ready_OL mode

        Parameters
        ----------
        steps : int
            Number of steps to move the piezo

        Raises
        ------
        PiezoStateError
            
        """
        status = self.get_status()
        if status == PiezoState.READY_OL:
            steps = math.trunc(steps)
            command = f"XR{steps}"
            self.send_command(command, wait_for_motion = False) # To go a bit faster
        else:
            raise PiezoStateError(f"Controller should be in READY_OL state: {status}")
            
    def set_frequency(self, frequency:int) -> None:
        """
        Modify the stepping frequency

        Parameters
        ----------
        frequency : int
            Frequency to set to the contoller.
            
        Raises
        ------
        PiezoStateError
        """
        status = self.get_status()
        if status == PiezoState.READY_OL:
            frequency = int(frequency)
            command = f"XF{frequency}"
            self.send_command(command)
        else:
            raise PiezoStateError(f"Controller should be in READY_OL state: {status}")
            
    def get_frequency(self) -> int :
        frequency = self.query("XF?")
        try :
            return int(frequency[2:])
        except :
            raise PiezoProtocolError(f"Freqency is not in the right format : {frequency}")
        
            
    def set_step_size(self, neg_step:int, pos_step:int) -> None:
        """
        Change the current open loop step size

        Parameters
        ----------
        neg_step : int
            Negative Step size (should be a positive number).
        pos_step : TYPE
            Positive Step size.

        Raises
        ------
        PiezoStateError
            
        """
        status = self.get_status()
        if status == PiezoState.READY_OL:
            command = f"XU-{neg_step},{pos_step}"
            self.send_command(command)
        else:
            raise PiezoStateError(f"Controller should be in READY_OL state: {status}")
            
    def get_step_size(self) -> tuple[int, int]:
        """
        Get the current open loop step size

        Raises
        ------
        PiezoProtocolError

        Returns
        -------
        tuple(int, int)
            negative and positive step size (both positives numbers).

        """
        message = self.query("XU?")
        try :
            steps_size = message[3:].split(",")
            neg_step = int(steps_size[0])
            pos_step = int(steps_size[1])
            return neg_step, pos_step
        except:
            raise PiezoProtocolError(f"step size is not in the right format : {message}")
            
    def is_moving(self) -> bool:
        """
        Test if the piezo is moving

        Raises
        ------
        PiezoProtocolError

        Returns
        -------
        bool
            True if the piezo is moving

        """
        motion = self.query('MS')
        if motion == "MS1" :
            return True
        elif motion == "MS0" :
            return False
        else :
            raise PiezoProtocolError(f"Command MS should return MS1 or MS0, actual message : {motion}")


    def stop_motion(self) -> None:
        """
        Stop the actual motion of the piezo

        Raises
        ------
        PiezoCommunicationError
            
        """
        with self._comm_lock :
            if not self.connected:
                raise PiezoStateError("Piezo is not connected.")
                
            try:
                self._serial.write(b"ST\r\n")
            except OSError as exc:
                raise PiezoCommunicationError(
                    "Communication failure for command 'ST'"
                ) from exc
            
    def query(self, command: str) -> str:
        """
        Send a command to the Super Agilis Controller and get response.

        Parameters
        ----------
        command : str
            The command to send to the device

        Raises
        ------
        PiezoCommunicationError
        PiezoTimeoutError
        PiezoProtocolError
            
        Returns
        -------
        str
            Message returned by the piezo

        """
        if not self.connected :
            raise PiezoStateError(f'Piezo should be connected before sending command, connected: {self.connected}')
        with self._comm_lock:
            try:
                self._serial.write(command.encode('ascii') + b'\r\n')
                t.sleep(0.01)
                response = self._serial.readline()
                t.sleep(0.01)
            except OSError as exc:
                raise PiezoCommunicationError(
                    f'Communication failure for the command: {command}') from exc
                
            if not response :
                raise PiezoTimeoutError(
                    f'No response for command {command}')
        
            try :
                return response.decode('ascii').strip()
            except UnicodeDecodeError as exc :
                raise PiezoProtocolError(
                    f"Response not decodable for {command!r}: {response!r}") from exc
            
    def send_command(self,
                command: str,
                wait_for_motion: bool =  True,
                timeout_s: float = 1.0 ) -> None:
        """
        Send a command to the piezo

        Parameters
        ----------
        command : str
            Command to send to the piezo
        wait_for_motion : bool, optional
            If the program should wait for the motion to finish. The default is True.
        timeout_s : float, optional
            Timeout for the piezo connexion. The default is 1.0.

        Raises
        ------
        PiezoCommunicationError
        PiezoControllerError

        """
        if not self.connected :
            raise PiezoStateError(f'Piezo should be connected before sending command, connected: {self.connected}')
        with self._comm_lock:
            try:
                self._serial.write(command.encode('ascii') + b'\r\n')
                t.sleep(0.01)
            except OSError as exc:
                raise PiezoCommunicationError(
                    f'Communication failure for the command: {command}') from exc  
                    
        if wait_for_motion :
            self.wait_for_motion(timeout_s)
             
        error = self.query('TB')
        if error != 'TB@ No error' :
            raise PiezoControllerError(f'Controller reported and error: {error}')
            
    def wait_for_motion(self, timeout_s:float = 10.0) -> None:
        """
        Freese the program during the motion

        Parameters
        ----------
        timeout_s : float, optional
            Maximum time that the program wait. The default is 10.0.

        Raises
        ------
        PiezoMotionError
            
        """
        time_start = t.time()
        while True:
            if not self.is_moving():
                break
            
            if t.time() > (time_start + timeout_s):
                raise PiezoMotionError(f"Mouvement could not be performed in time {timeout_s}")
                
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