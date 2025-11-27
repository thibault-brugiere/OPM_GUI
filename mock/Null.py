# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 13:40:46 2025

@author: tbrugiere
"""

class NullObject:
    def __getattr__(self, name):
        return self

    def __call__(self, *args, **kwargs):
        return self

    def __setattr__(self, name, value):
        pass

    def __repr__(self):
        return "<NullObject>"