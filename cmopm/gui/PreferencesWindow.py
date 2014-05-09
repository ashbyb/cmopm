'''
Created on April 24, 2014

@author: student
'''

# Import Qt modules
from PyQt4 import QtCore, QtGui

#Import .ui to .py generated layout
from cmopm.gui.generated.PreferencesWindow_generated import Ui_Dialog_Preferences

class Dialog_Preferences(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)

        # Create our account window
        self.preferences = Ui_Dialog_Preferences()
        self.preferences.setupUi(self)
