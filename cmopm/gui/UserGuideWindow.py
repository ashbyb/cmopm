'''
Created on May 8, 2014

@author: student
'''

# Import Qt modules
from PyQt4 import QtCore, QtGui

#Import .ui to .py generated layout
from cmopm.gui.generated.UserGuideWindow_generated import Ui_Dialog_Userguide

class Dialog_Userguide(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)

        # Create our account window
        self.userguide = Ui_Dialog_Userguide()
        self.userguide.setupUi(self)
