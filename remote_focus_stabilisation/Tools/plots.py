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
    float_values,
    step_values,
    w_px=800,
    h_px=300,
    dpi=100,
    max_points=50,
    line_width=2,
    font_size=10,
):
    """
    Create a QImage showing the last stabilisation values.

    Parameters
    ----------
    float_values : list[float]
        Continuous values, for example measured drift.
    step_values : list[int]
        Integer correction steps, typically between -5 and 5.
    w_px : int, optional
        Output image width in pixels.
    h_px : int, optional
        Output image height in pixels.
    dpi : int, optional
        Matplotlib figure DPI.
    max_points : int, optional
        Number of last points to display.
    line_width : float, optional
        Width of the plotted line.
    font_size : int, optional
        Axis font size.

    Returns
    -------
    QImage
        Rendered plot as a Qt image.
    """

    float_arr = np.asarray(float_values[-max_points:], dtype=float)
    step_arr = np.asarray(step_values[-max_points:], dtype=int)

    n = min(len(float_arr), len(step_arr))
    float_arr = float_arr[-n:]
    step_arr = step_arr[-n:]

    fig = plt.Figure(figsize=(w_px / dpi, h_px / dpi), dpi=dpi)
    canvas = FigureCanvas(fig)

    ax1 = fig.add_subplot(111)
    x = np.arange(n)

    ax1.plot(x, float_arr, color="blue", linewidth=line_width, marker="o")
    ax1.set_ylabel("Value", fontsize=font_size, color="blue")
    ax1.tick_params(axis="y", labelcolor="blue", labelsize=font_size)
    ax1.tick_params(axis="x", labelsize=font_size)
    
    if n > 0:
        ymin = min(np.min(float_arr), 0)
        ymax = max(np.max(float_arr), 0)
    
        margin = 0.05 * max(abs(ymin), abs(ymax), 1)
        ax1.set_ylim(ymin - margin, ymax + margin)

    ax2 = ax1.twinx()
    ax2.bar(x, step_arr, color="red", alpha=0.35)
    ax2.set_ylabel("Steps", fontsize=font_size, color="red")
    ax2.tick_params(axis="y", labelcolor="red", labelsize=font_size)
    ax2.set_ylim(-5.5, 5.5)
    ax2.set_yticks(np.arange(-5, 6, 5))
    ax2.grid(True, axis="y", alpha=0.25)

    ax1.set_xlabel("Last values", fontsize=font_size)
    ax1.set_xlim(-0.5, max(n - 0.5, 0.5))
    ax1.grid(True, alpha=0.25)

    fig.tight_layout()

    canvas.draw()
    w, h = canvas.get_width_height()

    image_data = np.asarray(canvas.buffer_rgba(), dtype=np.uint8).reshape(h, w, 4)

    qimage = QImage(
        image_data.data,
        w,
        h,
        w * 4,
        QImage.Format_RGBA8888,
    ).copy()

    return qimage