'''
Created on April 24, 2014

@author: student
'''

# Import Qt modules
from PyQt4 import QtCore, QtGui

# Import .ui to .py generated layout
from cmopm.gui.generated.AboutWindow_generated import Ui_Dialog_about

class Dialog_About(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)

        # Create our account window
        self.about = Ui_Dialog_about()
        self.about.setupUi(self)
