=========
Changelog
=========

Version 0.7
===========

**Date:** TBD

New Features
------------

- Linux: Utility for creating a system launcher
- Sending usage statistics with user consent
- Reading .CR3 Canon Raw files
- Introduction of profiles (default settings for assisted visual or photo)
- Addition of a QR code display leading to the integrated web server
- Addition of jpeg, png, and tiff file reading
- French translation
- Dark frame subtraction
- Hot pixel removal
- Night mode

Improvements
------------

- Windows: ALS version is provided as a proper installer
- Improved autostretch
- Improved zoom with default settings reset and keyboard shortcuts
- Saving logs in the user's home folder
- Option to display only issues in the session log
- Ability to manually override the Bayer pattern used for debayering
- User-defined minimum number of matches for alignment
- Writing web content to a specific folder
- Critical session information moved to the status bar for constant visibility
- Toggleable night mode

Bug Fixes
---------

- Windows: Failed to write images to paths containing non-ASCII characters
- Support for FITS files with .fts extension
- RPI: Crash when saving black and white images

Version 0.6.1
=============

**Date:** November 18, 2019

Bug Fixes
---------

- Defective debayering of images taken with cameras having a CFA GBRG pattern

Version 0.6
===========

**Date:** November 14, 2019

New Features
------------

- User settings dialog
- Pan and zoom in the image with mouse clicks and wheel
- Two auto-brightness adjustment methods to choose from
- Histogram display
- RGB color balance

Improvements
------------

- Image server port is configurable
- Image server page auto-refreshes with a configurable time period
- Remembering window size and position
- Configurable image file save type
- Log window, session controls, and image processing controls can be hidden
- Fullscreen mode
- Much more responsive graphical interface

Bug Fixes
---------

- Crash if new images are written to a slow storage device
- Image served by the web server is too bright
- Crash if the new image cannot be aligned with the current stack
- Crash if a new session is started when the scan folder is missing

Version 0.5
===========

**Date:** July 10, 2019

New Features
------------

- Stacked image can be served by the new integrated web server

Version 0.4
===========

**Date:** June 22, 2019

New Features
------------

- New stacked image processor: Wavelets

Version 0.3
===========

**Date:** May 23, 2019

New Features
------------

- Support for common DSLR raw files
- Folder scanner can be paused
- Image processing controls reset button
- New stacked image processor: SCNR

Version 0.2
===========

**Date:** May 21, 2019

New Features
------------

- Contrast and brightness of stacked images can be adjusted

Version 0.1
===========

**Date:** May 18, 2019

Initial Release
---------------

- Alignment and stacking of FITS files
