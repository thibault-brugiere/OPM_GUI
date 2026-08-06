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
    
class PiezoProtolError(PiezoCommunicationError):
    "Controller response is invalid or unexpected"
    
class PiezoStateError(KeyError):
    "Piezo state is unexpected"
    
class PiezoControllerError(RuntimeError):
    "Controller reported and error"
    
class PiezoEcecutionError(RuntimeError):
    "Controller accepted the command, but the result is incorrect"
    
class PiezoMotionError(PiezoControllerError):
    "Mouvement could not be performed"
    

class piezo_SAS() : #SAS for Super Agilis Series
    """
    Control the piezo Super Agilis Series from MKS Newport
    """
    def __init__(self, port = 'COM6'):
        self.port = port
        
    def change_port(self, port: str):
        """
        Change the COM port of the piezo controller

        Parameters
        ----------
        port : str
            Name of the COM port of the piezo controller 
        """
        self.port = port
        
    def get_position(self):
        """

        Raises
        ------
        PiezoEcecutionError

        Returns
        -------
        float
            Actual position of the piezo

        """
        pos = self.query("TP?")
        try :
            return float(pos[2:])
        except :
            raise PiezoEcecutionError(
                f"Piezo could not report the position : {pos}")
        
    
    def test_position(self, position: float, tolerance: float  = 0.0001):
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
        if abs(actual_position - position) < tolerance:
            return True
        else :
            return False
        
    def open_loop(self):
        """
        Turn the piezo controller in open_loop mode,
        controller needs to be in close loop mode

        Raises
        ------
        PiezoEcecutionError
            
        PiezoStateError

        """
        if self.get_status() == PiezoState.READY_CL :
            self.send_command("OL", wait_for_motion = False)
            if not self.get_status() == PiezoState.READY_OL :
                raise PiezoEcecutionError(
                    f"Controller could not set to open loop : {self.get_status()}")
        else :
            raise PiezoStateError(f"Controller should be in READY_CL state: {self.get_status()}")
    
    def close_loop(self):
        """
        Turn the piezo controller in close loop mode,
        controller needs to be in open loop mode

        Raises
        ------
        PiezoEcecutionError
            
        PiezoStateError

        """
        if self.get_status() == PiezoState.READY_OL :
            self.send_command("OR", wait_for_motion = False)
            if not self.get_status() == PiezoState.READY_CL :
                raise PiezoEcecutionError(
                    f"Controlller cound not set to close loop : {self.get_status()}")
        else :
            raise PiezoStateError(f"Controller should be in READY_OL state: {self.get_status()}")
        
    def reference(self, move_back: bool = True):
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
        PiezoEcecutionError
            
        PiezoStateError
            
        """
        if self.get_status() == PiezoState.READY_CL :
            if move_back :
                position = self.get_position()
                self.send_command("RFP")
                self.wait_for_motion(15.0)
                if not self.test_position(position):
                    raise PiezoEcecutionError(f"Unexpected position after referencing : {position} / {self.get_position()}")
            else :
                self.send_command("RFH")
                self.wait_for_motion(10.0)
            
            if not self.is_referenced() :
                raise PiezoEcecutionError("Controller not referenced after referencing")
            if not self.get_status() == PiezoState.READY_CL:
                raise PiezoEcecutionError("Controller not in READY_CL after referencing")
            
        else :
            raise PiezoStateError(f"Controller should be in READY_CL state: {self.get_status()}")
            
                
    def is_referenced(self):
        """
        Check if the controler is already referenced

        Returns
        -------
        bool
            True if the controller is already referenced

        """
        if self.query("RFS?") == "RFS1":
            return True
        else :
            return False

    
    def move_by(self, step: float):
        """
        Move the piezo by a certan distance. Controler should be in READY_CL mode

        Parameters
        ----------
        step : float
            Distance in mm to move the piezo

        Raises
        ------
        PiezoEcecutionError
            
        PiezoStateError
            
        """
        if self.get_status() == PiezoState.READY_CL:
            position = self.get_position()
            step_str = str(step)[:7]
            command = f"XR{step_str}"
            self.send_command(command)
            
            if not self.test_position(position + step) :
                raise PiezoEcecutionError(f"Unexpected position after relative movement : {position + step} / {self.get_position()}")
        else :
            raise PiezoStateError(f"Controller should be in READY_CL state: {self.get_status()}")
        
    def move_to(self, position:float):
        """
        Move the piezo to a certan position. Controler should be in READY_CL mode

        Parameters
        ----------
        position : float
            Position to move the piezo in mm

        Raises
        ------
        PiezoEcecutionError
            DESCRIPTION
        PiezoStateError
            
        """
        if self.get_status() == PiezoState.READY_CL:
            position_str = str(position)[:7]
            command = f"PA{position_str}"
            self.send_command(command)
            
            if not self.test_position(float(position)):
                raise PiezoEcecutionError(f"Unexpected position after movement : {position} / {self.get_position()}")
        else :
            raise PiezoStateError(f"Controller should be in READY_CL state: {self.get_status()}")
            
    def step_move(self, steps:int):
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
        if self.get_status() == PiezoState.READY_OL:
            steps = math.trunc(steps)
            command = f"XR{steps}"
            self.send_command(command)
        else:
            raise PiezoStateError(f"Controller should be in READY_OL state: {self.get_status()}")

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
        code = self.query('TS')
        try :
            return STATUS_BY_CODE.get(code[-2:])
        except KeyError as exc:
            raise PiezoStateError(
                f"Unexpected PiezoState: {code}") from exc   
            
    def is_moving(self) -> bool:
        """
        Test if the piezo is moving

        Raises
        ------
        PiezoProtolError

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
            raise PiezoProtolError(f"Command MS should return MS1 or MS0, actual message : {motion}")


    def stop_motion(self):
        """
        Stop the actual motion of the piezo

        Raises
        ------
        PiezoCommunicationError
            
        """
        try:
            with serial.Serial(self.port, 9600, timeout=1) as ser:
                ser.write("ST".encode('ascii') + b'\r\n')
                t.sleep(0.01)
        except OSError as exc:
            raise PiezoCommunicationError(
                'Communication failure for the command: ST') from exc  
            
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
        PiezoProtolError
            
        Returns
        -------
        str
            Message returned by the piezo

        """
        try:
            with serial.Serial(self.port, 9600, timeout=1) as ser:
                ser.write(command.encode('ascii') + b'\r\n')
                t.sleep(0.01)
                response = ser.readline()
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
            raise PiezoProtolError(
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
        try:
            with serial.Serial(self.port, 9600, timeout=timeout_s) as ser:
                ser.write(command.encode('ascii') + b'\r\n')
                t.sleep(0.01)
        except OSError as exc:
            raise PiezoCommunicationError(
                f'Communication failure for the command: {command}') from exc  
                
        if wait_for_motion :
            self.wait_for_motion(timeout_s)
             
        error = self.query('TB')
        if error != 'TB@ No error' :
            raise PiezoControllerError(f'Controller reported and error: {error}')
            
    def wait_for_motion(self, timeout_s:float = 10.0):
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