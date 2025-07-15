# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 15:38:23 2025

@author: tbrugiere
"""

from main_MDA import MultidimensionalAcquisition

MDA = MultidimensionalAcquisition()
MDA.initialize_cameras()
MDA.initialize_acquisition_workers()
MDA.configure_daq()
MDA.run()