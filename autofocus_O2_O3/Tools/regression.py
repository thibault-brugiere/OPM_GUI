# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:24:21 2026

@author: tbrugiere
"""

import matplotlib.pyplot as plt
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

    try :
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
    
        return y_fit, r_squared, x_max, y_max, parameters
    except :
        return 0,0,0,0,None

def plot_gaussian_fit(x, y, r_squared, x_max, y_max, parameters, show):
    """
    Plot experimental points and fitted Gaussian curve.

    Parameters
    ----------
    x : array_like
        X coordinates used for the fit.
    y : array_like
        Experimental values used for the fit.
    r_squared : float
        Coefficient of determination R².
    x_max : float
        X position of the fitted Gaussian maximum.
    y_max : float
        Y value of the fitted Gaussian maximum.
    parameters : array_like
        Gaussian parameters: amplitude, center, sigma and offset.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    # Dense X axis for a smooth fitted curve
    x_fit = np.linspace(np.min(x), np.max(x), 500)
    y_fit = gaussian(x_fit, *parameters)

    plt.figure(figsize=(6, 6))

    plt.scatter(x, y, label="Data")
    plt.plot(x_fit, y_fit, label=f"Gaussian fit ($R^2$ = {r_squared:.4f})")
    plt.scatter(x_max, y_max, marker="x", s=100, label=f"Maximum ({x_max:.6f}, {y_max:.0f})")

    plt.xlabel("X")
    plt.ylabel("Intensity")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    if show :
        plt.show()
        
    # return plt.gcf()

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    x_fit = np.linspace(np.min(x), np.max(x), 500)
    y_fit = gaussian(x_fit, *parameters)

    fig, ax = plt.subplots(figsize=(8, 5))

    # Background
    fig.patch.set_facecolor("#303030")
    ax.set_facecolor("#303030")

    # Experimental points
    ax.scatter(
        x,
        y,
        s=55,
        color="#ED7D31",
        edgecolors="none",
        zorder=3,
        label="Measurements"
    )

    # Gaussian fit
    ax.plot(
        x_fit,
        y_fit,
        color="#5B9BD5",
        linewidth=2.5,
        label=f"Gaussian fit  R² = {r_squared:.3f}"
    )

    # Maximum
    ax.scatter(
        x_max,
        y_max,
        s=80,
        color="#FFC000",
        edgecolors="none",
        zorder=4,
        label=f"Maximum = {x_max:.4f}"
    )

    # Labels
    ax.set_xlabel("Piezo position", color="white")
    ax.set_ylabel("Intensity", color="white")

    # Ticks
    ax.tick_params(
        axis="both",
        colors="#D9D9D9",
        length=0
    )

    # Grid
    ax.grid(
        axis="y",
        color="#666666",
        linewidth=0.8,
        alpha=0.5
    )

    # Remove unnecessary borders
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["left"].set_color("#A0A0A0")
    ax.spines["bottom"].set_color("#A0A0A0")

    # Legend
    legend = ax.legend(
        frameon=False,
        fontsize=9
    )

    for text in legend.get_texts():
        text.set_color("#D9D9D9")

    fig.tight_layout()

    return fig

    # if show :
    #     plt.show()
        
    # return plt.gcf()
    
def create_black_graph():
    """
    Create an empty black Matplotlib figure.

    Returns
    -------
    matplotlib.figure.Figure
        Empty black figure.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    fig.patch.set_facecolor("#303030")
    ax.set_facecolor("#303030")

    ax.axis("off")

    return fig