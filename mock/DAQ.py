# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 11:34:21 2025

@author: tbrugiere
"""

class functions_daq:
    def get_connected_daq_devices():
        return ['Dev1']

    def analog_out(tension=0, output_channel='Dev1/ao0'):
        # print("generation " + str(tension) + " V at " + output_channel)
        pass
    
    def digital_out (signal = True, line_name = 'Dev1/port0/line3'):
        # if signal:
        #     print("Start signal at " + line_name)
        # else:
        #     print("Stop signal at " + line_name)
        pass