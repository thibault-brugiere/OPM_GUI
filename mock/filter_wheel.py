# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:46:19 2025

@author: tbrugiere
"""

filterList = ['BFP','GFP','CY3.5','TexRed','empty5', 'empty6']

class FilterWheel:
    
    def __init__(self, filterList = filterList):
        
        self.filterList = filterList
        
        self.connected = False
        
        self.position = 0
        
        self.on_init()
        
    def on_init(self):
        pass
    
    def connect(self):
        self.connected = True
        print("[FW] connected to simulated filterwheel")
        
    def close(self):
        self.connected = False
        
    def home(self):
        self.position = 0
        print(f"[FW] moved to {self.filterList[self.position]}")
        
    def moveToFilter(self, filterName):
        slot = self._getFilterSlot(filterName)
        if slot != -1:
            self.position = slot
            print(f"[FW] moved to {self.filterList[self.position]}")
            
    def _setMaximumVelocity(self):
        pass
        
    def _setTrigering(self):
        pass
        
    def setTrigFilter(self, filterName):
        pass
        
    def setTrigMove(self, movement):
        pass
    
    def get_position(self):
        return self.position

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