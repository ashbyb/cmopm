# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\ui\AboutWindow_v1.ui'
#
# Created: Fri May 09 01:25:28 2014
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog_about(object):
    def setupUi(self, Dialog_about):
        Dialog_about.setObjectName(_fromUtf8("Dialog_about"))
        Dialog_about.resize(307, 321)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/images/icons/toolkit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog_about.setWindowIcon(icon)
        Dialog_about.setSizeGripEnabled(False)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog_about)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(4, 0, 4, 4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(Dialog_about)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_logo = QtGui.QLabel(self.frame)
        self.label_logo.setText(_fromUtf8(""))
        self.label_logo.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/hatsune-miku.gif")))
        self.label_logo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_logo.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_logo.setObjectName(_fromUtf8("label_logo"))
        self.horizontalLayout.addWidget(self.label_logo)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_logo_2 = QtGui.QLabel(self.frame)
        self.label_logo_2.setText(_fromUtf8(""))
        self.label_logo_2.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/images/megurine-luka1.gif")))
        self.label_logo_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_logo_2.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_logo_2.setObjectName(_fromUtf8("label_logo_2"))
        self.horizontalLayout.addWidget(self.label_logo_2)
        self.verticalLayout.addWidget(self.frame)
        self.line = QtGui.QFrame(Dialog_about)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.label_details = QtGui.QLabel(Dialog_about)
        self.label_details.setAlignment(QtCore.Qt.AlignCenter)
        self.label_details.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_details.setObjectName(_fromUtf8("label_details"))
        self.verticalLayout.addWidget(self.label_details)
        self.line_2 = QtGui.QFrame(Dialog_about)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.pushButton_close = QtGui.QPushButton(Dialog_about)
        self.pushButton_close.setObjectName(_fromUtf8("pushButton_close"))
        self.verticalLayout.addWidget(self.pushButton_close)

        self.retranslateUi(Dialog_about)
        QtCore.QObject.connect(self.pushButton_close, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog_about.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog_about)

    def retranslateUi(self, Dialog_about):
        Dialog_about.setWindowTitle(_translate("Dialog_about", "About | CMO: PM", None))
        self.label.setText(_translate("Dialog_about", "<html><head/><body><p align=\"center\">CMO: Packet Manipulator</p></body></html>", None))
        self.label_details.setText(_translate("Dialog_about", "<html><head/><body><p align=\"center\">A tool to &quot;<span style=\" font-style:italic; color:#ff0004;\">play</span>&quot; with the packet flow of <span style=\" font-weight:600;\">Custom Maid Online</span></p><p align=\"center\">Remember kids;<span style=\" font-style:italic;\"> Security through Obscurity</span>!</p><p align=\"center\">Built with love using:</p><p align=\"center\">Python 2.7.x</p><p align=\"center\">PyQT4</p><p align=\"center\">WinDivert &gt; pyDivert</p><p align=\"center\">pyInstaller</p></body></html>", None))
        self.pushButton_close.setText(_translate("Dialog_about", "Close", None))

import resources_rc
