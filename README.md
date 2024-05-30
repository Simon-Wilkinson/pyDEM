# PyDEM

## Overview
PyDEM is a project designed to demonstrate how to build a Python interface to a Discrete Element Modelling (DEM) simulation written in C++.

## Requirements
- CMake
- Visual Studio
- Python 3.8 or higher

## Installation Instructions

1. **Configure Setup Script:**
   - Open `setup.bat` in a text editor.
   - Replace the `MSBuild.exe` path on line 20 with the path to your local Visual Studio installation.
   - Save the changes.

2. **Run Setup Script:**
   - Execute `setup.bat` by double-clicking it or running it from the command prompt.

This will:
1. Clone pybind11 into the `dependencies` directory.
2. Build the C++ project with CMake.
3. Create a virtual environment in the `/py` directory and install the necessary dependencies.
4. Copy the C++ module into the virtual environment.

## Running a Simulation
To run a simulation, execute `main.py` using the Python interpreter from the virtual environment. Feel free to edit the simulation configuration in main.py.
