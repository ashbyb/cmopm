#!/usr/bin/env python
# -*- coding: utf_8 -*-

'''
@created: April 27 2014
@author: ashbyb
@summary: Run the test suite for pyDivert
'''

# Standard Lib Imports
import os

# Dependency Imports
from pydivert import tests
from pydivert.windivert import WinDivert

def testPyDivert():
	''' Run the test suite for pyDivert '''

	tests.run_test_suites()

def testRegister():
	''' Attempt to register WinDivert '''

	dll_path3 = r"c:\Python276\lib\site-packages\pydivert-0.0.2-py2.7.egg\lib\1.1\amd64\WinDivert.dll"
	driver_path = r"c:\Python276\lib\site-packages\pydivert-0.0.2-py2.7.egg\lib\1.1\amd64"
	
	os.chdir(driver_path)

	handle = WinDivert(dll_path3)
	print "HANDLE:", handle
	handle.register()
	print "REGISTERED:", handle.is_registered()

if __name__ == "__main__":
	# Test Time!
	testPyDivert()
	#testRegister()