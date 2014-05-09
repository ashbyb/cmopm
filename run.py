#!/usr/bin/env python
# -*- coding: utf_8 -*-

'''
@created: April 22 2014
@author: Student, Kit, Sye
@summary: a system to intecept, decrypt, and manipulate the CMO client
@copyright: Personal Copyright 2014 - All Rights Reserved
'''

pass

if __name__ == "__main__":
    # Standard Imports
    import sys

    # Import Core Qt modules
    from PyQt4.QtGui import QApplication

    # Import the main window for execution
    from cmopm.gui.MainWindow import CMOPMMainWindow

    # Start up main PyQT Application loop
    app = QApplication(sys.argv)

    # Build and show main window
    window = CMOPMMainWindow()
    
    # Show Main Window
    window.show()

    # Exit program when our window is closed.
    sys.exit(app.exec_())
