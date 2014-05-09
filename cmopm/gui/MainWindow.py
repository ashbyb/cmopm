#!/usr/bin/env python
# -*- coding: utf_8 -*-

'''
@created: April 22 2014
@author: Student, Kit, Sye
@summary: a system to intecept, decrypt, and manipulate the CMO client
@copyright: Personal Copyright 2014 - All Rights Reserved
'''

# Standard Imports
import sys
import logging
import argparse
import datetime

# Attach logger
log = logging.getLogger(__name__)

# Import Core Qt modules
from PyQt4 import QtCore, QtGui

# Import the compiled UI module for main
from cmopm.gui.generated.MainWindow_generated import Ui_MainWindow

# Import Classes for child dialogs
from UserGuideWindow import Dialog_Userguide
from AboutWindow import Dialog_About
from PreferencesWindow import Dialog_Preferences

# Import threading library
from cmopm.lib.threading import threadIdSpooler, CMOServerRequestThread, CMOPMThread

# Import Exceptions
from cmopm.lib.exception import InterpreterArchitectureMisMatch, RequireElevatedPrivileges


class CMOPMMainWindow(QtGui.QMainWindow):
    ''' Implements PyQt GUI MainWindow. A GUI class to play with packets '''

    def __init__(self):
        ''' constructor, build window, assign a timer to a server '''
        QtGui.QMainWindow.__init__(self, None) # No parent

        # Create the main window class layout
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create child window classes
        self.userguide = Dialog_Userguide(self)
        self.about = Dialog_About(self)
        self.preferences = Dialog_Preferences(self)

        # Create class to maintain / distribute unique thread IDs
        self.threadIdSpooler = threadIdSpooler(self)

        # Set Default sorting
        # TODO: Default column widths
        self.ui.treeWidget_log.sortItems(7, 1)

        # Bind mouse move to hover event
        QtCore.QObject.connect(self.ui.treeWidget_log, QtCore.SIGNAL("mouseMoveEvent()"), self.handleTreeWidgetMouseMoveEvent)

        # Log startup
        log.debug("Starting")

    def handleTreeWidgetMouseMoveEvent(self, event):
        ''' Hover event '''

        print "Test"

    @QtCore.pyqtSignature("")
    def on_actionUser_Guide_triggered(self,):
        ''' SLOT. Called when we select the user guide menu option '''

        self.userguide.exec_()  # Blocking window

    @QtCore.pyqtSignature("")
    def on_actionPreferences_triggered(self):
        ''' SLOT. Called when we select the preferences menu option '''

        self.preferences.exec_()  # Blocking window

    @QtCore.pyqtSignature("")
    def on_actionAbout_triggered(self):
        ''' SLOT. Called when we select the about menu option '''

        self.about.exec_()  # Blocking window

    @QtCore.pyqtSignature("")
    def on_pushButton_find_server_clicked(self):
        ''' SLOT. Called when we click find server ip button '''

        # Lock UI elements
        self.ui.pushButton_find_server.setEnabled(False)
        self.ui.label_server_ip.setText("Querying...")

        # Spawn thread
        self.aCMOServerRequestThread = CMOServerRequestThread(self, self.threadIdSpooler.requestID())
        QtCore.QObject.connect(self.aCMOServerRequestThread, QtCore.SIGNAL("finished()"), self.threadIdSpooler.returnID)
        QtCore.QObject.connect(self.aCMOServerRequestThread, QtCore.SIGNAL("finished()"), self.handleServerIPPingThreadFinished)
        QtCore.QObject.connect(self.aCMOServerRequestThread, QtCore.SIGNAL("pingThreadPartialFailure"), self.handleServerIPPingThreadPartialFailure)
        QtCore.QObject.connect(self.aCMOServerRequestThread, QtCore.SIGNAL("pingThreadFailure"), self.handleServerIPPingThreadFailure)
        QtCore.QObject.connect(self.aCMOServerRequestThread, QtCore.SIGNAL("ServerIPPingThreadSuccess"), self.handleServerIPPingThreadSuccess)
        self.aCMOServerRequestThread.start()

    def handleServerIPPingThreadFinished(self):
        ''' SLOT. Called when the thread finishes '''

        self.ui.pushButton_find_server.setEnabled(True)

    def handleServerIPPingThreadPartialFailure(self, attempt, max_attempts):
        ''' SLOT. Clled when the thread failed on a request '''

        self.ui.label_server_ip.setText("Attempt %d of %d." % (attempt, max_attempts))

    def handleServerIPPingThreadFailure(self):
        ''' SLOT. Called when a thread has failed and will die '''

        self.ui.label_server_ip.setText("Request failed! Try Again?")

    def handleServerIPPingThreadSuccess(self, ip):
        ''' SLOT. Called when the thread found a server IP '''

        self.server_ip = str(ip[0])
        self.ui.label_server_ip.setText("Server is %s" % self.server_ip)
        self.ui.groupBox_step_2.setEnabled(False)
        self.ui.groupBox_step_3.setEnabled(True)

    @QtCore.pyqtSignature("")
    def on_pushButton_register_clicked(self):
        ''' SLOT. Called when we click register packet driver button '''

        # Lock UI elements
        self.ui.pushButton_register.setEnabled(False)
        self.ui.label_register.setText("Registering...")

        # Spawn thread
        self.aCMOPMThread = CMOPMThread(self, self.threadIdSpooler.requestID())
        
        # Attempt to register the driver
        success = False
        try:
            self.aCMOPMThread.register()
        except InterpreterArchitectureMisMatch:
            log.exception("System architecture does not match python interpreter architecture. Must match to be able to register the WinDivert .dll")
            QtGui.QMessageBox.critical(self, 'Notice | Architecture Mismatch', "This executable and Windows' architecture don't match!\nRun 64bit if Windows is 64bit, else 32bit.", QtGui.QMessageBox.Ok)
        except RequireElevatedPrivileges:
            log.exception("Need elevated privileges to be able to install WinDivert .dll")
            QtGui.QMessageBox.critical(self, 'Notice | Elevated Privileges', "This program needs elevated privileges to manipulate packets (not surprisingly).\nRun as Administrator.", QtGui.QMessageBox.Ok)
        except Exception:
            log.exception("Unhandled Error Seen.")
        else:
            success = True
        finally:
            # Clean up on failure
            if not success:
                self.aCMOPMThread = None
                self.ui.label_register.setText("Failed to Register! Try Again?")
                self.ui.pushButton_register.setEnabled(True)
            else:
                self.ui.label_register.setText("Driver Registered")
                self.ui.groupBox_step_1.setEnabled(False)
                self.ui.groupBox_step_2.setEnabled(True)

    @QtCore.pyqtSignature("")
    def on_pushButton_execute_clicked(self):
        ''' SLOT. Called when we click packet filtering execute button '''

        # Lock UI elements
        self.ui.pushButton_execute.setEnabled(False)
        self.ui.label_sniff_status.setText("Sniffing...")

        # Bind emits from thread
        QtCore.QObject.connect(self.aCMOPMThread, QtCore.SIGNAL("finished()"), self.threadIdSpooler.returnID)
        QtCore.QObject.connect(self.aCMOPMThread, QtCore.SIGNAL("finished()"), self.handleCMOPMThreadFinished)
        QtCore.QObject.connect(self.aCMOPMThread, QtCore.SIGNAL("pingThreadPartialFailure"), self.handleCMOPMThreadPartialFailure)
        QtCore.QObject.connect(self.aCMOPMThread, QtCore.SIGNAL("pingThreadFailure"), self.handleCMOPMThreadFailure)
        QtCore.QObject.connect(self.aCMOPMThread, QtCore.SIGNAL("startSniffing"), self.handleStartSniffing)
        QtCore.QObject.connect(self.aCMOPMThread, QtCore.SIGNAL("CMOPMThreadUnhandledException"), self.handleCMOPMThreadUnhandledException)
        
        # Connect to Sniffer emits
        QtCore.QObject.connect(self.aCMOPMThread.validSnifferRef(), QtCore.SIGNAL("PacketMsg"), self.handleSnifferPacketMsg)
        QtCore.QObject.connect(self.aCMOPMThread.validSnifferRef(), QtCore.SIGNAL("changeXOR32SEED"), self.handlechangeXOR32SEEDMsg)

        # Set sniffer target server IP
        self.aCMOPMThread.validSnifferRef().server_ip = self.server_ip

        # Begin Filtering
        self.aCMOPMThread.running = True
        self.aCMOPMThread.start()

    def handleCMOPMThreadUnhandledException(self, exception):
        ''' SLOT. Called when the CMOPM thread comes to an unhandled exception during sniffing '''

        QtGui.QMessageBox.critical(self, 'Notice | Unhandled Exception', "Sniffing Thread encountered an unhandled exception and died.\nCheck the logs for more information.\nIf this issue persists, ask for help.\nError: %s" % exception, QtGui.QMessageBox.Ok)

    def handleCMOPMThreadFinished(self):
        ''' SLOT. Called when the thread finishes '''

        self.ui.pushButton_execute.setEnabled(True)
        self.ui.stackedWidget.setCurrentIndex(0)

    def handleCMOPMThreadPartialFailure(self, attempt, max_attempts):
        ''' SLOT. Called when the thread partially fails '''

        self.ui.label_sniff_status.setText("Attempt %d of %d." % (attempt, max_attempts))

    def handleCMOPMThreadFailure(self):
        ''' SLOT. Called when the thread dies from failures '''

        self.ui.label_sniff_status.setText("Sniffer has died due to error")

    def handleStartSniffing(self):
        ''' SLOT. Called when the sniffer is good to go and starts sniffing '''

        self.ui.stackedWidget.setCurrentIndex(1)

    def handlechangeXOR32SEEDMsg(self, seed):
        ''' SLOT. Called when the XOR32 Encryption Seed changes '''

        self.ui.label_xor32_seed.setText("XOR32 Seed: %d" % seed)

    def handleSnifferPacketMsg(self, cmd, comment, decoded, com1, com2, com3, payload_len, payload, outbound, count):
        ''' SLOT. Called when the sniffer sniffs a packet worth mentioning '''

        # Update UI Count Stat
        self.ui.label_packets_captured.setText("Packets Captured: %d" % count)

        if outbound:
            color = QtGui.QColor(QtCore.Qt.green)
            packet_source = "Client"
        else:
            color = QtGui.QColor(QtCore.Qt.blue)
            packet_source = "Server"
        color.setAlpha(80)

        # Build text then push item to target widget with text
        text = QtCore.QStringList()
        text.append(packet_source)
        text.append(str(cmd))
        text.append(str(com1))
        text.append(str(com2))
        text.append(str(com3))
        text.append(decoded)
        text.append("%d bytes" % payload_len)
        text.append(datetime.datetime.utcnow().strftime("%H:%M:%S.%f"))
        item = QtGui.QTreeWidgetItem(self.ui.treeWidget_log, text)

        # Style item   
        item.setBackground(0, QtGui.QBrush(color))
        item.setToolTip(6, payload)
        item.setToolTip(1, comment)

    def closeEvent(self, event):
        '''
        This event is thrown when a close event is created (File>Exit or clicking the 'X' symbol in the window manager)
        A simple "Are you sure" dialog is presented. If 'no' the event is ignored.
        '''

        if QtGui.QMessageBox.question(self, 'Confirm', "Are you sure you want to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

