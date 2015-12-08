# -*- coding: utf-8 -*-
"""
Created on Mon Dec 07 21:55:57 2015

@author: derricw
"""

from sentechdll import SentechDLL
from camera import SentechCamera


class SentechSystem(object):
    
    def __init__(self, header_file):
        self.dll = SentechDLL(header_file)
        
    def camera_count(self):
        return self.dll.StCam_CameraCount(None)
        
    def get_camera(self, index):
        return 
        
if __name__ == "__main__":
    dot_h_file = r"C:\Users\derricw\Downloads\StandardSDK(v3.08)\StandardSDK(v3.08)\include\StCamD.h"
    system = SentechSystem(dot_h_file)
    print("Cameras: {}".format(system.camera_count()))