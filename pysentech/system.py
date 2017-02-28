# -*- coding: utf-8 -*-
"""
Created on Mon Dec 07 21:55:57 2015

@author: derricw
"""

from ctypes import *

from .sentechdll import SentechDLL
from .camera import SentechCamera


class SentechSystem(object):
    """ System object.  Used to count and access connected cameras.

    Example
    -------
    >>> system = SentechSystem("sentech/sdk/folder")
    >>> camera = system.get_camera(0)
    """
    def __init__(self, sdk_folder=""):
        self.dll = SentechDLL(sdk_folder)
        
    def camera_count(self):
        """ Gets the number of connected cameras.

        returns:
            int: number of connected cameras
        """
        return self.dll.StCam_CameraCount(None)
        
    def get_camera(self, index):
        """ Gets the camera at the specified index.

        args:
            index (int): camera index
        """
        return SentechCamera(index, self.dll)
        
if __name__ == "__main__":
    sdk_folder = r"C:\Users\derricw\Downloads\StandardSDK(v3.08)\StandardSDK(v3.08)"
    system = SentechSystem(sdk_folder)
    print("Cameras: {}".format(system.camera_count()))
    cam = system.get_camera(0)