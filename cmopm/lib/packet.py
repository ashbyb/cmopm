# -*- coding: utf_8 -*-

'''
@created: April 24 2014
@author: Student, Kit, Sye
@summary: Packet parsing classes
@copyright: Copyright 2014 Siye/Sye/Student - All Rights Reserved.
'''

# Standard Imports
import logging
import time
import sys
import os
import datetime
from string import Template
import struct
from binascii import hexlify
import math

# Attach logger
log = logging.getLogger(__name__)

# Import gui for colors
from PyQt4.QtGui import QColor, QBrush

# Import core for emits, qt for color defaults
from PyQt4.QtCore import SIGNAL, Qt, QObject

# Dependancies
try:
    import requests
except ImportError:
    log.critical("Missing Python Requests Library. Google for it.")
    sys.exit(1)

# More Dependencies
import pydivert
from pydivert.windivert import WinDivert, Handle

# Import Exceptions
from cmopm.lib.exception import InterpreterArchitectureMisMatch, RequireElevatedPrivileges, TargetServerIPNotSet

# Import Decryption Logic
from cmopm.lib.decrypt import TCP


class PacketSniffer(QObject):
    ''' A class to sniff packets and alter them '''
    interface = None
    countPacketsCaptured = 0
    _filter="ip and (ip.DstAddr == %s or ip.SrcAddr == %s)"
    dropOutbound = False
    dropInbound = False

    def __init__(self, parent, server_ip=None, dll=None, running=True, priority=1000):
        ''' consructor, set variables '''
        super(PacketSniffer, self).__init__(parent)

        # Store reference to parent for emiting
        self.parent = parent

        # Store server IP determined earlier
        self.server_ip = server_ip

        # Build dll path
        if dll is None:
            if is_python_64bit() and is_windows_64bit():
                version = "amd64"
            elif not is_python_64bit() and not is_windows_64bit():
                version = "x86"
            else:
                raise InterpreterArchitectureMisMatch
            self.dll = os.path.abspath(os.path.join("assets","libs","WinDivert",version,"WinDivert.dll")).replace('\\','\\\\')
        else:
            self.dll = dll

        # Executing Flag
        self.running = running

        # Listen Packet Priority
        self.priority = priority

        # Build sniffer object
        self.interface = WinDivert(self.dll)

        # Build Packet Decryption Class
        self.tcp = TCP(self)

        # Build our session for http requests we make
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'CMO3D', 'Accept': 'application/text'}) # TODO: Compare to what is actually being sent in Wireshark

    def stop(self):
        ''' Stop Execution '''
        self.running = False

    def register(self):
        ''' register pyDivert with the system '''

        if self.interface is not None and is_elevated_priv():
            self.interface.register()
        else:
            raise RequireElevatedPrivileges

    def isRegistered(self):
        ''' Bool. Is our sniffer properly registered '''

        if self.interface is not None:
            return self.interface.is_registered()
        else:
            return False

    def listen(self):
        ''' Core listen loop. Listen on interface for packets '''

        # Listen Packet Filter
        if self.server_ip is not None:
            self.filter = self._filter % (self.server_ip, self.server_ip)
        else:
            raise TargetServerIPNotSet

        if self.interface is not None and self.isRegistered():
            with Handle(self.interface, filter=self.filter, priority=self.priority, flags=1024) as handle:
                while self.running:

                    # Read in Packet
                    packet = handle.receive()

                    # Note the new packet
                    self.countPacketsCaptured += 1

                    # Parse Packet Payload (data)
                    payload = hexlify(packet.payload)

                    # Log IP headers
                    log.debug("[Packet]{}:{}:{}".format(packet.dst_addr, packet.dst_port, payload))

                    # Determine flow direction
                    self.outbound = False
                    if packet.meta.is_outbound():
                        self.outbound = True
                    
                    # Decode Packet, emit
                    if len(payload) is not 0:
                        self.tcp.checkPacket(payload)

                    # Send Packet on its way, if allowed
                    if self.outbound and not self.dropOutbound:
                        handle.send(packet)
                    elif not self.outbound and not self.dropInbound:
                        handle.send(packet)

                    
                handle.close()


class DeltaTemplate(Template):
    ''' Thanks to: http://stackoverflow.com/questions/8906926/formatting-python-timedelta-objects '''
    delimiter = "%"

def strfdelta(tdelta, fmt):
    ''' Thanks to: http://stackoverflow.com/questions/8906926/formatting-python-timedelta-objects '''
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    # Quick edit to 0 pad
    if d["H"] < 10:
    	d["H"] = "0%s" % d["H"]
    if d["M"] < 10:
    	d["M"] = "0%s" % d["M"]
    if d["S"] < 10:
    	d["S"] = "0%s" % d["S"]
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


class DictDiffer(object):
    """ Thanks to: http://stackoverflow.com/questions/1165352/fast-comparison-between-two-python-dictionary """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

def is_python_64bit():
    # Thanks to phobie: http://stackoverflow.com/questions/2208828/detect-64bit-os-windows-in-python
    return (struct.calcsize("P") == 8)

def is_windows_64bit():
    if 'PROCESSOR_ARCHITEW6432' in os.environ:
        return True
    return os.environ['PROCESSOR_ARCHITECTURE'].endswith('64')

def is_elevated_priv():
    # Thanks: http://stackoverflow.com/questions/1026431/cross-platform-way-to-check-admin-rights-in-a-python-script-under-windows
    import ctypes, os

    is_admin = False # Assume a failure state
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin
