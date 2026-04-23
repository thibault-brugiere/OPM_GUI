# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 16:45:35 2026

@author: tbrugiere
the progress_folder_callback, progress_file_callback and stop_requested_callback
are present in the file GUI_pretreatement_worker.py file
"""

from __future__ import annotations

from pathlib import Path
import shutil
from typing import Sequence

import numpy as np
import tifffile
import zarr

import parsename


def tiffs_to_zarr(file_path_list: Sequence[str | Path],
                  zarr_path: str | Path,
                  chunks: tuple[int, int, int] | None = None,
                  overwrite: bool = False,
                  read_z_chunk: int | None = None,
                  zarr_format: int = 3,
                  progress_file_callback = None,
                  stop_requested_callback = None) -> dict:
    """
    Convert a sequence of 3D TIFF files with identical YX shape into a single
    Zarr array by concatenating them along the Z axis.

    Memory usage is bounded by reading and writing only one Z chunk at a time.

    Parameters
    ----------
    file_path_list : Sequence[str | Path]
        Ordered list of TIFF files. Each file must have shape ``(Z, Y, X)``.
    zarr_path : str | Path
        Destination path of the Zarr store, e.g. ``"volume.zarr"``.
    chunks : tuple[int, int, int] | None, optional
        Chunk shape of the output Zarr array in ``(Z, Y, X)`` order.
        If ``None``, a conservative default is used.
    overwrite : bool, optional
        If ``True``, overwrite the output store if it already exists.
    read_z_chunk : int | None, optional
        Number of Z planes to read from each TIFF file at once.
        If ``None``, uses ``chunks[0]`` when available, otherwise a default value.
    zarr_format : int, optional
        Zarr format version to use. Default is 3.
    progress_file_callback : callable | None, optional
        Callback used to report progress during file conversion.
    stop_requested_callback : callable | None, optional
        Callback used to request early interruption of the conversion.

    Raises
    ------
    ValueError
        If input TIFF files have inconsistent shape or incompatible metadata.
    FileExistsError
        If the output store already exists and ``overwrite=False``.

    Returns
    -------
    dict
        Dictionary containing summary metadata of the generated Zarr array,
        including shape, dtype, chunks, and per-file Z sizes.
    """
    if not file_path_list:
        raise ValueError("file_path_list must not be empty.")

    file_paths = [Path(p) for p in file_path_list]
    zarr_path = Path(zarr_path)

    if zarr_path.exists() and not overwrite:
        raise FileExistsError(
            f"Zarr store already exists: {zarr_path}. "
            "Use overwrite=True to replace it."
        )

    shapes: list[tuple[int, int, int]] = []
    dtypes: list[np.dtype] = []

    for file_path in file_paths:
        with tifffile.TiffFile(file_path) as tif:
            shape = tuple(tif.series[0].shape)
            dtype = np.dtype(tif.series[0].dtype)

        if len(shape) != 3:
            raise ValueError(
                f"{file_path} has shape {shape}, expected a 3D TIFF (Z, Y, X)."
            )

        shapes.append(shape)
        dtypes.append(dtype)

    yx_set = {(shape[1], shape[2]) for shape in shapes}
    if len(yx_set) != 1:
        raise ValueError(f"All TIFFs must have identical (Y, X). Found: {yx_set}")

    dtype_set = set(dtypes)
    if len(dtype_set) != 1:
        raise ValueError(f"All TIFFs must have identical dtype. Found: {dtype_set}")

    z_sizes = [shape[0] for shape in shapes]
    total_z = int(np.sum(z_sizes))
    y_size, x_size = shapes[0][1], shapes[0][2]
    dtype = dtypes[0]

    if chunks is None:
        z_chunk = min(64, total_z)
        x_chunk = min(256, x_size)
        chunks = (z_chunk, y_size, x_chunk)

    if read_z_chunk is None:
        read_z_chunk = max(1, chunks[0])

    zarr_array = zarr.open(
        str(zarr_path),
        mode="w",
        shape=(total_z, y_size, x_size),
        chunks=chunks,
        dtype=dtype,
        zarr_format=zarr_format,
        compression = None,
    )

    global_z0 = 0

    for file_index, file_path in enumerate(file_paths):

        if stop_requested_callback is not None and stop_requested_callback() :
            return
        
        arr = tifffile.imread(file_path)
        file_z = z_sizes[file_index]
        
        for local_z0 in range(0, file_z, read_z_chunk):
            local_z1 = min(local_z0 + read_z_chunk, file_z)
            dst_z0 = global_z0 + local_z0
            dst_z1 = global_z0 + local_z1
        
            zarr_array[dst_z0:dst_z1, :, :] = arr[local_z0:local_z1, :, :]
        
        del arr
        
        if progress_file_callback is not None :
            progress_file_callback(file_index + 1,len(file_paths))
        else:
            print(f"[TIFF -> Zarr] file {file_index + 1}/{len(file_paths)}: {file_path.name}")

        global_z0 += file_z

    zarr_array.attrs["source_files"] = [str(p) for p in file_paths]
    zarr_array.attrs["source_z_sizes"] = z_sizes
    zarr_array.attrs["source_shape_per_file"] = [list(s) for s in shapes]

    return {
        "shape": (total_z, y_size, x_size),
        "dtype": str(dtype),
        "chunks": tuple(chunks),
        "source_z_sizes": z_sizes,
        "zarr_path": str(zarr_path),
    }

def zarr_to_small_tiffs(zarr_path: str | Path,
                        output_dir: str | Path,
                        max_z_size: int,
                        base_name: str = "volume",
                        bigtiff: bool = True,
                        compression: str | None = None,
                        progress_file_callback = None,
                        stop_requested_callback = None) -> list[str]:
    """
    Export a Zarr array of shape ``(Z, Y, X)`` into several TIFF files by
    splitting it along Z into smaller stacks.

    Parameters
    ----------
    zarr_path : str | Path
        Path to the input Zarr store.
    output_dir : str | Path
        Destination directory for the output TIFF files.
    max_z_size : int
        Maximum number of Z planes per output TIFF file.
    base_name : str, optional
        Prefix used for output TIFF filenames.
    bigtiff : bool, optional
        Whether to write TIFF files using the BigTIFF format.
        Passed to ``tifffile.imwrite``.
    compression : str | None, optional
        Compression method passed to ``tifffile.imwrite``.
        Use ``None`` for the simplest and fastest output.
    progress_file_callback : callable | None, optional
        Callback used to report progress during TIFF export.
    stop_requested_callback : callable | None, optional
        Callback used to request early interruption of the export.

    Raises
    ------
    ValueError
        If the input Zarr array is not 3D or if ``max_z_size`` is not valid.

    Returns
    -------
    list[str]
        List of written TIFF file paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    zarr_array = zarr.open_array(str(zarr_path), mode="r")

    if len(zarr_array.shape) != 3:
        raise ValueError(
            f"Expected a 3D Zarr array (Z, Y, X), got shape {zarr_array.shape}."
        )

    total_z, _, _ = zarr_array.shape
    
    if max_z_size is None:
        z_sizes = [zarr_array.shape[0]]
    else :
        n_files = zarr_array.shape[0] // max_z_size
        rest_images = zarr_array.shape[0] % max_z_size
        z_sizes = []
        for k in range(n_files) :
            z_sizes.append(max_z_size)
        z_sizes.append(rest_images)
    
    z_sizes = [int(v) for v in z_sizes]

    if np.sum(z_sizes) != total_z:
        raise ValueError(
            f"Sum(z_sizes) = {np.sum(z_sizes)} but Zarr Z size = {total_z}."
        )

    file_paths: list[str] = []
    start = 0

    for idx, file_z in enumerate(z_sizes):
            
        end = start + file_z
        out_path = output_dir / f"{base_name}_file_{idx:04d}.tif"

        if progress_file_callback is not None :
            progress_file_callback(idx + 1, len(z_sizes))
        else:
            print(f"[Zarr -> TIFF] file {idx + 1}/{len(z_sizes)}: {out_path.name}")
            
        if stop_requested_callback is not None and stop_requested_callback() :
            return

        # This slice reads only the required sub-volume.
        block = np.asarray(zarr_array[start:end, :, :])

        tifffile.imwrite(
            out_path,
            block,
            bigtiff=bigtiff,
            compression=compression,
        )

        file_paths.append(str(out_path))
        del block
        start = end

    return file_paths

