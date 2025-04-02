# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 11:40:06 2025

@author: tbrugiere
"""

"""
Convert file.ui to file.py

pyside6-uic widget/ui_channel_editor.ui -o widget/ui_channel_editor.py

TODO :

"""
import os
import sys
import copy

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

from Functions_UI import functions_ui
from configs.config import channel_config

from widget.ui_channel_editor import Ui_Form

class ChannelEditorWindow(QWidget, Ui_Form):
    """
    Show the window to set default camera size
    """
    def __init__(self, channel, channel_names, parent=None):
        """
        channels : dictionnary of channel objects 
        """
        
        super().__init__(parent)
        self.setupUi(self)
        self.original_channel_names = channel_names.copy()
        self.original_channel = channel.copy()
        
        # crée une copie profonde des objets afin qu'ils ne soient pas modifiés dans la fenêtre
        self.channel = copy.deepcopy(channel)
        self.channel_names = copy.deepcopy(channel_names)
        
        self.on_init()
        
    def on_init(self):
        self.setWindowTitle('Channels editor')
        self.setWindowFlag(Qt.Window)  # Assure que la fenêtre est indépendante
        
        ### Initialisation de la fenêtre
        
        self.label_status.setText("Ready")
        
        if self.parent() is not None and self.parent().n_camera > 1 :
            functions_ui.set_comboBox(self.comboBox_channel_camera ,
                                      functions_ui.generate_camera_indexes(self.parent().n_camera))
            self.comboBox_channel_camera.setDisabled(False)
        
        ### Library to set the channels
        
        self.lasers = ["405","488","561","640"] # = self.microscope.lasers
        
        self.checkBox_laser = {"405" : self.checkBox_laser_405,
                               "488" : self.checkBox_laser_488,
                               "561" : self.checkBox_laser_561,
                               "640" : self.checkBox_laser_640
                               } #Dictionnary of the laser checkboxes
        
        self.spinBox_laser_power = {"405": self.spinBox_laser_405,
                                    "488" : self.spinBox_laser_488,
                                    "561" : self.spinBox_laser_561,
                                    "640" : self.spinBox_laser_640
                                    } # Dictionnary of the laser power spin boxes
        
        self.list_channel_interface = { "checkBox_laser" :      self.checkBox_laser,
                                       "spinBox_laser_power" :  self.spinBox_laser_power,
                                       "filter" :               self.comboBox_channel_filter,
                                       "camera" :               self.comboBox_channel_camera,
                                       "exposure_time" :        self.spinBox_channel_exposure_time
                                       } # Dictionnary used to set all the interface elements for a given channel
        
        
        self.comboBox_channel_name_set_indexes()
        self.comboBox_channel_name_update()
        self.sync_filter_interface()
        
        #########################################
        ## Fonctions appelées pour les boutons ##
        #########################################
        
        self.comboBox_channel_name.currentIndexChanged.connect(self.comboBox_channel_name_update)
        self.pb_channel_save.clicked.connect(self.pb_channel_save_clicked_connect)
        self.pb_channel_add.clicked.connect(self.pb_channel_add_clicked_connect)
        self.pb_channel_remove.clicked.connect(self.pb_channel_remove_clicked_connect)
    
    def comboBox_channel_name_set_indexes(self):
        self.comboBox_channel_name.clear()
        self.comboBox_channel_name.addItems(list(self.channel_names))
        self.comboBox_channel_name_update()
        
    def comboBox_channel_name_update(self):
        "Configures the interface elements when changing the comboBox_channel from selected channel object."
        functions_ui.channel_set_interface(self.list_channel_interface,
                                           self.channel[self.comboBox_channel_name.currentText()])
        
        self.preview_channel = self.comboBox_channel_name.currentText() # Change the current name of the channel used for preview
    
    def pb_channel_add_clicked_connect(self):
        "Saves the settings from the interface elements into a new channel object named from channel_name lineEdit object."
        index = self.lineEdit_channel_name.text() # get name of the new channel
        
        if not index:
             self.label_status.setText("channel name cannot be empty!")
             return
        
        name_ok, index = functions_ui.legalize_name(index)
        
        if name_ok == False : self.label_status.setText("Invalid experiment name! Avoid spaces and special characters.")
        
        self.channel[index] = channel_config(index, self.lasers) #Create the new channel
        functions_ui.save_channel_from_interface(self.list_channel_interface,
                                                 self.channel[self.comboBox_channel_name.currentText()]) #save the channel parameters
        
        self.comboBox_channel_name.addItem(index) # Add the new channel to the comboBox
        self.comboBox_channel_name.setCurrentText(index) # set the comboBox to this index
        self.lineEdit_channel_name.setText(index)
        self.channel_names = list(self.channel.keys())
 
    def pb_channel_remove_clicked_connect(self):
        "Removes the currently selected channel from the combo box and the channel dictionary."
        channel_id = self.comboBox_channel_name.currentText()
        index = self.comboBox_channel_name.currentIndex()

        if index >= 0:
            self.comboBox_channel_name.removeItem(index)
            self.channel.pop(channel_id, None) # channel.pop remove the channel from the channel dictionnaire
            
            self.channel_names = list(self.channel.keys())


    def pb_channel_save_clicked_connect(self):
        "Saves the settings from the interface elements into the specified channel object."
        functions_ui.save_channel_from_interface(self.list_channel_interface,
                                                 self.channel[self.comboBox_channel_name.currentText()])
        
    def sync_filter_interface(self):
        """
        Updates the interfaceand channels based on the avaliable filters
        """
        if self.parent() is not None :
            options = copy.deepcopy(self.parent().microscope.filters)
        else:
            options = []
        
        options.insert(0, '-None-')
        
        self.comboBox_channel_filter.blockSignals(True) # Pas utile, peut-être plus tard ?
        self.comboBox_channel_filter.clear()
        self.comboBox_channel_filter.addItems(options)

        for channel in self.channel.keys():
            if self.channel[channel].filter not in options:
                self.channel[channel].filter = None
        
        self.comboBox_channel_filter.blockSignals(False)
        
        self.comboBox_channel_name_update()
            
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Confirmer changes',
            """"Are you sure you want to apply the changes?
            If ou press Yes, settings in the main window will be erased
            
            Warning: if filters list have been changed previously, channels may have been modified""",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Yes:
            self.parent().channel_names = self.channel_names
            self.parent().default_channel = self.channel
            self.parent().channel = self.channel
            self.parent().comboBox_channel_name_set_indexes()
            self.parent().comboBox_channel_name_index_changed()
            self.parent().sync_laser_interface()
            event.accept()
        elif reply == QMessageBox.No:
            event.ignore()
        else:
            event.accept()

    # Ce bloc permet de tester la fenêtre ChannelEditorWindow indépendamment
if __name__ == '__main__':
    "To test the window"
    app = QApplication(sys.argv)
    test_lasers = ["405","488","561","640"]
    test_channel_names = ['BFP', 'GFP', 'CY3.5', 'TexRed']
    channels = {}
    for channel in test_channel_names:
            channels[channel] = channel_config(channel, test_lasers)
    editor = ChannelEditorWindow(channels, test_channel_names)
    editor.show()
    sys.exit(app.exec())