# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 14:29:22 2025

@author: tbrugiere
"""

import os
import re

# Dossier contenant tes fichiers
folder = "C:/Users/tbrugiere/Documents/Images_OPM/20251128_161746_Lipid_Droplets_Timelaps/Imaris_OrignalImages"

# pattern = re.compile(r"stack_ch(?P<chan>\d+)_stack(?P<time>\d+)_.*")
pattern = re.compile(r"(?P<chan>[A-Za-z]+)_volume_(?P<time>\d+)\.tif[f]?$")

for filename in os.listdir(folder):
    if not filename.lower().endswith((".tif", ".tiff")):
        continue

    m = pattern.match(filename)
    if not m:
        continue

    chan = m.group("chan")
    time = int(m.group("time"))
    
    print(f"Image : {chan}_{time}")
    
    if chan == "BFP" :
        chan_num = 0
    elif chan == "GFP" :
        chan_num = 1
            

    new_name = f"img_C{chan_num}_T{time:03d}.tif"

    # Renommage
    print(f"{filename}  →  {new_name}")
    os.rename(os.path.join(folder, filename), 
              os.path.join(folder, new_name))

print("Terminé !")