# -*- coding: utf-8 -*-
"""
Created on Wed Dec 09 00:58:13 2015

@author: derricw
"""

#TODO: Get error messages from StCamMsg.dll

class SentechError(Exception):
    def __init__(self, cam_handle, dll):
        code = dll.StCam_GetLastError(cam_handle)
        message = "error code {}".format(code)
        super(SentechError, self).__init__(message)