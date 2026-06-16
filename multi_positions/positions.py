# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 16:46:08 2026

@author: tbrugiere
"""

import json
import string

from dataclasses import dataclass, asdict

@dataclass
class Position:
    """
    all positions ar in mm
    """
    x: float
    y: float
    z: float
    enabled: bool = True
    name: str = ""
                
class Positions:
    "Object containing multiple positions for experiment"
    def __init__(self):
        self._positions: list[Position] = []
        
        self.alphabet = string.ascii_lowercase
        self.i = 0 
        
    def add_position(self, position: Position) -> None :
        self._positions.append(position)
        self.i += 1

    def add_position_xyz(self, x, y, z, enabled = True, name = ""):
        self._positions.append(Position(x, y, z, enabled, name))
        self.i += 1
        
    def move_down(self, index: int) -> None:
        if index >= 0 and index < len(self._positions) -1 :
            self._positions[index], self._positions[index + 1] = (
                self._positions[index + 1],
                self._positions[index]
            )
            
    def move_up(self, index: int) -> None:
        if index > 0 and index <= len(self._positions):
            self._positions[index - 1], self._positions[index] = (
                self._positions[index],
                self._positions[index - 1]
            )
    
    def move(self, old_index: int, new_index: int) -> None:
        pos = self._positions.pop(old_index)
        self._positions.insert(new_index, pos)
        
    def remove(self, index:int) -> None:
        self._positions.pop(index)
        
    def __len__(self) -> int:
        return len(self._positions)
    
    def __getitem__(self, index: int) -> Position:
        return self._positions[index]
    
    def __iter__(self):
        return iter(self._positions)

    def sort_positions(self):
        if len(self._positions) == 0 :
            return
        
    def sort_nearest_neighbor(self, start_index: int = 0) -> None:
        if len(self._positions) <= 2:
            return
    
        remaining = self._positions.copy()
        current = remaining.pop(start_index)
        ordered = [current]
    
        while remaining:
            next_index = min(
                range(len(remaining)),
                key=lambda i: (
                    (remaining[i].x - current.x) ** 2
                    + (remaining[i].y - current.y) ** 2
                    + (remaining[i].z - current.z) ** 2
                )
            )
            current = remaining.pop(next_index)
            ordered.append(current)
    
        self._positions = ordered
        
    def sort_snake_xy(self) -> None:
        self._positions.sort(key=lambda p: (p.y, p.x))
    
        rows = {}
        for pos in self._positions:
            rows.setdefault(round(pos.y, 3), []).append(pos)
    
        ordered = []
        for row_index, y in enumerate(sorted(rows)):
            row = sorted(rows[y], key=lambda p: p.x)
            if row_index % 2:
                row.reverse()
            ordered.extend(row)
    
        self._positions = ordered
        
    def to_dict(self):
        positions = [asdict(pos) for pos in self._positions]
        pos_dict = {
            "positions" : positions,
            }
        return pos_dict
    
    def from_dict(self, pos_dict):
        self._positions = [Position(**pos_dict)
                           for pos_dict in pos_dict["positions"]]
        
    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, indent=4)
    
    def load(self, filename):
        with open(filename, "r") as f:
            pos_dict = json.load(f)
            self.from_dict(pos_dict)
        
        