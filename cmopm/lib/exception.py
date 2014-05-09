# -*- coding: utf_8 -*-

'''
Created on April 24, 2013

@author: Siye/Sye/Student
@copyright: Copyright 2013 Siye/Sye/Student - All Rights Reserved.
@summary: Holds class definitions for exceptions
'''


class GenericError(Exception):
    """ Base class for exceptions. """
    pass

class ResponseStatusCodeError(GenericError):
    """Exception raised for errors of a bad http request response code."""

    def __init__(self, code):
        self.code = code
    def __str__(self):
        return repr(self.code)

class InterpreterArchitectureMisMatch(GenericError):
    ''' Thrown when the python interpreter mismatches the system archtecture '''
    pass

class RequireElevatedPrivileges(GenericError):
	''' Thrown when the program needs elevated privileges (root on unix, and admin on windows) but does not currently have it (or failed to determine it) '''
	pass

class TargetServerIPNotSet(GenericError):
    ''' Thrown when a sniffer is being created but has not been told which server IP to filter against '''
    pass
