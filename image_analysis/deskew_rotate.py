# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:10:54 2026

@author: tbrugiere
"""

import numpy as np
from scipy import ndimage



def _shear_integer_y(volume: np.ndarray, shift_y_px_per_plane: int) -> np.ndarray:
    """
    Deskew by integer shear along Y: each Z-slice shifted by z*shift_y pixels.

    Parameters
    ----------
    volume_zyx : np.ndarray
        Input volume with shape (Z, Y, X).
    shift_y_px_per_plane : int
        Integer pixel shift along Y per Z-plane (can be negative).

    Returns
    -------
    np.ndarray
        Deskewed volume with shape (Z, Y + Z*abs(shift), X).
    """
    if volume_zyx.ndim != 3:
        raise ValueError("Expected a 3D array (Z, Y, X).")

    Z, Y, X = volume_zyx.shape
    shift = int(shift_y_px_per_plane)
    if  shift == 0:
        return volume_zyx.copy()

    pad_y = Z * abs(shift)
    out = np.zeros((Z, Y + pad_y, X), dtype=volume_zyx.dtype)

    if shift > 0:
        for z in range(Z):
            y0 = z * shift
            out[z, y0:y0 + Y, :] = volume_zyx[z]
    else:
        # shift negative: start near the bottom
        shift = -shift
        for z in range(Z):
            y0 = pad_y - z * shift
            out[z, y0:y0 + Y, :] = volume_zyx[z]

    return out


def rotate_about_x_physical(volume_zyx: np.ndarray,
                            dy_um: float,
                            dz_um: float,
                            theta_deg: float,
                            y_original_size: float = None,
                            order: int = 1,
                            cval: float = 0.0) -> np.ndarray:
    """
    Rotate a (Z,Y,X) volume around X axis, i.e. rotate in the (Z,Y) plane,
    while accounting for anisotropic voxel size (dy != dz).

    This performs ONE interpolation (affine transform). Use integer shear first.

    Parameters
    ----------
    volume_zyx : np.ndarray
        Volume shape (Z, Y, X).
    dy_um : float
        Pixel size along Y in micrometers.
    dz_um : float
        Spacing between Z planes in micrometers.
    theta_deg : float
        Rotation angle in degrees (positive/negative per your convention).
    y_original_size: int, optionnal
        Original Y size before deskew.
    order : int
        Interpolation order for ndimage.affine_transform (1 = linear, 3 = cubic).
        For speed + low ringing, order=1 is recommended.
    cval : float
        Constant fill value outside boundaries (0 is typical).

    Returns
    -------
    np.ndarray
        Rotated volume (same shape as input by default).
        (If you want tight bounds, we can extend canvas, but it costs memory.)
    """
    Z, Y, X = volume_zyx.shape
    theta = np.deg2rad(theta_deg)

    # Work in index coordinates but correct geometry via scaling:
    # physical coords p = S * i, with S = diag(dz, dy)
    # rotation in physical coords: p' = R * p
    # => i' = S^-1 * R * S * i
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    S = np.array([[dz_um, 0.0],
                  [0.0, dy_um]], dtype=np.float64)
    R = np.array([[cos_theta, -sin_theta],
                  [sin_theta,  cos_theta]], dtype=np.float64)
    A2 = np.linalg.inv(S) @ R @ S  # 2x2 acting on (z,y) indices

    # Build 3x3 affine for (z,y,x): keep x unchanged
    A = np.eye(3, dtype=np.float64)
    A[0:2, 0:2] = A2

    # Centered rotation: offset so that center maps to center
    # center_in = np.array([(Z - 1) / 2.0, (Y - 1) / 2.0, (X - 1) / 2.0], dtype=np.float64)
    # center_out = center_in.copy()
    # offset = center_in - A @ center_out

    # # affine_transform maps output coords -> input coords: input = A @ output + offset
    # # (Our A already represents that mapping for centered transform.)
    # rotated = ndimage.affine_transform(
    #     volume_zyx,
    #     matrix=A,
    #     offset=offset,
    #     output_shape=volume_zyx.shape,
    #     order=order,
    #     mode="constant",
    #     cval=cval,
    #     prefilter=(order > 1)
    # )
    
    # --- compute rotated bounding box in (Z, Y) ---
    corners_zy = np.array([
        [0,     0],
        [0,     Y - 1],
        [Z - 1, 0],
        [Z - 1, Y - 1],
    ], dtype=np.float64)
    
    center_zy = np.array([(Z - 1) / 2.0, (Y - 1) / 2.0], dtype=np.float64)
    corners_centered = corners_zy - center_zy[None, :]
    
    rotated_corners = corners_centered @ A2.T
    
    min_zy = rotated_corners.min(axis=0)
    max_zy = rotated_corners.max(axis=0)
    
    # out_Z = int(np.ceil(max_zy[0] - min_zy[0] + 1))
    if y_original_size is not None :
        out_Z = int(np.ceil(((y_original_size - 1) * dy_um * abs(np.cos(theta))) / dz_um)) + 1
    else:
        out_Z = Z
        
    out_Y = int(np.ceil(max_zy[1] - min_zy[1] + 1))
    out_X = X
    
    output_shape = (out_Z, out_Y, out_X)
    
    # center of output box in its own index space
    center_out = np.array([(out_Z - 1) / 2.0, (out_Y - 1) / 2.0, (X - 1) / 2.0], dtype=np.float64)
    center_in = np.array([(Z - 1) / 2.0, (Y - 1) / 2.0, (X - 1) / 2.0], dtype=np.float64)
    
    offset = center_in - A @ center_out
    
    rotated = ndimage.affine_transform(
        volume_zyx,
        matrix=A,
        offset=offset,
        output_shape=output_shape,
        order=order,
        mode="constant",
        cval=cval,
        prefilter=(order > 1)
    )

    return rotated


def deskew_and_rotate_opm(volume_zyx: np.ndarray,
                          dy_um: float,
                          dz_um: float,
                          shift_y_px_per_plane: int,
                          theta_deg: float,
                          order: int = 1) -> np.ndarray:
    """
    Full pipeline: integer deskew (shear) then rotation around X with anisotropy-aware geometry.

    Parameters
    ----------
    volume_zyx : np.ndarray
        Input volume (Z, Y, X).
    dy_um : float
        Y pixel size (um).
    dz_um : float
        Z spacing (um).
    shift_y_px_per_plane : int
        Integer shift in Y per Z plane (px).
    theta_deg : float
        Rotation angle around X (deg).
    order : int
        Interp order for rotation. 1 recommended for speed.

    Returns
    -------
    np.ndarray
        Deskewed + rotated volume.
    """
    
    _, size_y, _ = volume_zyx.shape
    
    v = _shear_integer_y(volume_zyx, shift_y_px_per_plane)
    # Rotation changes the "apparent" FOV; keeping same shape is simplest/fastest.
    # If you want a larger canvas to avoid cropping, tell me and I’ll adapt.
    v = rotate_about_x_physical(v, dy_um=dy_um, dz_um=dz_um, theta_deg=theta_deg, order=order, cval=0.0, y_original_size = size_y)
    return v


###############################################################################
if __name__ == '__main__':
    from pathlib import Path
    import os
    import tifffile
    
    
    dy_um = 0.155
    dz_um = 0.520
    shift = 4
    theta = -40

    folder = Path(r"D:\Projets_Python\OPM_GUI\Images\20260304_115005_LS3_Beads_170µm_GFP")
    filename = "Position_0001_GFP_file_"
    
    for k in range(4):
        file_path = os.path.join(folder, f'{filename}{k:04d}.tif')
        if k == 0 :
            volume_zyx = tifffile.imread(file_path)
        else:
            volume_zyx = np.concatenate((volume_zyx, tifffile.imread(file_path)))
    
    # volume_zyx = tifffile.imread(file_path)
    print("Images oppened")

    out_volume = deskew_and_rotate_opm(volume_zyx, dy_um, dz_um, shift, theta)
    
    print("image deskewed_rotated")
    
    # out_volume = shear_volume
    print("image deskew resampled")
    
    output_file_path = f'{folder}/dekew-rotate_{filename}.tif'
    tifffile.imwrite(output_file_path, out_volume, compression='zlib')
    print("image saved")