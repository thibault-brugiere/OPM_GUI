"""
Configuration Module
=====================

This module contains the configuration settings and variables for the application's
interface and system components. It includes settings for the camera, channels, experiment,
and microscope.

Module Contents:

- config.py:
  Contains the main configuration variables and settings for the application.
  This file defines default parameters for the camera, channels, experiment setup,
  and microscope configuration.

It also store in non-volatile settings in JSON and plk format

- saved_variables.json:
  Stores on-volatile settings in JSON JSON format (preset_size)

- channels_data.plk:
  Stores non-volatile channel configuration settings in a pickle file.
  This file maintains the state and settings of various default channels used in the application,
  ensuring that channel configurations are retained across sessions.

"""