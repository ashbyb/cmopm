# -*- coding: utf_8 -*-

'''
Created on April 24, 2013

@author: Siye/Sye/Student
@copyright: Copyright 2013 Siye/Sye/Student - All Rights Reserved.
@summary: Holds class definitions for threads
'''

# Import python libs
import logging
import Queue
import time
import os
import sys
import re

# Build logging ref
log = logging.getLogger(__name__)

# Import Core Qt modules
from PyQt4 import QtCore, QtGui

# Import the timer class
from cmopm.lib.packet import PacketSniffer

# Import Exceptions
from cmopm.lib.exception import ResponseStatusCodeError, TargetServerIPNotSet

# Dependancies
try:
    import requests
except ImportError:
    print "Missing Python Requests Library. Google for it."
    sys.exit(1)

# Handle SSL issue concerning building to exe via PyInstaller. See: https://github.com/kennethreitz/requests/issues/557
# Adpated from <http://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile>
def resource_path(relative):
    return os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")), relative)
# SSL Cert
_SSL_CERT_PATH = resource_path('cacert.pem')


class CMOPMThread(QtCore.QThread):
    defaultFilter = "tcp.addr == x"
    sniffer = None

    def __init__(self, parent, ident, server_ip=None, running=True, failureThreshold=0):
        super(CMOPMThread, self).__init__(parent)
        self.parent = parent
        self.id = ident
        self.server_ip = server_ip
        self.running = running
        self.failureThreshold = failureThreshold

    def stop(self):
        self.running = False

    def run(self):

        failures = 0

        while self.running:
            try:
                self._run()
            except:
                failures += 1
                if failures > self.failureThreshold:
                    log.exception("Thread killed by errors!")
                    self.emit(QtCore.SIGNAL("pingThreadFailure"))
                    self.running = False
                else:
                    self.emit(QtCore.SIGNAL("pingThreadPartialFailure"), failures, self.failureThreshold)
                    time.sleep(1)
            else:
                self.running = False

        # Thread is dying
        self.emit(QtCore.SIGNAL("pingThreadDeath"))
        log.debug("CMOPMThread stopping")

    def _run(self):
        ''' Main function of thread. '''

        # Alert Sniffing Start
        self.emit(QtCore.SIGNAL("startSniffing"))

        try:            
            # Begin Sniffing
            self.sniffer.listen() # TODO: Raise an actual error here is not registered
        except TargetServerIPNotSet:
            log.exception("Target IP not provided")
            raise
        except Exception as e:
            log.exception("[CMOPM Thread] Sniffer.listen() saw exception")
            self.emit(QtCore.SIGNAL("CMOPMThreadUnhandledException"), e)
            raise

    def register(self):
        ''' Register sniffer for sniffing '''
  
        # Build our packet sniffer
        self.sniffer = PacketSniffer(self) # TODO: Raise an actual error here is not registered

        # Register with system
        self.sniffer.register()

    def validSnifferRef(self):
        ''' Return a reference to a working valid sniffer '''

        if self.sniffer is not None and self.sniffer.isRegistered():
            return self.sniffer
        else:
            return None


class CMOServerRequestThread(QtCore.QThread):
    apiEndpoint = "http://t.kisscmo.jp/public/sys/server.txt"

    def __init__(self, parent, ident, running=True, failureThreshold=5):
        super(CMOServerRequestThread, self).__init__(parent)
        self.parent = parent
        self.id = ident
        self.running = running
        self.failureThreshold = failureThreshold

        # Build our session
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36', 'Accept': 'application/txt'})

    def stop(self):
        self.running = False

    def run(self):

        failures = 0

        while self.running:
            try:
                self._run()
            except:
                failures += 1
                if failures > self.failureThreshold:
                    log.exception("Thread killed by errors!")
                    self.emit(QtCore.SIGNAL("pingThreadFailure"))
                    self.running = False
                else:
                    self.emit(QtCore.SIGNAL("pingThreadPartialFailure"), failures, self.failureThreshold)
                    time.sleep(1)
            else:
                self.running = False

        # Thread is dying
        self.emit(QtCore.SIGNAL("pingThreadDeath"))
        log.debug("CMOServerRequestThread stopping")
    def _run(self):
        ''' Main function of thread. '''

        try:
            # Query the end point for the data we need
            r = self.session.get(self.apiEndpoint)
            if r.status_code is 200:
                #print r.text
                ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', r.text )
            else:
                raise ResponseStatusCodeError(r.status_code)
        except Exception:
            log.exception("[CMOServerRequest Thread] session.get() saw exception")
            raise
        else:
            self.emit(QtCore.SIGNAL("ServerIPPingThreadSuccess"), ip)

# Class that handles giving threads IDs (PyQt does not implement this natively)
class threadIdSpooler(QtCore.QObject):
    def __init__(self, parent):
        super(threadIdSpooler, self).__init__(parent)
        self.curID = 0
        self.pool = Queue.Queue()

    def requestID(self):
        if self.pool.empty():
            self.curID += 1
            return self.curID - 1
        else:
            return self.pool.get_nowait()

    def returnID(self):
        returningID = self.sender().id
        self.pool.put_nowait(returningID)

class threadManager(QtCore.QObject):
    children = dict()
    def __init__(self, parent):
        super(threadManager, self).__init__(parent)
        self.parent = parent

    def adopt(self, thread):
        ''' threadManager adopts thread '''

        try:
            _id = thread.id
            if _id is None:
                raise AttributeError
        except AttributeError:
            log.exception("Thread was supplied with no id")
            raise ThreadMissingID
        else:
            if _id not in self.children.keys() or self.children[_id] is None:
                # Set if not set
                log.debug("Manager adopts thread #%d" % _id)
                self.children[_id] = thread
            elif self.children[_id] != thread:
                # Overwrite current thread
                log.debug("Manager adopts thread #%d. Overwrites thread #%d" % (_id, self.children[_id].id))
                self.children[_id] = thread
            else:
                # Already adopted this thread.
                log.debug("Can not adopt thread #%d, already adopted." % _id)

    def release(self, _id):
        ''' threadManager stops managing thread with id _id '''

        try:
            del self.children[_id]
        except KeyError:
            # Catch, note, but don't raise
            log.debug("treadManager was told to release thread #%d but didn't have that thread to release." % _id)

    def getThread(self, _id=None, thread=None):
        ''' returns a reference to a thread that is being managed if possible, else None. Can look against _ids or thread objects '''

        pass
        # TODO: What am I trying to do here?


