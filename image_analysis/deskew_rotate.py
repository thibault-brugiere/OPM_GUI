# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 15:10:54 2026

@author: tbrugiere
"""

import math
import numpy as np
from scipy import ndimage

def _px_shift_calculation(aspect_ratio:float, angle:float, angle_unit:str = "rad", tolerance = 0.0001) -> int:
    """
    Compute the integer pixel shift per Z step required for OPM deskewing.

    The deskew operation assumes that the lateral shift between consecutive
    planes is an integer number of pixels. This function computes the pixel
    shift from the voxel aspect ratio and the tilt angle, and checks that
    the result is compatible with this constraint.

    Parameters
    ----------
    aspect_ratio : float
        Voxel aspect ratio (typically dz / dx). should be > 0
    angle : float
        Tilt angle of the oblique plane.
    angle_unit : str, optional
        Unit of the input angle: ``"rad"`` for radians or ``"deg"`` for
        degrees (default: ``"rad"``).
    tolerance : int, optional
        tolerance for the px_shift to be an integer (in function math.isclose)

    Returns
    -------
    int
        Integer pixel shift per Z plane.
    """
    angle = angle if angle_unit == "rad" else np.deg2rad(angle)
    
    if aspect_ratio <= 0:
        raise ValueError('aspect_ratio should be positive')
    
    if angle <= - math.pi or angle >= math.pi :
        raise ValueError(f'angle should be > 0 and < math.pi : {angle}')
                                                         
    px_shift = aspect_ratio/math.tan(angle)
    
    int_px_shift = round(px_shift)
    
    if not math.isclose(px_shift, int_px_shift, rel_tol=tolerance):
        raise ValueError(f'Aspect ratio is not legal, pixel shift = {px_shift}')
        
    return int(int_px_shift)

def _shear_integer_y(volume: np.ndarray, shift_y_px_per_plane: int) -> np.ndarray:
    """
    Apply an integer shear along Y on a 3D volume of shape (Z, Y, X).

    Each plane z is shifted along Y by:
        shift(z) = z * shift_y_px_per_plane

    Parameters
    ----------
    volume_zyx : np.ndarray
        Input volume of shape (Z, Y, X).
    shift_y_px_per_plane : int
        Integer shift in Y per Z-plane. Can be negative.

    Returns
    -------
    np.ndarray
        Sheared volume of shape (Z, Y + (Z - 1)*abs(shift), X).
    """
    if volume.ndim != 3:
        raise ValueError("Expected a 3D array (Z, Y, X).")

    z_size, y_size, x_size = volume.shape
    shift = int(shift_y_px_per_plane)
    if  shift == 0:
        return volume.copy()

    pad_y = z_size * abs(shift)
    out = np.zeros((z_size, y_size + pad_y, x_size), dtype=volume.dtype)

    if shift > 0:
        for z in range(z_size):
            y0 = z * shift
            out[z, y0:y0 + y_size, :] = volume[z]
    else:
        # shift negative: start near the bottom
        shift = -shift
        for z in range(z_size):
            y0 = pad_y - z * shift
            out[z, y0:y0 + y_size, :] = volume[z]

    return out

def rotate_about_x_physical(volume: np.ndarray,
                            dy_um: float,
                            dz_um: float,
                            theta_deg: float,
                            y_original_size: float = None,
                            order: int = 1,
                            cval: float = 0.0) -> np.ndarray:
    """
    Rotate a 3D volume around X, i.e. in the (Z, Y) plane, while accounting
    for anisotropic voxel size.

    Geometry
    --------
    The rotation is defined in physical space:
        p = S @ i
        p_rot = R @ p
        i_rot = S^-1 @ R @ S @ i

    where:
        - i are index coordinates in (z, y),
        - p are physical coordinates in micrometers,
        - S = diag(dz_um, dy_um),
        - R is the 2D rotation matrix.

    The output canvas is computed from the forward transform of the input corners.
    The transform passed to scipy.ndimage.affine_transform is then the inverse
    mapping required by SciPy.

    Parameters
    ----------
    volume_zyx : np.ndarray
        Input volume of shape (Z, Y, X).
    dy_um : float
        Pixel size along Y in micrometers.
    dz_um : float
        Plane spacing along Z in micrometers.
    theta_deg : float
        Rotation angle in degrees.
    y_original_size: float or None, optionnal
        Original size of the image in the y axis, use to get the dimension of the
        out cannevas
    order : int, optional
        Interpolation order for scipy.ndimage.affine_transform.
    cval : float, optional
        Fill value outside the input volume.

    Returns
    -------
    np.ndarray
        Rotated volume with tight output canvas.
    """
    
    if volume.ndim != 3:
        raise ValueError("Expected a 3D array with shape (Z, Y, X).")
    if dy_um <= 0 :
        raise ValueError("dy_um must be > 0.")
    if dz_um <= 0:
        raise ValueError("dz_um must be > 0.")
    if order not in (0, 1, 2, 3, 4, 5):
        raise ValueError("order must be an integer between 0 and 5.")    
        
    z_size, y_size, x_size = volume.shape
    theta = np.deg2rad(-theta_deg)

    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    # ------------------------------------------------------------------
    # 1) Forward linear transform in index space, corrected for anisotropy
    # ------------------------------------------------------------------

    scale_zy = np.array([[dz_um, 0.0],
                  [0.0, dy_um]], dtype=np.float64)
    rotate_zy = np.array([[cos_theta, -sin_theta],
                  [sin_theta,  cos_theta]], dtype=np.float64)
    
    # Forward mapping in index coordinates: input -> rotated output
    forward_zy = np.linalg.inv(scale_zy) @ rotate_zy @ scale_zy  # 2x2 acting on (z,y) indices

    # Build 3x3 affine for (z,y,x): keep x unchanged
    forward_3d  = np.eye(3, dtype=np.float64)
    forward_3d [0:2, 0:2] = forward_zy

    # ---------------------------------------------------------
    # 2) Compute the tight forward bounding box in the (Z, Y) plane
    # ---------------------------------------------------------
    center_in = np.array([
        (z_size - 1) / 2.0,
        (y_size - 1) / 2.0,
        (x_size - 1) / 2.0,
        ], dtype=np.float64)
    
    corners_zy = np.array([
        [0.0,     0.0],
        [0.0,     y_size - 1.0],
        [z_size - 1, 0.0],
        [z_size - 1.0, y_size - 1.0],
    ], dtype=np.float64)
    
    centered_corners_zy = corners_zy - center_in[None, 0:2]
    rotated_corners = centered_corners_zy @ forward_zy.T
    
    min_zy = rotated_corners.min(axis=0)
    max_zy = rotated_corners.max(axis=0)
    
    if y_original_size is not None :
        out_z = int(np.ceil(((y_original_size - 1) * dy_um * abs(np.sin(theta))) / dz_um))
    else:
        out_z =int(np.ceil(max_zy[0] - min_zy[0] + 1))
    out_y = int(np.ceil(max_zy[1] - min_zy[1] + 1))
    out_x = x_size
    
    output_shape = (out_z, out_y, out_x)
    
    # ---------------------------------------------------------
    # 3) Build the forward affine transform in absolute coordinates
    # ---------------------------------------------------------
    
    # center of output box in its own index space
    center_out = np.array([(out_z - 1) / 2.0, (out_y - 1) / 2.0, (out_x - 1) / 2.0], dtype=np.float64)
    center_in = np.array([(z_size - 1) / 2.0, (y_size - 1) / 2.0, (x_size - 1) / 2.0], dtype=np.float64)
    
    offset = center_in - forward_3d  @ center_out
    
    rotated = ndimage.affine_transform(
        volume,
        matrix=forward_3d ,
        offset=offset,
        output_shape=output_shape,
        order=order,
        mode="constant",
        cval=cval,
        prefilter=(order > 1)
    )

    return rotated

def deskew_and_rotate_opm(
        volume: np.ndarray,
        dy_um: float,
        aspect_ratio : float,
        theta_deg: float,
        order: int = 1) -> np.ndarray:
    """
    Full OPM pipeline:
    1) integer deskew (Y shear),
    2) anisotropy-aware rotation around X.

    Parameters
    ----------
    volume : np.ndarray
        Input volume of shape (Z, Y, X).
    dy_um : float
        Pixel size along Y in micrometers.
    dz_um : float
        Plane spacing along Z in micrometers.
    aspect_ratio : float
        ratio between dy and dz in the image
    theta_deg : float
        Rotation angle in degrees.
    order : int, optional
        Interpolation order.
    cval : float, optional
        Constant fill value outside boundaries.

    Returns
    -------
    np.ndarray
        Deskewed and rotated volume.
    """
    
    _, size_y, _ = volume.shape
    
    
    dz_um = dy_um * aspect_ratio
    
    shift_y_px_per_plane = _px_shift_calculation(aspect_ratio, theta_deg, angle_unit = "deg")
    
    sheared = _shear_integer_y(volume, shift_y_px_per_plane)

    rotated = rotate_about_x_physical(
        sheared,
        dy_um=dy_um,
        dz_um=dz_um,
        theta_deg=theta_deg,
        order=order, cval=0.0,
        y_original_size = size_y)
    
    return rotated

###############################################################################
if __name__ == '__main__':
    from pathlib import Path
    import os
    import tifffile
    
    dy_um = 0.155
    theta = 40
    aspect_ratio = 3.3564

    folder = Path(r"D:\Projets_Python\OPM_GUI\Images\20260313_TestLS_Grid\20260313_115359_Billes_170nm_LS3_300um")
    filename = "Position_0000_GFP_file_"
    
    for k in range(4):
        file_path = os.path.join(folder, f'{filename}{k:04d}.tif')
        if k == 0 :
            volume_zyx = tifffile.imread(file_path)
        else:
            volume_zyx = np.concatenate((volume_zyx, tifffile.imread(file_path)))
            
        print(f'\rImage {k:04d} / 36 oppened', end = " ")
            
    # filename = "GFP_volume_0000"
    # file_path = os.path.join(folder, f'{filename}.tif')
    # volume_zyx = tifffile.imread(file_path)
    
    # volume_zyx = tifffile.imread(file_path)
    print("Images oppened")
    
    for k in range(2):
        volume_zyx_deskew = volume_zyx[:, :, k*256:(k+1)*256]

        if k == 0 :
            out_volume = deskew_and_rotate_opm(volume_zyx_deskew, dy_um, aspect_ratio, theta)
        else:
            out_volume = np.concat((out_volume, deskew_and_rotate_opm(volume_zyx_deskew, dy_um, aspect_ratio, theta)),axis=2)
        
        print(f"image deskewed_rotated : {k}/7")
        
    output_file_path = f'{folder}/dekew-rotate_{filename}total.tif'
    tifffile.imwrite(output_file_path, out_volume, bigtiff=True, compression='zlib')
    print("image saved")