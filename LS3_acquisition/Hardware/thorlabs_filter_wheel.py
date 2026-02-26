# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 14:22:23 2025

@author: tbrugiere
"""

from math import fmod
import os
import clr
import sys
from System import Enum, Decimal
import time

# Point to the Kinesis DLLs
sys.path.append(r"C:\Program Files\Thorlabs\Kinesis")

# Load the assemblies (order matters)
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")
clr.AddReference("Thorlabs.MotionControl.KCube.StepperMotorCLI")

# Imports from the assemblies
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.KCube.StepperMotorCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import Settings as GMSettings


TrigMode = GMSettings.KCubeTriggerConfigSettings.TriggerPortMode
TrigPol  = GMSettings.KCubeTriggerConfigSettings.TriggerPolarity
# Simple polarity alias map (keeps code resilient across DLL variants)
_pol_alias  = {"TriggerHigh": ["TrigIN_High","TrigIN_Rising","High","ActiveHigh",
                                  "TrigOUT_High","TrigOUT_ActiveHigh","High","ActiveHigh"],
                  "TriggerLow":  ["TrigIN_Low","TrigIN_Falling","Low","ActiveLow",
                                  "TrigOUT_Low","TrigOUT_ActiveLow","Low","ActiveLow"]}


def _enum_from_name(enum_type, name, aliases=None):
    """
    Resolve a .NET enum value from a string, with optional alias fallback and
    case-insensitive matching.
    """
    names = set(Enum.GetNames(enum_type))
    if name in names:
        return getattr(enum_type, name)
    # alias optionnels : {'TriggerHigh': ['TrigIN_High','High','ActiveHigh'], ...}
    if aliases and name in aliases:
        for cand in aliases[name]:
            if cand in names:
                return getattr(enum_type, cand)
    # petite aide si l’utilisateur a mis une casse différente
    for cand in names:
        if cand.lower() == name.lower():
            return getattr(enum_type, cand)
    raise ValueError(f"'{name}' is not a valid member of {enum_type.__name__}. "
                     f"Valid: {sorted(names)}")

class ThorlabsFW103():
    """
    Thin convenience wrapper around a Thorlabs FW103M filter wheel driven by a KST201
    KCube Stepper. Provides slot-based moves (6 slots @ 60°), trigger setup, and
    basic velocity/home operations.
    """
    
    def __init__(self, serial_no = "26007018", simulation = False):
        """
        Initialize the wrapper (does not connect yet).

        Parameters
        ----------
        serial_no : str
            KST201 serial number.
        simulation : bool
            If True, initialize Kinesis simulation (no real hardware required).
        """
        
        self.serial_no = serial_no
        self.simulation = simulation
        self.nSlots = 6
        self.connected = False
        self.angle = None
        self.changing_time = [55,70,85] # Time to change 1, 2 or 3 position in ms
        
        self.on_init()
        
        self.move = 1
    
    def on_init(self):
        """
        Internal: build the device list, create the device instance, and
        optionally enable Kinesis simulation.
        """
        
        pass

    # ---------- Lifecycle ----------
        
    def connect(self, polling_ms=250):
        """
        Connect to the device, start polling, enable the drive and load settings.

        Parameters
        ----------
        polling_ms : int
            Polling interval in milliseconds. Lower values give snappier 'move completed'
            detection (e.g. 50 ms), at the cost of more USB traffic.
        use_file_settings : bool
            If True, load 'UseFileSettings'. Otherwise uses 'UseDeviceSettings'.
        """
        try:
            if self.simulation :
                SimulationManager.Instance.InitializeSimulations()
            
            DeviceManagerCLI.BuildDeviceList()
            self.device = KCubeStepper.CreateKCubeStepper(self.serial_no)
            
            self.device.Connect(self.serial_no)
            time.sleep(0.25)  # wait statements are important to allow settings to be sent to the device
            
            
            self.device.StartPolling(int(polling_ms))  #250ms polling rate
            time.sleep(0.25)
            self.device.EnableDevice()
            time.sleep(0.25)  # Wait for device to enable
            
            
            self.use_file_settings = DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings
            self.device_config = self.device.LoadMotorConfiguration(self.device.DeviceID, self.use_file_settings)
            
            # Get trigger container from device after connect
            # Apply config config (API recent of hold)
            if hasattr(self.device, "GetKCubeTriggerConfigParams"):
                self.trig = self.device.GetKCubeTriggerConfigParams()
            else: self.trig = self.device.GetTriggerConfigParams()
            
            self.connected = True
            self.angle = self.getAngle()
            print("[OK] FW103 connected")
        except:
            print('[FW103]: Connection failed, check not connected from another program (Kinesis GUI)')    
        
    def close(self):
        """
        Stop polling, disconnect the device, and tear down simulation if enabled.
        Safe to call multiple times.
        """
        try:
            self.device.StopPolling()
        except Exception:
            pass
        try:
            self.device.Disconnect()
        except Exception:
            pass
        self.connected = False
        
        try:
            self.device.Dispose()
        except Exception:
            pass
        
        if self.simulation:
            SimulationManager.Instance.UninitializeSimulations()
            
    # ---------- Info / basic ops ----------
        
    def printInfos(self):
        """
        Print human-readable device info and current homing velocity.
        """
        
        self.device_info = self.device.GetDeviceInfo()
        print(self.device_info.Description)
        
    def home(self):
        """
        Home the axis to the index sensor.

        Parameters
        ----------
        timeout_ms : int
            Move timeout in milliseconds.
        """
        print("[FW103]: Homing Motor...")
        self.device.Home(60000)  # 60 seconds
        print("[FW103]: Motor Homed.")
        
        self.angle = self.getAngle()
    
    # ---------- Angles & slots ----------
    
    def getAngle(self):
        """
        Read the current angle (in degrees) from the controller.

        Returns
        -------
        float
            angle.
        """
        return Decimal.ToDouble(self.device.Position)
    
    def getSlot(self, tolerance = 5.0):
        """
        Estimate the current slot index (0..5) by rounding the modulo angle to 60° steps.

        Parameters
        ----------
        tolerance : float
            Allowed angular deviation (degrees) around the nominal slot position before
            printing a warning.

        Returns
        -------
        int
            Slot index in [0..5].
        """
        self.angle = self.getAngle()
        step = 360.0 / self.nSlots
        
        slot = int(round(self.angle / step))
        error = abs(slot * step - self.angle)
        if error > tolerance :
            print(f"[FW103] Warning: angle {self.angle:.2f}° is {error:.2f}° away from slot {slot}.")
        return slot
    
    def setSlot(self, slot, timeout_ms=5000):
        """
        Move to the given slot (0..5). By default, chooses the shortest rotation.

        Parameters
        ----------
        slot : int
            Target slot index (0..5).
        shortest : bool
            If True, compute nearest absolute target to minimize rotation.
        timeout_ms : int
            Move timeout in milliseconds.
        """
        if int(slot) == slot:
            if 0 <= slot <= self.nSlots-1:
                step = 360.0 / self.nSlots
                pos = Decimal(slot * step)
                self.device.MoveTo(pos, timeout_ms)
                self.angle = self.getAngle()
            else:
                print(f"[FW103] 'slot' must be in [0, {self.nSlots}]. Got: {slot}")
        else:
            print(f"[FW103] 'slot' must an integer. Got: {slot}")
        
    # ---------- Triggers ----------
    
    def _apply_trig(self):
        """
        Push the trigger configuration back to the device, handling both old/new APIs.
        """
        if hasattr(self.device, "SetKCubeTriggerConfigParams"):
            self.device.SetKCubeTriggerConfigParams(self.trig)
        else:
            self.device.SetTriggerConfigParams(self.trig)
            
    """
    avaliableTriggerPortMode =  ['Disabled', 'TrigIN_GPI', 'TrigIN_RelativeMove', 'TrigIN_AbsoluteMove',
                                 'TrigIN_Homed', 'TrigIN_Stop', 'TrigIN_ScanStart', 'TrigIN_ShuttleMove',
                                 'TrigOUT_GPO', 'TrigOUT_InMotion', 'TrigOUT_AtMaxVelocity',
                                 'TrigOUT_AtPositionFwd', 'TrigOUT_AtPositionRev', 'TrigOUT_AtPositionBoth',
                                 'TrigOut_AtFwdLimit', 'TrigOut_AtBwdLimit', 'TrigOut_AtLimit']
    avaliableTriggerPolarity =  ['TriggerHigh', 'TriggerLow']
    """
        
    def setTrigger1(self, mode, polarity = 'TriggerHigh '):
        """
        Configure TRIG1 (input) mode and polarity.

        Parameters
        ----------
        mode : str
            Trigger mode name, e.g. 'TrigIN_RelativeMove' or 'TrigIN_AbsoluteMove'.
        polarity : str
            Polarity string, typically 'TriggerHigh' or 'TriggerLow'.
            Note: TrigIN_AbsoluteMove seems that it makes the wheel rotate forever
        """
        mode_enum = _enum_from_name(TrigMode, mode)
        pol_enum  = _enum_from_name(TrigPol, polarity, aliases=_pol_alias)
        
        self.trig.Trigger1Mode     = mode_enum
        self.trig.Trigger1Polarity = pol_enum
        self._apply_trig()
    
    def setTrigger2(self, mode, polarity = 'TriggerHigh'):
        """
        Configure TRIG2 (output) mode and polarity.

        Parameters
        ----------
        mode : str
            Trigger mode name, e.g. 'TrigOUT_InMotion' or 'TrigOUT_AtTarget'.
        polarity : str
            Polarity string, typically 'TriggerHigh' or 'TriggerLow'.
        """
        
        mode_enum = _enum_from_name(TrigMode, mode)
        pol_enum  = _enum_from_name(TrigPol, polarity, aliases=_pol_alias)
        self.trig.Trigger2Mode     = mode_enum
        self.trig.Trigger2Polarity = pol_enum
        self._apply_trig()
    
    def setTriggerForMicroscope(self):
        """
        Convenience: TRIG1 = RelativeMove (active-high pulse), TRIG2 = InMotion (active-high).
        Remember to set an relative target BEFORE sending a TRIG1 pulse.
        """
        
        self.setTrigger1('TrigIN_RelativeMove', 'TriggerHigh')
        self.setTrigger2('TrigOUT_InMotion', 'TriggerHigh')
    
    def setRelativeStep(self, degrees: float):
        """
        Set the default relative move distance used by RelativeMove and some TRIG1 modes.

        Parameters
        ----------
        degrees : float
            Relative distance in degrees (e.g. 60, 120, 180). Some DLLs ignore TRIG
            'RelativeMoveDistance' and use this device-wide value instead.
        """
        self.device.SetMoveRelativeDistance(Decimal(degrees))
        
    def setAbsoluteStep(self, pos: float):
        """
        Set the absolute target (0..360) for the next AbsoluteMove or TRIG1 AbsoluteMove.

        Parameters
        ----------
        pos : float
            Absolute angle in degrees. Must be in [0, 360).
                                                
        Note: TrigIN_AbsoluteMove seems that it makes the wheel rotate forever
        the best is to use the setRelativeStep and the getStepTo functions.
        """
        # Essayer la distance relative globale
        if pos >=0 and pos < 360 :
            print('[FW103] WARNING seems that it makes the wheel rotate forever')
            self.device.SetMoveAbsolutePosition(Decimal(pos))
        else:
            print(f'[FW103] Absolute position must be in [0, 360). Got: {pos}')
            
    def _getStepTo(self, pos):
        """
        Compute the shortest signed rotation (in degrees) from the current angle to a
        target absolute angle within [0, 360). The result is in (-180, +180].
    
        Parameters
        ----------
        pos_deg : float
            Target absolute angle in degrees (0..360).
    
        Returns
        -------
        float
            Signed relative step in degrees to reach the target using the shortest path.
        """
        self.angle = self.getAngle()
        angle = pos - self.angle
        if angle > 180 :
            angle = angle - 360
        elif angle < -180 :
            angle = angle + 360
            
        return angle
    
    def setStepTo(self, pos):
        """
        Prepare a 'RelativeMove' step equal to the shortest rotation to the requested
        absolute angle. Use this before firing a TRIG1 RelativeMove pulse.
    
        Parameters
        ----------
        pos_deg : float
            Target absolute angle in degrees (0..360). Values outside will be wrapped.
        """
        angle = self._getStepTo(pos)
        # if self.move == 1 :
        #     angle = 60
        #     self.move = 2
        # elif self.move == 2 :
        #     angle = 60
        #     self.move = 3
        # elif self.move == 3 :
        #     angle = -120
        #     self.move = 1
        
        self.setRelativeStep(angle)
        
    def setTrigSlot(self, slot):
        """
        Prepare a 'RelativeMove' step to go to the given slot (0..nSlots-1) via the
        shortest path, so a single TRIG1 RelativeMove pulse will land on that slot.
    
        Parameters
        ----------
        slot : int
            Target slot index in [0..nSlots-1].
    
        Notes
        -----
        - This does not move immediately; it only sets the *relative* step that the
          controller will use on the next RelativeMove (e.g., hardware trigger).
        - For a 6-slot wheel, each slot is spaced by 60 degrees.
        """
        if int(slot) == slot:
            if 0 <= slot <= self.nSlots-1:
                step = 360.0 / self.nSlots
                pos = slot * step
                self.setStepTo(pos)
            else:
                print(f"[FW103] 'slot' must be in [0, {self.nSlots}]. Got: {slot}")
        else:
            print(f"[FW103] 'slot' must an integer. Got: {slot}")
    
    # ---------- Motion params ----------
        
    def setVelocity(self, acceleration = 100000.0, maxVelocity = 3600.0):
        """
        Configure acceleration and maximum velocity (real-world units; degrees/s^2 and degrees/s).
        Default values are the maximum values allowed by the FW103 device

        Parameters
        ----------
        acceleration : float, should be between 0.0 and 100000.0
            Target acceleration.
        maxVelocity : float, should be between 0.0 and 3600.0
            Target max velocity.
        """
        acceleration = min(max(acceleration, 0.0), 100000.0)
        maxVelocity = min(max(maxVelocity, 0.0), 3600.0)
        
        acceleration = 0 if acceleration < 0 else 100000.0 if acceleration > 100000.0 else acceleration
        maxVelocity = 0 if maxVelocity <0 else 3600.0 if maxVelocity > 3600.0 else maxVelocity
        
        device_vel_params = self.device.GetVelocityParams()
        device_vel_params.Acceleration = Decimal(acceleration)
        device_vel_params.MaxVelocity = Decimal(maxVelocity)
        self.device.SetVelocityParams(device_vel_params)
        
    def setMaximumVelocity(self):
        """
        set maximum speed for the microscope
        """
        self.setVelocity(acceleration = 100000.0, maxVelocity = 3600.0)
        
    def printVelocityParam(self):
        # Get/Set Velocity Params
        
        home_params = self.device.GetHomingParams()
        print(f'[FW103]: Homing Velocity: {home_params.Velocity}')
        
        device_vel_params = self.device.GetVelocityParams()
        
        print(f'[FW103]: Acceleration: {device_vel_params.Acceleration}, Velocity: {device_vel_params.MaxVelocity}')
        
    # ---------- High-level moves ----------
    
    def moveto(self, pos, timeout_ms=10000):
        """
        Move to an absolute angle (0..360).

        Parameters
        ----------
        pos : float
            Absolute angle in [0, 360).
        timeout_ms : int
            Move timeout in milliseconds.
        """
        
        if 0.0 <= float(pos) <= 360.0:
            new_pos = Decimal(pos)  # in Real Units
            self.device.MoveTo(new_pos, timeout_ms)
            self.angle = self.getAngle()
        else:
            print(f"[FW103] 'pos' must be in [0, 360). Got: {pos}")
        
    def moveby(self, degrees, timeout_ms=10000):
        """
        Move by a relative angle (positive or negative).

        Parameters
        ----------
        step : float
            Relative step in degrees.
        timeout_ms : int
            Move timeout in milliseconds.
        """
        self.setRelativeStep(degrees)
        self.device.MoveRelative(timeout_ms)
        self.angle = self.getAngle()


# C'est ici pour des tests de vitesse

def mesure_temps_lecture_position(device, n=10):
    """
    Mesure le temps moyen et max pour lire la position de la roue `device` sur n essais.
    """
    temps = []
    for i in range(n):
        t0 = time.perf_counter()
        angle = device.getAngle()  # ou .GetPosition() selon ton SDK
        t1 = time.perf_counter()
        temps.append(t1 - t0)
        print(f"Essai {i+1}: angle = {angle:.2f}°, temps = {1000*(t1-t0):.2f} ms")
    print(f"Temps moyen lecture : {1000*sum(temps)/n:.2f} ms")
    print(f"Temps max   lecture : {1000*max(temps):.2f} ms")
    print(f"Temps min   lecture : {1000*min(temps):.2f} ms")
    return temps

def mesure_temps_setStepTo(device, n=10):
    """
    Mesure le temps moyen et max pour lire la position de la roue `device` sur n essais.
    """
    temps = []
    for i in range(n):
        t0 = time.perf_counter()
        device.setStepTo(120)  # ou .GetPosition() selon ton SDK
        t1 = time.perf_counter()
        temps.append(t1 - t0)
        print(f"Essai {i+1}: temps = {1000*(t1-t0):.2f} ms")
    print(f"Temps moyen lecture : {1000*sum(temps)/n:.2f} ms")
    print(f"Temps max   lecture : {1000*max(temps):.2f} ms")
    print(f"Temps min   lecture : {1000*min(temps):.2f} ms")
    return temps