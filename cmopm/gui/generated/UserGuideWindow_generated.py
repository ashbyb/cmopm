# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\ui\UserGuideWindow_v1.ui'
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

class Ui_Dialog_Userguide(object):
    def setupUi(self, Dialog_Userguide):
        Dialog_Userguide.setObjectName(_fromUtf8("Dialog_Userguide"))
        Dialog_Userguide.resize(200, 97)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/images/icons/toolkit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog_Userguide.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog_Userguide)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog_Userguide)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)

        self.retranslateUi(Dialog_Userguide)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Userguide)

    def retranslateUi(self, Dialog_Userguide):
        Dialog_Userguide.setWindowTitle(_translate("Dialog_Userguide", "Userguide - CMOPM", None))
        self.label.setText(_translate("Dialog_Userguide", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Userguide Window</span></p><p align=\"center\">- to be developed -</p></body></html>", None))

import resources_rc
