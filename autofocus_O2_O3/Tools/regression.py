# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:24:21 2026

@author: tbrugiere
"""

import numpy as np
from scipy.optimize import curve_fit


def gaussian(x, amplitude, center, sigma, offset):
    """
    Gaussian function with constant offset.

    Parameters
    ----------
    x : np.ndarray
        X coordinates.
    amplitude : float
        Gaussian amplitude.
    center : float
        Gaussian center.
    sigma : float
        Gaussian standard deviation.
    offset : float
        Constant background.

    Returns
    -------
    np.ndarray
        Gaussian values.
    """
    return offset + amplitude * np.exp(
        -0.5 * ((x - center) / sigma) ** 2
    )


def gaussian_fit(x, y):
    """
    Fit a Gaussian function to x/y data.

    Parameters
    ----------
    x : array_like
        X coordinates.
    y : array_like
        Y values.

    Returns
    -------
    y_fit : np.ndarray
        Gaussian fitted values evaluated at x.
    r_squared : float
        Coefficient of determination R².
    x_max : float
        X position of the Gaussian maximum.
    y_max : float
        Y value of the Gaussian maximum.

    Raises
    ------
    ValueError
        If x and y have different sizes or contain too few valid points.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if x.size != y.size:
        raise ValueError("x and y must have the same size.")

    valid = np.isfinite(x) & np.isfinite(y)
    x = x[valid]
    y = y[valid]

    if x.size < 4:
        raise ValueError("At least 4 valid points are required.")

    # Initial estimates
    offset_0 = np.min(y)
    amplitude_0 = np.max(y) - offset_0
    center_0 = x[np.argmax(y)]
    sigma_0 = (np.max(x) - np.min(x)) / 4

    parameters, _ = curve_fit(
        gaussian,
        x,
        y,
        p0=[amplitude_0, center_0, sigma_0, offset_0],
        bounds=(
            [0, np.min(x), 0, -np.inf],
            [np.inf, np.max(x), np.inf, np.inf],
        ),
    )

    amplitude, center, sigma, offset = parameters

    y_fit = gaussian(x, *parameters)

    residual_sum = np.sum((y - y_fit) ** 2)
    total_sum = np.sum((y - np.mean(y)) ** 2)

    r_squared = 1 - residual_sum / total_sum

    x_max = center
    y_max = offset + amplitude

    return y_fit, r_squared, x_max, y_max