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

# from PySide6.QtCore import QTimer, QThread, Signal, Qt, QElapsedTimer
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PySide6.QtWidgets import QCheckBox, QLineEdit, QDoubleSpinBox, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    
from multi_positions.positions import Positions
from multi_positions.ui_multi_position import Ui_Form
from hardware.functions_Stage_ASI import Stage_ASI
    
class multi_position_edditor(QWidget, Ui_Form):
    
    def __init__(self, positions = None, parent = None, stage = None):
        super().__init__(parent)
        self.setupUi(self)
        self.stage = stage
        
        if positions is not None :
            self.positions = positions
        else :
            self.positions = Positions()
        
        self.on_init()
            
    def on_init(self):
        self.setWindowTitle('Multi position')
        self.setWindowFlag(Qt.Window)  # Assure que la fenêtre est indépendante
        
        #
        # Check the connexion of the stage
        #
        
        if self.stage is None :
            self.stage = Stage_ASI()
            
        self.stage_connected = self.stage.connected
        self._own_stage_connection = not self.stage_connected
        
        self.stage_connected = False
        
        self.alphabet = string.ascii_lowercase
        
        self.devices = self.stage.list_serial_ports()
        self.set_comboBox_devices()
        self.comboBox_devices_indexChanged()
        self.try_stage()
        
        #
        # Connexion entre les boutons et les fonctions
        #
        
        self.pb_save.clicked.connect(self.save_positions)
        self.pb_load.clicked.connect(self.load_positions)
        self.comboBox_devices.currentIndexChanged.connect(self.comboBox_devices_indexChanged)
        self.pb_add_position.clicked.connect(self.pb_add_position_clicked)
        self.pb_remove_all_positions.clicked.connect(self.pb_remove_all_positions_clicked)
        self.pb_sort_snake.clicked.connect(self.pb_sort_snake_clicked)
        self.pb_sort_nearest.clicked.connect(self.pb_sort_nearest_clicked)
        
    def try_stage(self):
        "Try to connect the stage witout the setting the port"
        if not self.stage.connected :
            try :
                self.stage.connect()
            except :
                pass
        
        if self.stage.connected :
            self.stage_connected = True
            self.comboBox_devices.setCurrentText(self.stage.port)
            self.comboBox_devices.setEnabled(False)
            
        self.tools_desactivation()
        self._refresh_table()
        
    def set_comboBox_devices(self):
        "set the indexes of the comboBox_devices depending on avaliable devices"
        self.comboBox_devices.addItems(['None'])
        self.comboBox_devices.addItems(self.devices)
        
    def tools_desactivation(self):
        self.pb_save.setEnabled(self.stage_connected)
        self.pb_load.setEnabled(self.stage_connected)
        self.pb_add_position.setEnabled(self.stage_connected)
        self.pb_remove_all_positions.setEnabled(self.stage_connected)
        self.pb_sort_nearest.setEnabled(self.stage_connected)
        self.pb_sort_snake.setEnabled(self.stage_connected)
        if self.stage_connected :
            self.label_connection.setText('Connected')
        else :
            self.label_connection.setText('Not Connected')
                
    def comboBox_devices_indexChanged(self):
        """"set the self.port and self.connection status as well as the interface
        depending on the comboBox_devices index"""
        self.stage.close()
        self.stage_connected = False
        self.port = self.comboBox_devices.currentText() 
        if self.port != 'None':
            try :
                self.stage.change_port(self.port)
                self.stage.connect()
                if self.stage.test_port() :
                    self.connected = True
                else :
                    self.stage.close()
            except :
                pass
        
        self.tools_desactivation()
        
    def pb_add_position_clicked(self):
        if self.stage.is_moving():
            return

        name = f"Position{self.positions.i:04d}"
        
        pos = self.stage.get_position()
        self.positions.add_position_xyz(pos[0] / 1000, pos[1] / 1000, pos[2] / 1000, True, name)
        self._refresh_table()
    
    def pb_remove_all_positions_clicked(self):
        message = "Would you like to\nreinitialize all the position\nif Yes, all positions will be deleted"
        if self.ask_user(message = message):
            for _ in range(len(self.positions)) :
                self.positions.remove(0)
            
            self._refresh_table()
    
    def pb_sort_snake_clicked(self):
        self.positions.sort_snake_xy()
        self._refresh_table()
    
    def pb_sort_nearest_clicked(self):
        self.positions.sort_nearest_neighbor()
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
                
        self._send_to_parent()
    
    def set_enabled(self, r, enabled):
        self.positions[r].enabled = enabled
        
        self._send_to_parent()
        
    def get_name(self, r):
        return self.positions[r].name
        
    def set_name(self, r):
        line_edit = self.table_positions.cellWidget(r,1)
        if line_edit is not None :
            name = line_edit.text()
            self.positions[r].name = name
            
        self._send_to_parent()
        
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
                
            self._send_to_parent()
            
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
        if self.ask_user() :
            self.positions.remove(r)
            self._refresh_table()
            
    def save_positions(self):
        filename, _ = QFileDialog.getSaveFileName(self,
                                               "ave positions",
                                               "",
                                               "Position files (*.json);;All files (*)")
        
        if filename:
            self.positions.save(filename)
    
    def load_positions(self):
        filename, _ = QFileDialog.getOpenFileName(self,
                                               "Open positions",
                                               "",
                                               "Position files (*.json);;All files (*)")
        if filename:
            self.positions.load(filename)
                
            self._refresh_table()
            
    def _create_icon(self, path:str):
        if __name__ == "__main__": # Si jamais la fenêtre est appelée depuis ce fichier
            icon_path = os.path.join(parent_dir, path)
        else:
            icon_path = path
            
        return QIcon(icon_path)
    
    def _send_to_parent(self):
        if self.parent is not None :
            self.parent().positions = self.positions
            self.parent()._set_lcdNumber_multipositions()
    
    def ask_user(self, title = "Confirm deletion", message = "Would you like to delete position ?"):
        result = QMessageBox.question(self,
                                      title,
                                      message,
                                      (QMessageBox.Yes |
                                       QMessageBox.No))
        
        if result == QMessageBox.Yes :
            return True
        else:
            return False
    
    def closeEvent(self, event):
        
        result = QMessageBox.question(self,
                                      "Confirm Exit...",
                                      "Do you want to exit ?",
                                      (QMessageBox.Yes |
                                       QMessageBox.No))
        if result == QMessageBox.Yes:
            if self._own_stage_connection :
                self.stage.close()
            try :
                self.parent().positions = self.positions
                self.parent()._set_lcdNumber_multipositions()
            except:
                pass
            
            event.accept()
        else:
            event.ignore()


##############################################################################
if __name__ == '__main__':
    
    
    
    app = QApplication(sys.argv)

    editor = multi_position_edditor()
    editor.show()
    sys.exit(app.exec())