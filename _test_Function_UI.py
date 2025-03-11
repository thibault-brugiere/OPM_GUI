# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 15:54:08 2025

@author: tbrugiere
"""
import numpy as np

from PySide6.QtCore import QTime

from Functions_UI import functions_ui

def test_legalize_name():
    name_1 = "bonjour\/:*?<>| ù"
    
    name_ok_1, NAME_1 = functions_ui.legalize_name(name_1)
    
    name_2 = "bonjour_tout_le_monde"
    
    name_ok_2, NAME_2 = functions_ui.legalize_name(name_2)
    
    if name_ok_1 == False and NAME_1 == "bonjour__________" and name_ok_2 and NAME_2 == "bonjour_tout_le_monde" :
        print("Test pass!")
        
    else:
        print("Results are : -" + NAME_1 + "- and -" + NAME_2 +
              "- and it should be -bonjour__________- and -bonjour_tout_le_monde-")
    
    pass

def test_generate_camera_indexes():
    camera_names = functions_ui.generate_camera_indexes(2)
    
    if camera_names == ['camera_1', 'camera_2']:
        print('test pass')
    else:
        print(f'Result is {camera_names}\nand it should be : [''camera_1'', ''camera_2'']')

def test_set_pos():
    hchipsize = 4432
    hsize = 1024
    
    pos1 = functions_ui.set_pos(1020, hsize, hchipsize)
    
    pos2 = functions_ui.set_pos(3412, hsize, hchipsize)

    pos3 = functions_ui.set_pos(1023, hsize, hchipsize)
    
    if pos1 == 1020 and pos2 == 3408 and pos3 == 1020:
        print("Test pass!")
    else:
        print("     Result are : "+str(pos1)+(" , ") + str(pos2)+(" , ") + str(pos3) +
              "\nand it should be : "+str(1020)+(" , ") + str(3408)+(" , ") + str(1020))
        
def test_set_size():
    hchipsize = 4432
    
    size1 = functions_ui.set_size(4400,hchipsize)
    
    size2 = functions_ui.set_size(4460, hchipsize)
                                  
    if size1 == 4400 and size2 == 4432:
        print("Test pass!")
    else:
        print("Result are : "+str(size1)+(" , ") + str(size2)+
              "\nand i should be : "+str(4400)+(" , ") + str(4432))

def test_QTime_to_seconds():
    'test the function QTime_to_seconds from functions_ui'
    hours = 2
    minutes = 15
    seconds = 30
    milliseconds = 32
    
    expected_seconds = 8130.032
    
    time = QTime(hours,minutes,seconds,milliseconds)
    
    total_seconds = functions_ui.QTime_to_seconds(time)
    
    if expected_seconds == total_seconds:
        print("Test pass!")
    else:
        print("Test not pass!\nResult is : " +str(total_seconds)+
          "\nand i should be : "+str(expected_seconds))
        
def test_seconds_to_QTime():
    'test the function seconds_to_QTime from functions_ui'
    hours = 2
    minutes = 15
    seconds = 30
    milliseconds = 32
    
    total_seconds = 8130.032
    
    time = functions_ui.seconds_to_QTime(total_seconds)
    
    print("Result is : "+str(time)+
          "\nand i should be :"+str(hours)+" , "+str(minutes)+" , "+str(seconds)+" , "+str(milliseconds))
    
    
def test_create_preview():
    frame = np.load("Images/DefaultExpName.npy")
    min_grayscale = 1200
    max_grayscale = 65535
    coef_grayscale = 255/(max_grayscale - min_grayscale)
    zoom = 0.25
    
    qt_image = functions_ui.create_preview_resize(frame, "grayscale", min_grayscale, max_grayscale, coef_grayscale, zoom)
    
    return qt_image
    
    