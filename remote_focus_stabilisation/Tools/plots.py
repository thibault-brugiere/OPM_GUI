# -*- coding: utf-8 -*-
"""
Created on Fri May 29 11:05:53 2026

@author: tbrugiere
"""

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PySide6.QtGui import QImage

def create_stabilisation_plot(
    displacement,
    corrections,
    w_px=800,
    h_px=300,
    dpi=100,
    max_points=50,
    line_width=2,
    font_size=10,
):
    """
    Create a QImage showing the latest stabilisation data.

    Parameters
    ----------
    displacement : list[float]
        Measured displacement values.
    corrections : list[float]
        Applied correction values.
    w_px : int, optional
        Output image width in pixels.
    h_px : int, optional
        Output image height in pixels.
    dpi : int, optional
        Matplotlib figure DPI.
    max_points : int, optional
        Maximum number of latest points to display.
    line_width : float, optional
        Width of the displacement line.
    font_size : int, optional
        Axis font size.

    Returns
    -------
    QImage
        Rendered stabilisation plot as a Qt image.

    Raises
    ------
    ValueError
        If ``displacement`` and ``corrections`` do not have the same length.
    """
    if len(displacement) != len(corrections):
        raise ValueError(
            "'displacement' and 'corrections' must have the same length."
        )

    displacement_arr = np.asarray(
        displacement[-max_points:],
        dtype=float,
    )
    corrections_arr = np.asarray(
        corrections[-max_points:],
        dtype=float,
    )

    n = len(displacement_arr)
    x = np.arange(n)

    fig = plt.Figure(
        figsize=(w_px / dpi, h_px / dpi),
        dpi=dpi,
    )
    canvas = FigureCanvas(fig)

    # Displacement axis
    ax1 = fig.add_subplot(111)

    ax1.plot(
        x,
        displacement_arr,
        color="blue",
        linewidth=line_width,
        marker="o",
    )

    ax1.set_ylabel(
        "Displacement",
        fontsize=font_size,
        color="blue",
    )
    ax1.tick_params(
        axis="y",
        labelcolor="blue",
        labelsize=font_size,
    )
    ax1.tick_params(
        axis="x",
        labelsize=font_size,
    )

    if n:
        ymin = min(displacement_arr.min(), 0.0)
        ymax = max(displacement_arr.max(), 0.0)

        margin = 0.05 * max(abs(ymin), abs(ymax), 1.0)
        ax1.set_ylim(ymin - margin, ymax + margin)

    # Correction axis
    ax2 = ax1.twinx()

    ax2.bar(
        x,
        corrections_arr,
        color="red",
        alpha=0.35,
    )

    ax2.set_ylabel(
        "Correction",
        fontsize=font_size,
        color="red",
    )
    ax2.tick_params(
        axis="y",
        labelcolor="red",
        labelsize=font_size,
    )

    if n:
        correction_limit = max(
            np.max(np.abs(corrections_arr)),
            1.0,
        )
        margin = 0.1 * correction_limit

        ax2.set_ylim(
            -correction_limit - margin,
            correction_limit + margin,
        )

    ax2.grid(
        True,
        axis="y",
        alpha=0.25,
    )

    ax1.set_xlabel(
        "Last values",
        fontsize=font_size,
    )
    ax1.set_xlim(
        -0.5,
        max(n - 0.5, 0.5),
    )
    ax1.grid(
        True,
        axis="x",
        alpha=0.25,
    )

    fig.tight_layout()

    canvas.draw()
    w, h = canvas.get_width_height()

    image_data = np.asarray(
        canvas.buffer_rgba(),
        dtype=np.uint8,
    ).reshape(h, w, 4)

    return QImage(
        image_data.data,
        w,
        h,
        w * 4,
        QImage.Format_RGBA8888,
    ).copy()