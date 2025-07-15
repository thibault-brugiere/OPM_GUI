# -*- coding: utf-8 -*-
import os
from datetime import datetime

def prepare_saving_directory(base_path, exp_name):
    """
    Create a unique saving directory with timestamp for the given experiment.

    Parameters:
    - base_path: str
        Root folder where experiment directories will be created.
    - exp_name: str
        Name of the experiment (used in the folder name).

    Returns:
    - full_path: str
        Full path to the created directory.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{timestamp}_{exp_name}"
    full_path = os.path.join(base_path, folder_name)
    os.makedirs(full_path, exist_ok=True)
    return full_path

def save_metadata(config, save_path):
    """
    Save experiment metadata to a log.txt file in the saving directory.

    Parameters:
    - config: object
        The configuration object loaded from MDA_config, containing cameras,
        channels, experiment and microscope attributes.
    - save_path: str
        Path to the directory where log.txt will be written.
    """
    log_file = os.path.join(save_path, "log.txt")
    with open(log_file, "w") as f:
        f.write("Experiment Metadata Log\n")
        f.write("=======================\n")
        f.write(f"Experiment Name: {config.experiment.exp_name}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Save Path: {save_path}\n")
        f.write(f"Number of Channels: {len(config.channels)}\n")
        f.write("Channel Names: " + ", ".join([ch.channel_id for ch in config.channels]) + "\n")
        f.write(f"Number of Cameras: {len(config.cameras)}\n")
        f.write(f"Z Slices (n_steps): {config.experiment.n_steps}\n")
        f.write(f"Timepoints: {config.experiment.timepoints}\n")
        f.write(f"Scan Range: {config.experiment.scan_range:.2f} µm\n")
        f.write(f"Step Size: {config.experiment.step_size:.3f} µm\n")
        f.write(f"Slit Aperture: {config.experiment.slit_aperture}\n")
        f.write("\n")
        f.write("# Additional metadata can be added below:\n")
        f.write("\n")
        
def add_acquisition_stats(stats, save_path):
    log_file = os.path.join(save_path, "log.txt")
    with open(log_file, "w") as f:
        try:
            with open(log_file, "a") as f:
                f.write("\n=== Acquisition Summary ===\n")
                f.write(f"Total frames acquired : {stats['total_frames']}\n")
                f.write(f"Total frames dropped  : {stats['total_dropped']}\n")
                f.write(f"Total volumes saved   : {stats['total_volumes']}\n")
                f.write(f"Elapsed time (s)      : {stats['elapsed']}\n")
                if stats["elapsed"] > 0:
                    f.write(f"Effective FPS         : {stats['FPS']}\n")
                    f.write(f"Volume rate (Hz)      : {stats['Hz']}\n")
                f.write("============================\n")
        except Exception as e:
            print(f"[WARNING] Could not write final stats to log.txt: {e}")