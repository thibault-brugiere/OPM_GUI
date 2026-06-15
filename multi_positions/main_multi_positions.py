# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 14:27:02 2026

@author: tbrugiere

pyside6-uic D:/Projets_Python/OPM_GUI/multi_positions/ui_multi_position.ui -o D:/Projets_Python/OPM_GUI/multi_positions/ui_multi_position.py

"""
from functools import partial
import os
import string
import sys
import time as t

from PySide6.QtCore import QTimer, QThread, Signal, Qt, QElapsedTimer
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from PySide6.QtWidgets import QCheckBox, QLineEdit, QSpinBox, QDoubleSpinBox, QPushButton
from PySide6.QtGui import QPixmap, QImage, QIcon

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    
from multi_positions.positions import Positions
from multi_positions.ui_multi_position import Ui_Form
from hardware.functions_Stage_ASI import Stage_ASI
from hardware.functions_serial_ports import functions_serial_ports as serial_port
    
class multi_position_edditor(QWidget, Ui_Form):
    
    def __init__(self, port = None, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.port = port
        
        self.positions = Positions()
        
        self.on_init()
            
    def on_init(self):
        self.stage_connected = False
        if self.port is not None :
            if self.test_port() :
                self.stage_connected = True
                self.stage = Stage_ASI(self.port)
                self.comboBox_devices.setEnabled(False)
        
        self.alphabet = string.ascii_lowercase
        self.i = 0 
        
        self.devices = serial_port.list_serial_ports()
        self.set_comboBox_devices()
        self.tools_desactivation()
        
        self.comboBox_devices.currentIndexChanged.connect(self.comboBox_devices_indexChanged)
        self.pb_add_position.clicked.connect(self.pb_add_position_clicked)
        self.pb_remove_all_positions.clicked.connect(self.pb_remove_all_positions_clicked)
        self.pb_sort_snake.clicked.connect(self.pb_sort_snake_clicked)
        self.pb_sort_nearest.clicked.connect(self.pb_sort_nearest_clicked)
        
    def set_comboBox_devices(self):
        "set the indexes of the comboBox_devices depending on avaliable devices"
        self.comboBox_devices.addItems(['None'])
        self.comboBox_devices.addItems(self.devices)
        
    def tools_desactivation(self):
        self.pb_add_position.setEnabled(self.stage_connected)
        self.pb_remove_all_positions.setEnabled(self.stage_connected)
        self.pb_sort_nearest.setEnabled(self.stage_connected)
        self.pb_sort_snake.setEnabled(self.stage_connected)
        if self.stage_connected :
            self.label_connection.setText('Connected')
        else :
            self.label_connection.setText('Not Connected')
    
    def test_port(self):
            response = serial_port.send_command_response("W X Y Z", self.port)
            if response[0:2] == ':A':
                return True
            
            else :
                return False
                
    def comboBox_devices_indexChanged(self):
        """"set the self.port and self.connection status as well as the interface
        depending on the comboBox_devices index"""
        self.port = self.comboBox_devices.currentText() 
        if self.port != 'None':
            if self.test_port():
                self.stage_connected = True
                self.comboBox_devices.setEnabled(False)
                t.sleep(0.01)
                self.stage = Stage_ASI(self.port)
                
            else:
                self.stage_connected = False
                print("not connected")
        else :
            self.stage_connected = False
        
        self.tools_desactivation()
        
    def pb_add_position_clicked(self):
        if self.stage.is_moving():
            return

        name = self.alphabet[self.i]
        self.i = (self.i + 1) % len(self.alphabet)
        
        pos = self.stage.get_position()
        self.positions.add_position_xyz(pos[0] / 1000, pos[1] / 1000, pos[2] / 1000, True, name)
        self._refresh_table()
    
    def pb_remove_all_positions_clicked(self):
        for _ in range(len(self.positions)) :
            self.positions.remove(0)
        
        self._refresh_table()
    
    def pb_sort_snake_clicked(self):
        self.positions.sort_snake_xy()
        self._refresh_table()
    
    def pb_sort_nearest_clicked(self):
        self.positions.sort_positions()
        self._refresh_table()
    
    def _refresh_table(self):
        self.table_positions.setRowCount(len(self.positions))
        
        for row, pos in enumerate(self.positions):
            checkbox = QCheckBox()
            checkbox.setChecked(pos.enabled)
            checkbox.stateChanged.connect(partial(self.set_enabled, row))
            
            self.table_positions.setCellWidget(row, 0, checkbox)
            
            nameedit = QLineEdit()
            nameedit.setText(self.get_name(row))
            nameedit.editingFinished.connect(
                partial(self.set_name, row))
            
            self.table_positions.setCellWidget(row, 1, nameedit)
            
            axes = ["x","y","z"]
            column = 2
            
            for axe in axes :
                sb_pos = QDoubleSpinBox()
                sb_pos.setMaximum(10.0)
                sb_pos.setMinimum(-10.0)
                sb_pos.setDecimals(4)
                sb_pos.setSingleStep(0.01)
                sb_pos.setValue(self.get_axe_value(row, axe))
                sb_pos.editingFinished.connect(
                    partial(self.set_axe_value, row, column,axe))
                
                self.table_positions.setCellWidget(row, column, sb_pos)
                
                column += 1
                
            pb_functions = [self.move_up,
                            self.move_down,
                            self.move_to,
                            self.reset_position,
                            self.remove_position]
            
            pb_icons = [self._create_icon('Icons/Arrows_09.png'),
                        self._create_icon('Icons/Arrows_10.png'),
                        "Move to", "Set", "Remove"]
            column = 5
            
            for i, fun in enumerate(pb_functions) :
                pb_fun = QPushButton()
                if type(pb_icons[i]) is QIcon :
                    pb_fun.setIcon(pb_icons[i])
                elif type(pb_icons[i]) is str :
                    pb_fun.setText(pb_icons[i])
                
                pb_fun.clicked.connect(
                    partial(fun, row))
                
                self.table_positions.setCellWidget(row, column, pb_fun)
                
                column += 1
    
    def set_enabled(self, r, enabled):
        self.positions[r].enabled = enabled
        
    def get_name(self, r):
        return self.positions[r].name
        
    def set_name(self, r):
        line_edit = self.table_positions.cellWidget(r,1)
        if line_edit is not None :
            name = line_edit.text()
            self.positions[r].name = name
        
    def set_axe_value(self, r, column, axe):
        sb = self.table_positions.cellWidget(r, column)
        if sb is not None :
            if axe == "x" :
                self.positions[r].x = sb.value()
            elif axe == "y" :
                self.positions[r].y = sb.value()
            elif axe == "z" :
                self.positions[r].z = sb.value()
            else :
                raise ValueError(f"Axe should be x, y or z, actually {axe}")
            
    def get_axe_value(self, r, axe:str) :
        if axe == "x" :
            # print(self.positions[r].x)
            return self.positions[r].x
        elif axe == "y" :
            # print(self.positions[r].y)
            return self.positions[r].y
        elif axe == "z" :
            # print(self.positions[r].z)
            return self.positions[r].z
        else :
            raise ValueError(f"Axe should be x, y or z, actually {axe}")
            
    def move_up(self, r):
        self.positions.move_up(r)
        self._refresh_table()
        
    def move_down(self,r):
        self.positions.move_down(r)
        self._refresh_table()
        
    def move_to(self,r):
        if self.stage.is_moving():
            return
        position = [self.positions[r].x * 1000, self.positions[r].y * 1000, self.positions[r].z * 1000 ]
        self.stage.go_to_position(position)
        
    def reset_position(self,r):
        if self.stage.is_moving():
            return
        
        pos = self.stage.get_position()
        self.positions[r].x = pos[0] / 1000
        self.positions[r].y = pos[1] / 1000
        self.positions[r].z = pos[2] / 1000
        self._refresh_table()
        
    def remove_position(self,r):
        self.positions.remove(r)
        self._refresh_table()
            
    def _create_icon(self, path:str):
        if __name__ == "__main__": # Si jamais la fenêtre est appelée depuis ce fichier
            icon_path = os.path.join(parent_dir, path)
        else:
            icon_path = path
            
        return QIcon(icon_path)


##############################################################################
if __name__ == '__main__':
    
    
    
    app = QApplication(sys.argv)

    editor = multi_position_edditor()
    editor.show()
    sys.exit(app.exec())