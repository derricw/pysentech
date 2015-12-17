# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 00:58:13 2015

@author: derricw
"""

#TODO: Get error messages from StCamMsg.dll

class SentechError(Exception):
    def __init__(self, message, code=None):
        message = "{} -> error code {}".format(message, code)
        super(SenpyError, self).__init__(message)