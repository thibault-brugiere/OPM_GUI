# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 09:20:04 2026

@author: tbrugiere

functions used to deskew and rotate images acquired using the OPM
These functions use the GPU of the computer and does the operation in one step
but there is a DEGRADATION OF IMAGE QUALITY
This program should be run with the environnement OPM_gpu that contains the library
cupyx
"""
import numpy as np
import cupy as cp
import cupyx.scipy.ndimage as cpx_ndimage

def shear_rotate_about_x_physical(
    volume: np.ndarray,
    shift_y_px_per_plane: int,
    dy_um: float,
    dz_um: float,
    theta_deg: float,
    order: int = 1,
    cval: float = 0.0,
    return_numpy: bool = True,
    gpu_id: int = 0,
):
    """
    Apply an implicit integer shear along Y followed by a physical rotation
    around X (i.e. in the ZY plane), using a single affine resampling step.

    The shear is not materialized as an intermediate zero-padded array.
    This function consume less memory (perfect for giant volumes), but there is a
    DEGRADATION OF IMAGE QUALITY

    Parameters
    ----------
    volume : np.ndarray or cp.ndarray
        Input volume of shape (Z, Y, X).
    shift_y_px_per_plane : int
        Integer shear along Y per Z plane:
            y_sheared = y + z * shift_y_px_per_plane
    dy_um : float
        Pixel size along Y in micrometers.
    dz_um : float
        Plane spacing along Z in micrometers.
    theta_deg : float
        Rotation angle in degrees.
    order : int, optional
        Interpolation order for affine_transform.
    cval : float, optional
        Fill value outside the input volume.
    return_numpy : bool, optional
        If True, return a NumPy array. Otherwise return a CuPy array.
    gpu_id : int, optional
        GPU device ID.

    Returns
    -------
    np.ndarray or cp.ndarray
        Output rotated volume with tight canvas.
    """
    if volume.ndim != 3:
        raise ValueError("Expected a 3D array with shape (Z, Y, X).")
    if dy_um <= 0:
        raise ValueError("dy_um must be > 0.")
    if dz_um <= 0:
        raise ValueError("dz_um must be > 0.")
    if order not in (0, 1, 2, 3, 4, 5):
        raise ValueError("order must be an integer between 0 and 5.")

    with cp.cuda.Device(gpu_id):
        volume_gpu = cp.asarray(volume)
        z_size, y_size, x_size = volume_gpu.shape

        # --------------------------------------------------------------
        # 1) Inverse rotation in index coordinates (for affine_transform)
        # --------------------------------------------------------------
        theta = np.deg2rad(-theta_deg)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)

        scale_zy = np.array(
            [[dz_um, 0.0],
             [0.0, dy_um]],
            dtype=np.float64,
        )

        rotate_zy = np.array(
            [[cos_theta, -sin_theta],
             [sin_theta,  cos_theta]],
            dtype=np.float64,
        )

        # output -> sheared
        rot_inv_zy = np.linalg.inv(scale_zy) @ rotate_zy @ scale_zy

        # --------------------------------------------------------------
        # 2) Inverse shear: sheared -> source
        # --------------------------------------------------------------
        s = float(shift_y_px_per_plane)
        shear_inv_zy = np.array(
            [[1.0,  0.0],
             [-s,   1.0]],
            dtype=np.float64,
        )

        # --------------------------------------------------------------
        # 3) Full inverse mapping: output -> source
        # --------------------------------------------------------------
        combined_inv_zy = shear_inv_zy @ rot_inv_zy

        combined_inv_3d = np.eye(3, dtype=np.float64)
        combined_inv_3d[0:2, 0:2] = combined_inv_zy

        # --------------------------------------------------------------
        # 4) Compute tight output canvas from forward transform
        #    source -> output = inverse(combined_inv_zy)
        # --------------------------------------------------------------
        combined_fwd_zy = np.linalg.inv(combined_inv_zy)

        center_in_zy = np.array(
            [(z_size - 1) / 2.0, (y_size - 1) / 2.0],
            dtype=np.float64,
        )

        corners_zy = np.array(
            [[0.0,          0.0],
             [0.0,          y_size - 1.0],
             [z_size - 1.0, 0.0],
             [z_size - 1.0, y_size - 1.0]],
            dtype=np.float64,
        )

        centered_corners_zy = corners_zy - center_in_zy[None, :]
        out_corners_zy = centered_corners_zy @ combined_fwd_zy.T

        min_zy = out_corners_zy.min(axis=0)
        max_zy = out_corners_zy.max(axis=0)

        out_z = int(np.ceil(max_zy[0] - min_zy[0] + 1.0))
        out_y = int(np.ceil(max_zy[1] - min_zy[1] + 1.0))
        out_x = x_size
        output_shape = (out_z, out_y, out_x)

        # --------------------------------------------------------------
        # 5) Centered affine mapping for scipy/cupy affine_transform
        # --------------------------------------------------------------
        center_out = np.array(
            [(out_z - 1) / 2.0, (out_y - 1) / 2.0, (out_x - 1) / 2.0],
            dtype=np.float64,
        )

        center_in = np.array(
            [(z_size - 1) / 2.0, (y_size - 1) / 2.0, (x_size - 1) / 2.0],
            dtype=np.float64,
        )

        offset = center_in - combined_inv_3d @ center_out

        out_gpu = cpx_ndimage.affine_transform(
            volume_gpu,
            matrix=cp.asarray(combined_inv_3d),
            offset=cp.asarray(offset),
            output_shape=output_shape,
            order=order,
            mode="constant",
            cval=cval,
            prefilter=(order > 1),
        )

        if return_numpy:
            return cp.asnumpy(out_gpu)
        return out_gpu
    
###############################################################################
if __name__ == '__main__':
    from pathlib import Path
    import os
    import tifffile
    
    dy_um = 0.155
    theta = 40
    aspect_ratio = 3.3564
    shift = 4

    folder = Path(r"C:\Users\tbrugiere\Documents\Images_OPM\20260330_154402_Image")
    
    file_list = []
    
    for index in range(13):
        filename = f'Position_0000_GFP_file_{index:04d}.tif'
        file_path = os.path.join(folder, filename)
        file_list.append(tifffile.imread(file_path))
        print(f'charged : {index} / 12')
        
    volume_zyx = np.concatenate(file_list)
    
    del file_list

    print("Image oppened")
    
    volume_zyx_cp = cp.asarray(volume_zyx)
    
    del volume_zyx
    
    out_volume = shear_rotate_about_x_physical(volume_zyx_cp ,
                                               shift,
                                               dy_um,
                                               dy_um * aspect_ratio,
                                               theta
                                               )

    output_file_path = f'{folder}/test_dekew-rotate_{filename}.tif'
    tifffile.imwrite(output_file_path, out_volume, bigtiff=True)
    print(f"""image {filename} saved
          """)