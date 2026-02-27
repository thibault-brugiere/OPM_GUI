# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 09:03:43 2025

@author: tbrugiere
"""

"""
    ########
    # Main #
    ########

# TODO : ouvrir laser_GUI depuis l'interface (et autres GUI)
# TODO : faire un dictionnaire.json dans config pour toute la description du microscope
        Pour qu'elle soit enregistrée lors de l'acquisition
# TODO : Ajuster la taille du preview pour avoir le champ entier (auto ?)
# TODO : Avoir plusieurs LUT (Fire ?)
# TODO : améliorer l'affichage du temps d'acquisition d'un volume.

# TODO : si on modifie la liste des filtres depuis l'interface, il faut la modifier dans la classe filter_wheel
        
    #################################
    # Multidimensionnal acquisition #
    #################################
# TODO : Dans le main quand on ajoute un channel, il faut modifier le nombre de channes
    pour accéder au nouveau channel ajouté
# TODO : pourquoi les lasers ne s'allument pas si je lance directement le main_MDA ?
# TODO : Ajouter le raise error experiment.mode (comme LS3)

    #-----------
    #MDA_manager
    #-----------

    # ---------
    # Hardware
    # --------
# TODO: warning fun acquisition : "Finite acquisition or generation has been stopped before the requested number of samples were acquired or generated."

# TODO Ajout mock filterwheel
    
    # daq_controller
# TODO ligne 175, ajouter : trigger_edge=nidaqmx.constants.Edge.RISING)

    #-------------
    # Tools
    #-------------

    #################
    # Sample Finder #
    #################
    
# TODO : Save positions for multi-position acquisition
# TODO : apply selected LUT
# TODO : controll illuminators using DAQ

    #############
    # Deskewing #
    #############
# TODO : Add a deskewing interface from the main
# TODO : Read the aspect ratio from 
"""