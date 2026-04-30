# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:37:59 2026

@author: tbrugiere
"""

import os
import sys


# Ajoutez le dossier parent au sys.path si le fichier est exécuté directement
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)