def delete_zarr(path:str):
    """
    Delete a Zarr store (directory) and all its contents.
    
    Parameters
    ----------
    path : str | Path
        Path to the Zarr directory (must end with '.zarr').
    
    Raises
    ------
    FileNotFoundError
        If the path does not exist.
    ValueError
        If the path is not a directory or does not point to a '.zarr' store.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist.")
    
    if not path.is_dir():
        raise ValueError(f"{path} is not a directory (not a valid Zarr store).")
        
    if path.suffix != ".zarr":
        raise ValueError("Refusing to delete non-.zarr directory")

    shutil.rmtree(path)
    
def auto_convert_tiffs_to_zarr(folder :str,
                               progress_file_callback = None,
                               progress_folder_callback = None,
                               stop_requested_callback=None):
    """
    Convert original tiff images acquired during LS3 experiment into zarr file

    Parameters
    ----------
    folder : str
        folder containing images to convert
    progress_folder_callback : None, optional
        External process use to follow the advancement of the program
    progress_file_callback : None, optional
        External process use to follow the advancement of the program
    stop_requested_callback : None, optional
        External process use to stop the advancement of the program

    Returns
    -------
    None.

    """
    
    parse_ls3 = parsename.parse_ls3_filenames(folder)
    processed_images = 0
    total_images = len(parse_ls3["channels"]) * len(parse_ls3["positions"])
    
    for channel in parse_ls3["channels"]:
        for position in parse_ls3["positions"]:
    
            files = []
            for file in parse_ls3["files"]:
                if file["channel"] == channel :
                    if file["position"] == position :
                        files.append(file['path'])
            
            zarr_path = folder + r"\Position_" + f"{position:04d}_{channel}_file.zarr"
            
            if progress_folder_callback is not None :
                progress_folder_callback(processed_images, total_images, f"{position:04d}_{channel}_file")
                processed_images += 1
                
            if stop_requested_callback is not None and stop_requested_callback() :
                return

            tiffs_to_zarr(files, zarr_path, overwrite=True,
                          progress_file_callback = progress_file_callback,
                          stop_requested_callback = stop_requested_callback)
            
    if progress_folder_callback is not None :
        progress_folder_callback(processed_images, total_images, f"{position:04d}_{channel}_file")
            
def auto_convert_zarr_to_tiffs(folder: str,
                               delete = False,
                               max_z_size = None,
                               progress_folder_callback = None,
                               progress_file_callback = None,
                               stop_requested_callback=None):
    """
    

    Parameters
    ----------
    folder : str
        folder containing images to convert
    delete : bool, The default is False.
        to delete automatically the processed files
    max_z_size : TYPE, optional
        Number of Z planes per output TIFF.
        The sum must match the Z size of the Zarr array.
        The default is None.
    progress_folder_callback : None, optional
        External process use to follow the advancement of the program
    progress_file_callback : None, optional
        External process use to follow the advancement of the program
    stop_requested_callback : None, optional
        External process use to stop the advancement of the program

    Returns
    -------
    None.

    """
    
    parse_ls3_deskew = parsename.parse_ls3_deskew_foldernames(folder)
    
    processed_images = 0
    total_images = len(parse_ls3_deskew["channels"]) * len(parse_ls3_deskew["positions"])
    
    for channel in parse_ls3_deskew["channels"]:
        for position in parse_ls3_deskew["positions"]:
            
            if stop_requested_callback is not None and stop_requested_callback() :
                return
            
            if progress_folder_callback is not None :
                progress_folder_callback(processed_images, total_images, f"{position:04d}_{channel}_file")
                processed_images += 1
                
            zarr_file = folder + r"\deskew_Position_" + f"{position:04d}_{channel}_file.zarr"
            out = folder + r"\deskew_tif"          
                
            zarr_to_small_tiffs(zarr_file , out, max_z_size,
                                f"deskew_Position_{position}_{channel}",
                                progress_file_callback = progress_file_callback,
                                stop_requested_callback = stop_requested_callback)
            
            if delete :
                delete_zarr(zarr_file)
                
    if progress_folder_callback is not None :
        progress_folder_callback(processed_images, total_images, f"{position:04d}_{channel}_file")
        
##############################################################################

if __name__ == "__main__" :
    import time as t

    folders = [
        # r"C:\Users\tbrugiere\Documents\Images_OPM\20260330_154402_Image",
        # r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260313_110909_Monica_Cos7_NHS-Esther_x4",
        r"C:\Users\tbrugiere\Documents\Images_OPM\20260327_Tests_Treatment\20260313_110909_Monica_Cos7_NHS-Esther_x4_copie",
        ]
    
    # Convert TIFFS in ZARR
    # t0 = t.time()
    
    # for folder in folders :
    #     parse_ls3 = parsename.parse_ls3_filenames(folder)
        
    #     for channel in parse_ls3["channels"]:
    #         for position in parse_ls3["positions"]:
        
    #             files = []
    #             for file in parse_ls3["files"]:
    #                 if file["channel"] == channel :
    #                     if file["position"] == position :
    #                         files.append(file['path'])
                
    #             zarr_path = folder + r"\Position_" + f"{position:04d}_{channel}_file.zarr"

    #             tiffs_to_zarr(files, zarr_path, overwrite=True)
        
    # t1 = t.time()
    
    # print(f"total conversion time : {t1-t0}s")
    
    # Convert ZARR in tiffs
    t0 = t.time()
    
    for folder in folders:
        parse_ls3_deskew = parsename.parse_ls3_deskew_foldernames(folder)
        
        for channel in parse_ls3_deskew["channels"]:
            for position in parse_ls3_deskew["positions"]:
    
                zarr_file = folder + r"\deskew_Position_" + f"{position:04d}_{channel}_file.zarr"
                out = folder + r"\deskew_tif"
                z_sizes = None
                zarr_to_small_tiffs(zarr_file , out, z_sizes, f"deskew_Position_{position}_{channel}")
                delete_zarr(zarr_file)
        
    t1 = t.time()
    
    print(f"total conversion time : {t1-t0}s")