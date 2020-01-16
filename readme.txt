INSTALLATION
============
1. Download and install python interpreter using following url:
https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe

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
blue|2|Blue;1.0

This line means that output image will contain 2 prints of `images/blue.png` with 2 lines of text.

dpi for output image is set to 300.
