# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:30:13 2025

@author: tbrugiere
"""

"""
Convert file.ui to file.py

pyside6-uic widget/ui_set_filters.ui -o widget/ui_set_filters.py

TODO :

"""
import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget

# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)

from widget.ui_set_filters import Ui_Form

class filtersEditionWindow(QWidget, Ui_Form):
    """
    Show the window to set default channels
    """
    def __init__(self, filters, parent=None):
        """
        preset_size : Array of preset sizes 
        """
        
        super().__init__(parent)
        self.setupUi(self)
        
        self.filters = filters
        
        self.on_init()
        
    def on_init(self):
        
        self.setWindowTitle('set filters')
        self.setWindowFlag(Qt.Window)  # Assure que la fenêtre est indépendante
        
        self.lineEdit = {'Filter1' : self.lineEdit_Filter1,
                         'Filter2' : self.lineEdit_Filter2,
                         'Filter3' : self.lineEdit_Filter3,
                         'Filter4' : self.lineEdit_Filter4,
                         'Filter5' : self.lineEdit_Filter5,
                         'Filter6' : self.lineEdit_Filter6}
        
        for i, (key, line_edit) in enumerate(self.lineEdit.items()):
            if i < len(self.filters):
                line_edit.setText(self.filters[i])
        
    def set_filter_list(self):
        self.filters = [line_edit.text() for line_edit in self.lineEdit.values()]
        self.parent().microscope.filters = self.filters
             
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Confirmer changes',
            "Are you sure you want to apply the changes?\nIf ou press Yes, settings in the main window will be erased",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Cancel
        )

        if reply == QMessageBox.Yes:
            self.set_filter_list()
            self.parent().sync_filter_interface()
            event.accept()
        elif reply == QMessageBox.No:
            event.ignore()
        else:
            event.accept()
        
if __name__ == '__main__':
    "To test the window"
    app = QApplication(sys.argv)
    filters = ['BFP','GFP','CY3.5','TexRed','empty5', 'empty6']
    
    editor = filtersEditionWindow(filters)
    editor.show()
    sys.exit(app.exec())