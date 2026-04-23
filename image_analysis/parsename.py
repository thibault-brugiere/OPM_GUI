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
    Parse filenames in a folder following the pattern:
    {channel}_volume_{image:04d}

    The file extension is ignored during parsing
    (e.g. '.tif', '.tiff').

    Only files matching the pattern are considered. Others are ignored.

    Parameters
    ----------
    folder : str | Path
        Folder containing the image files.

    Raises
    ------
    FileNotFoundError
        If the folder does not exist.
    NotADirectoryError
        If ``folder`` is not a directory.

    Returns
    -------
    dict[str, Any]
        Dictionary containing:
    - ``files``: list of dict with keys:
        ``path`` (Path), ``channel`` (str), ``image`` (int),
        sorted by (channel, image)
    - ``channels``: sorted list of unique channel names
    - ``images``: sorted list of unique image indices (int)
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
        
        if channel.startswith("deskew"):
            continue

        parsed_files.append({
            "path": path,
            "channel": channel,
            "image": image,
            "process": True,
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
    Parse filenames in a folder following the pattern:
    Position_{position}_{channel}_file_{file:04d}
    
    The file extension is ignored during parsing
    (e.g. '.tif', '.tiff', '.npy').
    
    Only files matching the pattern are considered. Others are ignored.

    Parameters
    ----------
    folder : str | Path
        Folder containing the image files.

    Raises
    ------
    FileNotFoundError
        If the folder does not exist.
    NotADirectoryError
        If ``folder`` is not a directory.

    Returns
    -------
    dict[str, Any]
    Dictionary containing:
        - ``files``: list of dict with keys:
          ``path`` (Path), ``position`` (int),
          ``channel`` (str), ``file`` (int),
          sorted by (position, channel, file)
        - ``positions``: sorted list of unique positions (int)
        - ``channels``: sorted list of unique channel names
        - ``file_indices``: sorted list of unique file indices (int)

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
            "process": True,
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

_PATTERN_LS3_ZARR = re.compile(r"^Position_(?P<position>\d{4})_(?P<channel>[A-Za-z0-9]+)_file$")

def parse_ls3_foldernames(folder: str | Path) -> dict[str, Any]:
    """
    Analyse les noms de fichiers d'un dossier selon le motif :
    Position_{position}_{channel}_file
    Le suffixe .zarr du dossier n'est pas pris en compte'

    :param folder:
        Dossier contenant les images.
    :type folder: str | Path

    :returns:
        Dictionnaire contenant :
            - ``files`` : liste triée des fichiers correspondants avec
              ``path``, ``channel`` et ``image``
            - ``positions`` : listre triée des positions uniques
            - ``channels`` : liste triée des canaux uniques
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

    for path in folder.iterdir():
        if not path.is_dir() :
            continue

        stem = path.stem
        match = _PATTERN_LS3_ZARR.match(stem)
        if match is None:
            continue

        position = int(match.group("position"))
        channel = match.group("channel")

        parsed_files.append({
            "path": path,
            "position" : position,
            "channel": channel,
            "process": True,
        })

        positions_set.add(position)
        channels_set.add(channel)

    parsed_files.sort(key=lambda item: (item["position"], item["channel"]))

    return {
        "files": parsed_files,
        "positions": sorted(positions_set),
        "channels": sorted(channels_set),
    }

_PATTERN_LS3_DESKEW_ZARR = re.compile(r"^deskew_Position_(?P<position>\d{4})_(?P<channel>[A-Za-z0-9]+)_file$")

def parse_ls3_deskew_foldernames(folder: str | Path) -> dict[str, Any]:
    """
    Parse folder names in a directory following the pattern:
    Position_{position}_{channel}_file

    The '.zarr' suffix is ignored during parsing.

    Only folders matching the pattern are considered. Others are ignored.

    Parameters
    ----------
    folder : str | Path
        Folder containing the Zarr directories.

    Raises
    ------
    FileNotFoundError
        If the folder does not exist.
    NotADirectoryError
        If ``folder`` is not a directory.

    Returns
    -------
    dict[str, Any]
        Dictionary containing:
            - ``files``: list of dict with keys:
              ``path`` (Path), ``position`` (int), ``channel`` (str),
              sorted by (position, channel)
            - ``positions``: sorted list of unique positions (int)
            - ``channels``: sorted list of unique channel names
    """
    folder = Path(folder)

    if not folder.exists():
        raise FileNotFoundError(f"Dossier introuvable : {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Ce n'est pas un dossier : {folder}")

    parsed_files: list[dict[str, Any]] = []
    positions_set: set[int] = set()
    channels_set: set[str] = set()

    for path in folder.iterdir():
        if not path.is_dir() :
            continue

        stem = path.stem
        match = _PATTERN_LS3_DESKEW_ZARR.match(stem)
        if match is None:
            continue

        position = int(match.group("position"))
        channel = match.group("channel")

        parsed_files.append({
            "path": path,
            "position" : position,
            "channel": channel,
            "process": True,
        })

        positions_set.add(position)
        channels_set.add(channel)

    parsed_files.sort(key=lambda item: (item["position"], item["channel"]))

    return {
        "files": parsed_files,
        "positions": sorted(positions_set),
        "channels": sorted(channels_set),
    }


def get_metadata(folder, filename = "GUI_parameters.txt"):
    """
    Load microscope metadata from a JSON file and extract key parameters.

    The JSON file must contain at least:
        - parameters["microscope"]["tilt_angle"]
        - parameters["experiment"]["aspect_ratio"]

    Parameters
    ----------
    folder : str | Path
        Directory containing the metadata file.
    filename : str, optional
        Name of the metadata file (default: "GUI_parameters.txt").

    Raises
    ------
    FileNotFoundError
        If the metadata file does not exist.
    KeyError
        If required fields are missing in the JSON structure.
    json.JSONDecodeError
        If the file is not a valid JSON.

    Returns
    -------
    dict[str, float]
        Dictionary containing:
            - ``angle``: microscope tilt angle (float)
            - ``aspect_ratio``: voxel aspect ratio (float)
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
    # folder_mda = r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260324_145316_Neurosphere_GFP_DIV7"
    # result_mda = parse_mda_filenames(folder_mda)
    
    # print("MDA folder")
    # metadata_mda = get_metadata(folder_mda)
    # print("px_size :", metadata_mda["px_size"])
    # print("angle :", metadata_mda["angle"])
    # print("aspect_ratio :", metadata_mda["aspect_ratio"])
    
    # folder_ls3 = r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260313_110909_Monica_Cos7_NHS-Esther_x4"
    # result_ls3 = parse_ls3_filenames(folder_ls3)
    
    # print("LS3 folder")
    # print("files :", result_ls3["files"])
    # metadata_ls3 = get_metadata(folder_ls3)
    # print("px_size :", metadata_ls3["px_size"])
    # print("aspect_ratio :", metadata_ls3["aspect_ratio"])
    # print("angle :", metadata_ls3["angle"])
    
    # print("LS3 ZARR folder")
    # folder_ls3_zarr = r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260313_110909_Monica_Cos7_NHS-Esther_x4_copie"
    # result_ls3_zarr = parse_ls3_foldernames(folder_ls3_zarr)
    # print('files :', result_ls3_zarr["files"])
    
    print("LS3 deskew ZARR folder")
    folder_ls3_zarr = r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260313_110909_Monica_Cos7_NHS-Esther_x4_copie"
    result_ls3_zarr = parse_ls3_deskew_foldernames(folder_ls3_zarr)
    print('files :', result_ls3_zarr["files"])