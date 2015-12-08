# -*- coding: utf-8 -*-
"""
Created on Mon Dec 07 22:08:13 2015

@author: derricw
"""
import traceback
import ctypes
from ctypes import *
malloc = ctypes.cdll.msvcrt.malloc  #windows

import numpy as np
import matplotlib.pyplot as plt

from senpy import SentechDLL


# load the dll
dot_h_file = r"C:\Users\derricw\Downloads\StandardSDK(v3.08)\StandardSDK(v3.08)\include\StCamD.h"
dll = SentechDLL(dot_h_file)

# check for cameras
cameras_available = dll.StCam_CameraCount(None)
print("Cameras found: {}".format(cameras_available))

if cameras_available < 1:
    raise Exception("No cameras found.")

# Open a camera
camera = dll.StCam_Open(0)

if camera > 0:
    print("Camera open! Handle: {}".format(camera))
else:
    raise Exception("Failed to initialize camera!")

try:
    # Get image size
    cwidth = c_ulong()
    cheight = c_ulong()
    creserved = c_ulong()
    cscanmode = c_ushort()
    coffsetx = c_ulong()
    coffsety = c_ulong()
    
    dll.StCam_GetImageSize(camera, byref(creserved), byref(cscanmode),
                           byref(coffsetx), byref(coffsety), byref(cwidth),
                           byref(cheight))
    
    width, height = cwidth.value, cheight.value
    print("Camera image shape: {}x{}".format(width, height))
    
    # Get pixel format
    cpixformat = c_ulong()
    dll.StCam_GetPreviewPixelFormat(camera, byref(cpixformat))
    pixformat = cpixformat.value
    print("Camera pixel format: {}".format(pixformat))
    
    # Get bits per pixel
    cbpp = c_ulong()
    dll.StCam_GetTransferBitsPerPixel(camera, byref(cbpp))
    bpp = cbpp.value
    print("Camera bits per pixel: {}".format(bpp))
    
    # Get bytes per image
    cbpi = c_ulong()
    clinepitch = c_ulong()
    dll.StCam_GetPreviewDataSize(camera, byref(cbpi), byref(cwidth),
                                 byref(cheight), byref(clinepitch))
    bpi = cbpi.value
    print("Camera bytes per image: {}".format(bpi))
    
    # Allocate memory
    imgpointer = malloc(bpi)
    imgdata = cast(imgpointer, POINTER(c_byte))
    
    # Transfer image from camera
    cbytesxferred = c_ulong()
    cframeno = c_ulong()
    cmillisecs = c_ulong(1000)
    ret = dll.StCam_TakePreviewSnapShot(camera, imgdata, bpi,
                                        byref(cbytesxferred), byref(cframeno),
                                        cmillisecs)
    if not ret:
        print("Failed to transfer image from camera.")

    # Make image array
    array = (c_ubyte * int(height*bpi) *
             int(width*bpi)).from_address(addressof(imgdata.contents))
             
    # Convert image array to numpy so we can use it in pythonland
    npimg = np.ndarray(buffer=array, dtype=np.uint8, shape=(height, width))
    
    # Show using matplotlib
    plt.imshow(npimg, cmap='gray')
    plt.show()
    
except Exception:
    traceback.print_exc()

# Close the camera
dll.StCam_Close(camera)