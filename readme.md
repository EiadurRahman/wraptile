# Wraptile

Wraptile is a powerful graphical user interface for PyInstaller that simplifies the process of converting Python scripts into standalone executable files. This tool provides a user-friendly interface to access PyInstaller's extensive options without having to remember command-line arguments.

<img src = assets/ui.png width=500>

## Table of Contents

- [Wraptile](#wraptile)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
  - [Detailed Interface Guide](#detailed-interface-guide)
    - [Main Settings Tab](#main-settings-tab)
      - [Script Selection](#script-selection)
      - [Output Settings](#output-settings)
      - [Icon Settings](#icon-settings)
      - [Console Settings](#console-settings)
      - [Distribution Format](#distribution-format)
    - [Advanced Settings Tab](#advanced-settings-tab)
      - [Advanced PyInstaller Options](#advanced-pyinstaller-options)
      - [Additional Data Files](#additional-data-files)
      - [Additional PyInstaller Arguments](#additional-pyinstaller-arguments)
    - [Output Log Tab](#output-log-tab)
  - [Building Your Executable](#building-your-executable)
  - [Common Issues](#common-issues)
    - [Multiple Qt Bindings Error](#multiple-qt-bindings-error)
    - [Missing Modules](#missing-modules)
    - [File Not Found Errors](#file-not-found-errors)
    - [Anti-Virus Detection](#anti-virus-detection)
    - [UPX Compression Issues](#upx-compression-issues)
  - [Requirements](#requirements)
  - [Contributing](#contributing)

## Features

- Modern, intuitive PyQt5-based interface
- Support for all essential PyInstaller options
- Real-time build output monitoring
- Background processing to keep UI responsive
- Comprehensive error handling
- Customizable executable properties
- Support for data files, icons, and other resources

## Installation

1. Ensure you have Python 3.6+ installed
2. Install required dependencies:

```bash
pip install PyQt5 pyinstaller
```

3. Download `wraptile.py` and run it:

```bash
python wraptile.py
```

## Quick Start

1. Launch Wraptile
2. In the Main Settings tab, click "Browse..." to select your Python script
3. Adjust basic settings as needed (output directory, executable name, etc.)
4. Click the "Compile" button
5. Monitor progress in the Output Log tab
6. Once complete, find your executable in the specified output directory

## Detailed Interface Guide

Wraptile's interface is divided into three main tabs:

### Main Settings Tab

This tab contains the most commonly used options for building your executable:

#### Script Selection
- **Python Script**: Path to the Python (.py) file you want to convert to an executable
- **Browse...**: Opens a file dialog to select your Python script

#### Output Settings
- **Output Directory**: Where your executable will be saved
  - Leave blank to use PyInstaller's default 'dist' folder in your project directory
  - Click "Browse..." to select a custom location
- **Executable Name**: Name for your executable file (without .exe extension)
  - Automatically populated with your script name, but can be customized

#### Icon Settings
- **Icon File (.ico)**: Path to an icon file (.ico) to use for your executable
- **Browse...**: Opens a file dialog to select your icon file

#### Console Settings
- **Show Console Window**: Creates an executable that shows the console window when running (default)
- **Hide Console Window**: Creates an executable that hides the console window (for GUI applications)

#### Distribution Format
- **Create a single executable file (--onefile)**: Packages everything into a single .exe file
  - When unchecked, creates a folder with the executable and supporting files

### Advanced Settings Tab

This tab contains additional options for more specific customization:

#### Advanced PyInstaller Options
- **Clean before build (--clean)**: Removes temporary files before building
- **Use UPX compression (if installed)**: Compresses the executable using UPX to reduce size
- **Strip symbols from executable (--strip)**: Reduces size by removing debugging symbols
- **Disable UPX (--noupx)**: Explicitly disables UPX compression
- **Request UAC elevation (--uac-admin)**: Makes the program request administrator privileges on Windows

#### Additional Data Files
- Text area for specifying data files to include with your executable
- Format: `source_path;destination_path`
- Example: `images/*.png;images/` will include all PNG files from an images folder

#### Additional PyInstaller Arguments
- Text field for any custom PyInstaller command line arguments
- For advanced users who need options not covered by the interface

### Output Log Tab

This tab shows real-time output from the PyInstaller process:

- Displays the full command being executed
- Shows all build progress messages
- Highlights errors or warnings
- Indicates build success or failure
- Shows the final executable location

## Building Your Executable

1. **Configure Settings**: Fill in all necessary fields in the Main and Advanced tabs
2. **Click Compile**: This will start the build process
3. **Monitor Progress**: The interface will automatically switch to the Output Log tab
4. **Wait for Completion**: The build process may take several minutes depending on your script
5. **Check Results**: A success message will appear when the build is complete

After successful compilation, you'll find your executable in the specified output directory or in the default `dist` folder of your project.

## Common Issues

### Multiple Qt Bindings Error
If you see an error like:
```
Aborting build process due to attempt to collect multiple Qt bindings packages: attempting to run hook for 'PyQt6', while hook for 'PyQt5' has already been run!
```

This happens when PyInstaller detects both PyQt5 and PyQt6 in your environment. Solutions:

1. **Exclude the unused Qt binding**:
   - Add `--exclude PyQt6` or `--exclude PyQt5` in the Additional PyInstaller Arguments field
   - Use whichever exclusion keeps the Qt version your application actually uses

2. **Create a virtual environment**:
   - Set up a clean virtual environment with only the required Qt binding
   - Install only the necessary packages to avoid conflicts

3. **Check implicit dependencies**:
   - Some packages might pull in Qt bindings as dependencies
   - Use `pip list` to identify all installed packages
   - Look for packages that might be importing the unwanted Qt version

### Missing Modules
If your executable fails with "ModuleNotFoundError", you may need to explicitly include hidden imports:
- Add `--hidden-import module_name` in the Additional PyInstaller Arguments field

### File Not Found Errors
If your application cannot find data files:
- Make sure to add them correctly in the Additional Data Files section
- Use relative paths in your code to access these files

### Anti-Virus Detection
Some antivirus software may flag PyInstaller executables as suspicious:
- This is a common false positive due to how PyInstaller works
- Consider adding exceptions in your antivirus software
- Use code signing if distributing commercially

### UPX Compression Issues
If you encounter problems with UPX compression:
- Try disabling UPX by checking the "Disable UPX" option
- Or install UPX and ensure it's in your system PATH

## Requirements

- Python 3.6 or higher
- PyQt5
- PyInstaller

## Contributing

Wraptile is an open project, and contributions are welcome! If you encounter bugs or have feature suggestions, please submit them through the issue tracker.