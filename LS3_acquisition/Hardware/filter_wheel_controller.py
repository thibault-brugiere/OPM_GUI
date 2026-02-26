# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 11:24:24 2025

@author: tbrugiere
"""
import os
import sys

    
from LS3_acquisition.Hardware.thorlabs_filter_wheel import ThorlabsFW103

filterList = ['BFP','GFP','CY3.5','TexRed','empty5', 'empty6']

class FilterWheel():
    """
    Minimal, microscope-oriented wrapper that exposes just what the microscope
    control code needs from a concrete filter wheel driver (e.g., ThorlabsFW103).

    Parameters
    ----------
    fw : object, optional
        A concrete filter wheel backend exposing the methods used below
        (connect, close, home, setSlot, getSlot, setMaximumVelocity,
         setTriggerForMicroscope, setTrigSlot). If None, a ThorlabsFW103 is created.
    filterList : list of str
        Ordered list of filter names corresponding to wheel slots (index == slot).
        Example: ['Empty', '405', '488', '561', '640', 'ND'] for a 6-slot wheel.
    """
    
    def __init__(self, fw = None, filterList = filterList):
        """
        Construct the high-level facade and store the concrete backend and the
        user-facing filter list.

        Notes
        -----
        - The list length must match the physical number of slots on the device.
        - This constructor does not attempt to connect to hardware.
        """
        self.fw = fw
        
        if self.fw is None :
            self.fw = ThorlabsFW103()
            
        self.filterList = filterList
        
        self.on_init()
        self.connected = False
        
    def on_init(self):
        """
        Validate configuration after construction (to be called by the owner if desired).

        Behavior
        --------
        - Checks that the number of provided filter names matches the device's slot count.
        - Only prints an error; does not raise, so the caller can decide how to handle it.
        """
        
        if self.fw.nSlots != len(self.filterList):
            print(f"""[FilterWheel]: ERROR There should be the same number of filters\n
                  in the filter wheel (curently {self.fw.nSlots}\n
                  than the filter list (currently {len(self.filterLIst)})""")
    
    def connect(self):
        """
        Establish connection to the underlying device and apply standard microscope settings.

        Behavior
        --------
        - Connects the concrete backend (opens USB, starts polling, enables drive).
        - Sets maximum safe velocity for snappy slot changes.
        - Programs trigger I/O for microscope integration:
            * TRIG1 = RelativeMove (input)
            * TRIG2 = InMotion     (output)
        """
        self.fw.connect()
        self._setMaximumVelocity()
        self._setTrigering()
        self.connected = True
        
    def close(self):
        """
        Cleanly disconnect from the device.

        Behavior
        --------
        - Stops polling and releases the USB handle on the backend.
        - Safe to call multiple times.
        """
        self.fw.close()
        self.connected = False
        
    def home(self):
        """
        Home the wheel to its index mark.

        When to use
        -----------
        - After first connection or if the absolute position is uncertain.
        - Ensures consistent mapping between slot indices and physical positions.
        """
        self.fw.home()
    
    def moveToFilter(self, filterName):
        """
        Move the wheel to the slot that corresponds to a given filter name.

        Parameters
        ----------
        filterName : str
            Human-readable filter label present in `self.filterList`.

        Behavior
        --------
        - Looks up the requested filter in the list and commands an absolute
          slot move on the backend if found.
        - If the name is unknown, the call is a no-op.
        """
        slot = self._getFilterSlot(filterName)
        if slot != -1:
            self.fw.setSlot(slot)
            
    def _setMaximumVelocity(self):
        """
        Apply device-specific maximum velocity/acceleration settings.

        Notes
        -----
        - Delegates to the backend so limits and units remain device-accurate.
        - Intended to be called after connect().
        """
        self.fw.setMaximumVelocity()
        
    def _setTrigering(self):
        """
        Configure hardware triggers for microscope synchronization.

        Mapping
        -------
        - TRIG1 (input): a pulse initiates a preprogrammed RelativeMove
          (set beforehand with `setTrigFilter(...)`).
        - TRIG2 (output): asserted while the wheel is in motion.

        Usage
        -----
        - Call once after connect().
        - Before pulsing TRIG1, call `setTrigFilter(name)` to preload
          the shortest-path relative step to the desired slot.
        """
        self.fw.setTriggerForMicroscope()
        
    def setTrigFilter(self, filterName):
        """
        Preload the 'shortest-path' relative move to reach a filter by name.

        Parameters
        ----------
        filterName : str
            Label present in `self.filterList`.

        Behavior
        --------
        - Computes the target slot and programs the backend so that a single
          TRIG1 RelativeMove pulse will rotate the wheel to that slot.
        - Does not move immediately; only prepares the next hardware-triggered move.
        """
        slot = self._getFilterSlot(filterName)
        self.fw.setTrigSlot(slot)
        
    def setTrigMove(self, movement):
        """
        Preload the relative move to reach a ne filter.

        Parameters
        ----------
        movement : int
            number of filter to move

        Behavior
        --------
        - Computes the target slot and programs the backend so that a single
          TRIG1 RelativeMove pulse will rotate the wheel to that slot.
        - Does not move immediately; only prepares the next hardware-triggered move.
        """
        angle = movement * 360 / 6
        self.fw.setRelativeStep(angle)
        
    def getPosition(self):
        """
        Return the current filter name based on the wheel's current slot.

        Returns
        -------
        str
            The human-readable name of the filter occupying the current slot.

        Notes
        -----
        - Uses `fw.getSlot()` (angle->slot rounding) then maps to `filterList`.
        """
        slot = self.fw.getSlot()
        return self.filterLIst[slot]
        
    
    def _getFilterSlot(self, filterName):
        """
        Resolve a filter label into a slot index.

        Parameters
        ----------
        filterName : str
            Name to search for (case-sensitive match against `filterList`).

        Returns
        -------
        int
            0-based slot index if found, -1 otherwise.

        Implementation detail
        ---------------------
        - Exact match is used to avoid accidental collisions.
        - The caller decides how to handle the -1 'not found' sentinel.
        """
        try:
            # Return the index of the filter in the list
            return self.filterList.index(filterName)
        except ValueError:
            # Return -1 if the filter is not in the list
            print(f"[FilterWheel]: {filterName} is not int the filterList")
            return -1