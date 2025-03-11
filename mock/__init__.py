"""
Mock Module
============

This module provides mock implementations of hardware components, allowing the application
interface to function even when the actual hardware is not connected. It is particularly 
useful for development, testing, and demonstration purposes, ensuring that the application
can run seamlessly without physical devices.

Module Contents:

- hamamatsu.py:
  Contains mock functions for emulating the behavior of Hamamatsu cameras. This file includes methods to
  simulate camera initialization, configuration, and image acquisition.
  It generates dynamic gradient images to mimic real camera output, enabling interface testing
  and development without a physical camera connected.

- DAQ.py:
  Provides mock functions for emulating Data Acquisition (DAQ) devices. This file includes
  methods that ignore commands sent to the DAQ, allowing the application to proceed as if the DAQ hardware
  were present. It is useful for testing and developing DAQ-related features without requiring actual DAQ devices.

"""