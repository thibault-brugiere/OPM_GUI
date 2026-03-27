# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 10:08:14 2026

@author: tbrugiere
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
from typing import Any


_PATTERN_MDA = re.compile(r"^(?P<channel>.+?)_volume_(?P<image>\d{4})$")


def parse_mda_filenames(folder: str | Path) -> dict[str, Any]:
    """
    Analyse les noms de fichiers d'un dossier selon le motif :
    {channel}_volume_{image:04d}

    Le suffixe de fichier n'est pas pris en compte pour l'analyse
    (ex. '.tif', '.tiff', '.npy').

    :param folder:
        Dossier contenant les images.
    :type folder: str | Path

    :returns:
        Dictionnaire contenant :
            - ``files`` : liste triée des fichiers correspondants avec
              ``path``, ``channel`` et ``image``
            - ``channels`` : liste triée des canaux uniques
            - ``images`` : liste triée des indices image uniques
    :rtype: dict[str, Any]

    :raises FileNotFoundError:
        Si le dossier n'existe pas.
    :raises NotADirectoryError:
        Si ``folder`` n'est pas un dossier.
    """
    folder = Path(folder)

    if not folder.exists():
        raise FileNotFoundError(f"Dossier introuvable : {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Ce n'est pas un dossier : {folder}")

    parsed_files: list[dict[str, Any]] = []
    channels_set: set[str] = set()
    images_set: set[int] = set()

    for path in folder.iterdir():
        if not path.is_file():
            continue

        stem = path.stem
        match = _PATTERN_MDA.match(stem)
        if match is None:
            continue

        channel = match.group("channel")
        image = int(match.group("image"))

        parsed_files.append({
            "path": path,
            "channel": channel,
            "image": image,
        })

        channels_set.add(channel)
        images_set.add(image)

    parsed_files.sort(key=lambda item: (item["channel"], item["image"]))

    return {
        "files": parsed_files,
        "channels": sorted(channels_set),
        "images": sorted(images_set),
    }

_PATTERN_LS3 = re.compile(r"^Position_(?P<position>\d{4})_(?P<channel>[A-Za-z0-9]+)_file_(?P<index>\d{4})$")

def parse_ls3_filenames(folder: str | Path) -> dict[str, Any]:
    """
    Analyse les noms de fichiers d'un dossier selon le motif :
    Position_{position}_{channel}_file_{file:04d}

    Le suffixe de fichier n'est pas pris en compte pour l'analyse
    (ex. '.tif', '.tiff', '.npy').

    :param folder:
        Dossier contenant les images.
    :type folder: str | Path

    :returns:
        Dictionnaire contenant :
            - ``files`` : liste triée des fichiers correspondants avec
              ``path``, ``channel`` et ``image``
            - ``positions`` : listre triée des positions uniques
            - ``channels`` : liste triée des canaux uniques
            - ``files`` : liste triée des indices fichiers uniques
    :rtype: dict[str, Any]

    :raises FileNotFoundError:
        Si le dossier n'existe pas.
    :raises NotADirectoryError:
        Si ``folder`` n'est pas un dossier.
    """
    folder = Path(folder)

    if not folder.exists():
        raise FileNotFoundError(f"Dossier introuvable : {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Ce n'est pas un dossier : {folder}")

    parsed_files: list[dict[str, Any]] = []
    positions_set: set[int] = set()
    channels_set: set[str] = set()
    index_set: set[int] = set()

    for path in folder.iterdir():
        if not path.is_file():
            continue

        stem = path.stem
        match = _PATTERN_LS3.match(stem)
        if match is None:
            continue

        position = int(match.group("position"))
        channel = match.group("channel")
        index = int(match.group("index"))

        parsed_files.append({
            "path": path,
            "position" : position,
            "channel": channel,
            "index": index,
        })

        positions_set.add(position)
        channels_set.add(channel)
        index_set.add(index)

    parsed_files.sort(key=lambda item: (item["position"], item["channel"], item["index"]))

    return {
        "files": parsed_files,
        "positions": sorted(positions_set),
        "channels": sorted(channels_set),
        "index": sorted(index_set),
    }


def get_metadata(folder, filename = "GUI_parameters.txt"):
    """
    Load microscope metadata from a JSON file and extract key parameters.
    
    The function expects a JSON file containing at least the following fields:
        - parameters["microscope"]["tilt_angle"]
        - parameters["experiment"]["aspect_ratio"]
    
    :param folder:
        Directory containing the metadata file.
    :type folder: str | Path
    
    :param filename:
        Name of the metadata file (default: "GUI_parameters.txt").
    :type filename: str
    
    :returns:
        Dictionary containing:
            - ``angle`` : tilt angle of the microscope (float)
            - ``aspect_ratio`` : voxel aspect ratio (float)
    :rtype: dict[str, float]
    
    :raises FileNotFoundError:
        If the metadata file does not exist.
    :raises KeyError:
        If required fields are missing in the JSON structure.
    :raises json.JSONDecodeError:
        If the file is not a valid JSON.
    """
    folder = Path(folder)
    file_path = os.path.join(folder, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No metadata file found: {file_path}")
        
    with open(file_path, 'r') as json_file:
        parameters = json.load(json_file)
    return {
        "angle": float(parameters["microscope"]["tilt_angle"]),
        "aspect_ratio": float(parameters["experiment"]["aspect_ratio"]),
        "px_size": float(parameters["cameras"]["camera_0"]["sample_pixel_size"])}

def get_preprocess_steps(folder, filename = "preprocess_parameters.txt"):
    folder = Path(folder)
    file_path = os.path.join(folder, filename)
    if not os.path.exists(file_path):
        return None
        
    with open(file_path, 'r') as json_file:
        parameters = json.load(json_file)
    return parameters

###############################################################################
if __name__ == "__main__":
    folder_mda = r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260324_145316_Neurosphere_GFP_DIV7"
    result_mda = parse_mda_filenames(folder_mda)
    
    print("MDA folder")
    # print("Channels :", result_mda["channels"])
    # print("Images   :", result_mda["images"])
    metadata_mda = get_metadata(folder_mda)
    print("px_size :", metadata_mda["px_size"])
    print("angle :", metadata_mda["angle"])
    print("aspect_ratio :", metadata_mda["aspect_ratio"])
    
    folder_ls3 = r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260313_110909_Monica_Cos7_NHS-Esther_x4"
    result_ls3 = parse_ls3_filenames(folder_ls3)
    
    print("LS3 folder")
    print("files :", result_ls3["files"])
    # print("positions :", result_ls3["positions"])
    # print("channels :", result_ls3["channels"])
    # print("index :", result_ls3["index"])
    metadata_ls3 = get_metadata(folder_ls3)
    print("px_size :", metadata_ls3["px_size"])
    print("aspect_ratio :", metadata_ls3["aspect_ratio"])
    print("angle :", metadata_ls3["angle"])