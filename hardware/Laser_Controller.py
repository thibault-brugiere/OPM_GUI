# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 15:39:22 2025

@author: tbrugiere
"""
from collections import Counter
import time

from hardware.functions_serial_ports import functions_serial_ports as serial
from hardware.functions_DAQ import functions_daq
# from mock.DAQ import functions_daq

class LaserController:
    """
    This class unifies laser control between NI-DAQ and an Oxxius combiner.
     - Power modulation is handled by NI-DAQ analog outputs when available;
       if not, the Oxxius USB setpoint is used as a fallback.
     - Emission on/off is always gated by NI-DAQ digital outputs,
       so that the microscope timing stays fully hardware-synchronized.
     TODO
    """
    def __init__(self, analog_out: dict, digital_out: dict, volts_per_laser_percent: dict,
                 OxxiusCombiner_command: dict, channel_list: list, OxxiusCombiner_port = None,
                 OxxiusCombiner_model = "L4Cc"):
        """
        Unified controller for multiple lasers. It can drive:
          - Analog outputs (NI-DAQ) for power setpoint (V),
          - Digital outputs (NI-DAQ) for gating (on/off),
          - Oxxius L4Cc/L6Cc over USB for power (APC) + shutter/TTL.
        
        Parameters
        ----------
        analog_out : dict[channel -> AO line or None]
            Mapping from channel label (e.g. "405") to NI-DAQ analog output line.
        digital_out : dict[channel -> DO line or None]
            Mapping from channel label to NI-DAQ digital output line.
        volts_per_laser_percent : dict[channel -> float]
            Scale factor: volts_per_percent (V per % of desired power).
        OxxiusCombiner_command: dict[channel -> str] or None
            Command send to the combiner to set laser power,
            can be None if OxxiusCombiner_port == None
        channel_list : list[str]
            Declared channels (labels).
        OxxiusCombiner_port : str | None
            Serial/USB port for Oxxius combiner. If None, USB control is disabled.
        OxxiusCombiner_model : str
            "L4Cc" or "L6Cc".
        """
        self.analog_out = analog_out
        self.digital_out = digital_out
        self.volts_per_laser_percent = volts_per_laser_percent
        self.OxxiusCombiner_command = OxxiusCombiner_command
        self.channel_list = channel_list
        self.OxxiusCombiner_port = OxxiusCombiner_port
        self.OxxiusCombiner_model = OxxiusCombiner_model
        
        # Track emission state per channel (False at init).
        self.laser_on = {channel: False for channel in self.channel_list}
        
        # Throttle state per channel (last time/value sent to Oxxius)
        # to avoid to much message sending to laser combiner
        self._usb_throttle = {ch: 0.0 for ch in self.channel_list}
        self._usb_min_interval_s = 0.1   # 150 ms between USB writes
        
        # If requested, initialize Oxxius combiner and configure modulation.
        if self.OxxiusCombiner_port != None:
            serial.send_command("SH1 1", self.OxxiusCombiner_port) # To open main shutter of the oxxius combiner
            power = serial.send_command_response("?PL2", "COM5")
            print(f'power:{power}')
            
        #
        # Check that the number of elements in the dictionnaries / channel_list / Oxiuss are the right ones
        #
        
        self._check_config()
                
    def _check_config(self):
        """Validate that dicts and channel_list are coherent; collect all errors and raise once."""
        
        keys_analog_out = list(self.analog_out.keys())
        keys_digital_out = list(self.digital_out.keys())
        keys_volts_per_laser_percent = list(self.volts_per_laser_percent.keys())
        if self.OxxiusCombiner_port != None :
            keys_OxxiusCombiner_command = list(self.OxxiusCombiner_command.keys())
        channel_list = self.channel_list
        
        errors = []
        
        # 1) Channel list sanity
        if len(channel_list) != len(set(channel_list)):
            errors.append("Duplicate entries found in 'channel_list'.")
        
        # # 2) Oxxius capacity (only if an Oxxius combiner is present)
        # if self.OxxiusCombiner is not None:
        #     max_channels = self.OxxiusCombiner.max_channels
        #     if max_channels < len(channel_list):
        #         errors.append(f"Oxxius channel capacity exceeded: {len(channel_list)} configured, "
        #                       f"but device supports at most {max_channels} channels.")
        
        # 3) Cardinality vs analog/digital dicts
        if len(channel_list) != len(keys_analog_out) or len(channel_list) != len(keys_digital_out):
            errors.append(
                "Mismatch in counts: 'channel_list', 'analog_out' keys and 'digital_out' keys "
                f"must have the same length (got {len(channel_list)} / {len(keys_analog_out)} / {len(keys_digital_out)})."
                    )
        # 4) Key sets must match channel_list
        if set(channel_list) != set(keys_analog_out):
            errors.append("Key set mismatch: 'analog_out' keys must match 'channel_list'.")
        if set(channel_list) != set(keys_digital_out):
            errors.append("Key set mismatch: 'digital_out' keys must match 'channel_list'.")
        if set(channel_list) != set(keys_volts_per_laser_percent):
            errors.append("Key set mismatch: 'volts_per_laser_percent' keys must match 'channel_list'.")
        if self.OxxiusCombiner_port != None :
            if set(channel_list) != set(keys_OxxiusCombiner_command):
                errors.append("Key set mismatch: 'OxxiusCombiner_command' keys must match 'channel_list'.")
            
        # 5) Detect duplicate *values* in AO/DO mappings (same hardware line used twice)
        ao_vals = list(self.analog_out.values())
        ao_dups = [k for k, v in Counter(ao_vals).items() if v > 1]
        if ao_dups and ao_dups != [None]:
            errors.append(f"Duplicate analog outputs detected: {ao_dups}")
            
        do_vals = list(self.digital_out.values())
        do_dups = [k for k, v in Counter(do_vals).items() if v > 1]
        if do_dups and do_dups != [None]:
            errors.append(f"Duplicate digital outputs detected: {do_dups}")
        
        # Raise the errors
        if errors:
            raise ValueError("Invalid laser configuration:\n - " + "\n - ".join(errors))
    
        return True
            

    def _check_channel(self, channel: str) -> str:
        """Ensure the provided channel exists in channel_list."""
        if channel not in self.channel_list:
            raise ValueError(f"Unknown channel '{channel}'. Must be one of {self.channel_list}.")
        else:
            return channel
        
    def _ch_to_oxxius_idx(self, channel: str) -> int:
        """Map channel label to Oxxius 1-based channel index."""
        # Oxxius API expects 1..N; list.index() is 0-based → add 1.
        return self.channel_list.index(channel) + 1
                    
    def set_laser_power(self, channel: str, power: float, force: bool = False):
        """
        Set Oxxius USB power setpoint (in %) for a channel
        with frequency limitation
        only if no analog output (AO) is available.
        Does not start emission; gating is done via DAQ.
        """
        self._check_channel(channel)
        
        if self.analog_out[channel] is not None :
            return
        
        if self.digital_out[channel] is None :
            return
        
        if self.OxxiusCombiner_command[channel] is None :
            pass
        
        # Clamp percent to [0, 100] for safety (adjust if you allow >100%).
        power = max(0.0, min(100.0, float(power)))
        
        # Throttle logic (par canal)
        last_time = self._usb_throttle[channel]
        now = time.monotonic()
        too_soon = (now - last_time) < self._usb_min_interval_s
        
        if not force and too_soon:
            return
        
        command = self.OxxiusCombiner_command[channel] + f' {power}'
        serial.send_command(command, self.OxxiusCombiner_port)
        print('send command')
        
        self._usb_throttle[channel] = now
                
    def start_laser_emission(self, channel: str, power: float):
        """
        Start emission using DAQ only:
        - AO: write voltage (power[%] * scale).
        - DO: set line high (True).
        Oxxius gating is not used here.
        """
        self._check_channel(channel)
        if self.analog_out[channel] is not None:
            self.laser_on[channel] = True
            power = max(0.0, min(100.0, float(power)))
            functions_daq.analog_out(power * self.volts_per_laser_percent[channel],
                                     self.analog_out[channel])
        if self.digital_out[channel] is not None :
            self.laser_on[channel] = True
            functions_daq.digital_out(True, self.digital_out[channel])   
    
    def stop_laser_emission(self, channel: str):
        """
        Stop emission using DAQ only:
        - DO: set line low (False).
        - AO: write 0 V if present.
        Oxxius gating is not used here.
        """
        self._check_channel(channel)
        if self.analog_out[channel] is not None:
            self.laser_on[channel] = False
            functions_daq.analog_out(0, self.analog_out[channel])
        if self.digital_out[channel] is not None :
            self.laser_on[channel] = False
            functions_daq.digital_out(False, self.digital_out[channel])
    
    def read_power(self, channel:str):
        """
        Read measured optical power (mW) from Oxxius if available.
        Returns None if not available.
        """
        self._check_channel(channel)
        if self.OxxiusCombiner is not None:
            idx = self._ch_to_oxxius_idx(channel)
            power = self.OxxiusCombiner.read_power_mw(idx)
            return(power)
        
        else:
            return(None)
        
        """
        Note :
            S'il n'est pas possible d'envoyer une commande au laser, vérifier 
            via le Gui du que la comment ?CDC renvoie 1. sinon envoyer
            la commande CDC = 1
            
            Voici la liste des fonctions utiles pour le laser oxxius.
            PLn xx :  set the laser power of the line n to xx mw
            ?PLn : return the laser power of the line n
            PPLn xx :  set the laser power of the line n to xx %
            ?PPLn : return the laser power of the line n
        """