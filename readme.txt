INSTALLATION
============
1. Download and install python interpreter using following url:
https://www.python.org/ftp/python/2.7/python-2.7.msi

2. Install python requirements by running `install_deps.bat` file.
To run this file simple double-click on it in windows explorer.


USAGE
=====
You need to double-click on `run.bat` to generate resulting image.
Resulting image will be displayed on screen and saved to `output.png` file.


Configuration
=============
Configuration is stored in `config.txt` file.
It has following format: filename_without_extension|number_of_prints|text_separated_by_semicolon

For example:
blue|2|Blue;sky;1.0

This line means that output image will contain 2 prints of `images/blue.png` with 3 lines of text.

Default dpi for output image is set to 300. You can change dpi to 150 by opening `main.py` file
and changing line:
DPI = 300
to line:
DPI = 150
