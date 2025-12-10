# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 10:55:10 2025

@author: tbrugiere
"""

from functions_serial_ports import functions_serial_ports as serial_port

serial_port.list_serial_ports()

class Stage_ASI:
    def  __init__ (self, port = 'COM10'):
       self.port = port

    def check_connexion(self):
        return 'ASI_STAGE'
    
    def move_rel(self, x = 0, y = 0, z = 0):
        command = f'R X={x} Y={y} Z= {z}'
        serial_port.send_command(command, self.port)
        
        
        

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
    
"""