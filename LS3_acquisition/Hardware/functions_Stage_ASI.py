# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 10:55:10 2025

@author: tbrugiere
"""

from Hardware.functions_serial_ports import functions_serial_ports as serial_port

serial_port.list_serial_ports()

class Stage_ASI:
    def  __init__ (self, port = 'COM10'):
       self.port = port
       
    def on_init(self):
        self.connection = False
        try:
            response = serial_port.send_command_response("W X Y Z", self.port)
            if response[0:2] == ':A':
                self.connexion = True
            else:
                raise NameError("ASI stage: connection error")
        except:
            raise NameError("ASI stage: connection error")
        
    def set_scan(self, SPEED, SCANR_start:float, SCANR_stop:float, SCANV_start:float,
                 SCANV_stop:float, SCANV_number_of_lines:float = 1, axis:str = 'Y'):
        """
        
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
        if axis != 'X' or axis != 'Y' :
            raise NameError("ASI stage: scanning axis not X or Y")
            
        scan = f'SCAN X={1 if axis == "X" else 2} Y={1 if axis == "Y" else 2} Z=0 F=0'
        
        commands = ['SCAN X=0 Y=0 Z=0 F=0',
                    scan,
                    f'SCANR X={SCANR_start} Y={SCANR_stop}', # Set the start and stop position for the fast scanning axis
                    f'SCANV X={SCANV_start} Y={SCANV_stop} Z={SCANV_number_of_lines}', # same for the slow axis
                    f'SPEED X={SPEED}'] # Set the speed for the fast scanning axis
        
        for command in commands:
            response = serial_port.send_command_response(command, self.port)
            if response[0:2] == ':A':
                pass
            else:
                raise NameError(f"ASI stage: Error command {command}, message {response}")
                
    def start_scan(self):
        """
        Star the scan if it is not running, stop ifit is

        Returns
        -------
        None.

        """
        if not self._is_moving() :
            response = serial_port.send_command_response('SCAN', self.port)
            if not response == ":A" :
                raise NameError(f"ASI stage: scan didn't start: {response}")
        else :
            raise NameError("ASI stage is actually moving")
            
    def stop_scan(self):
        if self._is_moving():
            response = serial_port.send_command_response('SCAN')
            if not response == ":A" :
                raise NameError(f"ASI stage: scan stop didn't work: {response}")
        
    def stop(self):
        """
        Stop the actual motion and print a message saying of the stage was on motion
        or not
        """
        
        response = serial_port.send_command_response('HALR', self.port)
        if response == ":A" :
            print("ASI stage: no movement")
        elif response == ":N-21":
            print("ASI stage: movement interupted")
        
    def set_speed(self, x=5.745920, y=5.745920, z=1.286400) :
        command = f'S X={x} Y={y} Z= {z}'
        serial_port.send_command(command, self.port)
    
    def _is_moving(self):
        response = serial_port.send_command_response("STATUS", self.port)
        if response == "N" :
            return False
        elif response == "B" :
            return True
        else : 
            return None
    
"""
ACCEL :
    sets the amount of time in milliseconds that it takes an axis motor speed to go from stopped to the maximum speed
    AC X? Y? Z? => :X=101 Y=101 Z=71 A
    
HOME :
    ! X Y Z
    
    Set the position to the actual absolute possition
    H X=-318128 Y=-547732 Z=0
    
MOVE : Move to an absolute position M X Y move to the origin
    M X=-2000 Y=-2000 Z=0
    
MOVREL :
    move to a relative position
    R X=-2000 Y=-2000 Z=1000
SPEED :
    get or set the speed of the stage
    S X? Y? Z? => X=5.745920 Y=5.745920 Z=1.286400
    S Y = 0.5
    
VERSION :
    get the version of the firmware
    V => :A Version: USB-9.53
    
WHERE :
 	Sets the origin of the coordinate system for the specified axis
     
STATUS : get the motion statuf of the stage
    N - Not Busy: there are no motors running from a serial command
    B - Busy: there is at least one motor running from a serial command 
    
"""