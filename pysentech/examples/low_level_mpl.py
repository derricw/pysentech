# -*- coding: utf-8 -*-
"""
Created on Mon Dec 07 22:08:13 2015

@author: derricw

Demonstrates use of the Sentech DLL using ctypes.

1) Loads the header file and dll.
2) Checks for available cameras.
3) Gets a camera handle.
4) Gets image properties from the camera.
5) Sets up a buffer for the image.
6) Copies the cameras current image to the buffer.
7) Casts the buffer to an ndarray.
8) Displays the ndarray using matplotlib.

"""
import traceback
import ctypes
from ctypes import *
malloc = ctypes.cdll.msvcrt.malloc  #windows

import numpy as np
import matplotlib.pyplot as plt

from pysentech import SentechDLL


# load the dll
sdk_folder = r"C:\Users\derricw\Downloads\StandardSDK(v3.08)\StandardSDK(v3.08)"
dll = SentechDLL(sdk_folder)
#dll = SentechDLL()  # or this, if you have set SENTECHPATH env variable
print("DLL loaded!")

# check for cameras
cameras_available = dll.StCam_CameraCount(None)
print("Cameras found: {}".format(cameras_available))

if cameras_available < 1:
    raise Exception("No cameras found.")

# Open a camera
camera = dll.StCam_Open(0)
handle_id = camera.contents.value

if handle_id > 0:
    print("Camera open! Handle: {}".format(handle_id))
else:
    raise Exception("Failed to initialize camera!")

try:
    # Get image shape
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
    
    # Set pixel format so that the rest of this example works properly
    pixformat = dll.STCAM_PIXEL_FORMAT_08_MONO_OR_RAW
    ret = dll.StCam_SetPreviewPixelFormat(camera, pixformat)
    if not ret:
        print("Failed to set pixel format!")
    
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
    dll.StCam_GetRawDataSize(camera, byref(cbpi))
    bpi = cbpi.value
    print("Camera bytes per image: {}".format(bpi))
    
    # Allocate memory for image
    imgdata = cast(create_string_buffer(bpi), POINTER(c_byte))
    
    # Transfer image from camera
    cbytesxferred = c_ulong()
    cframeno = c_ulong()
    cmillisecs = c_ulong(1000)
    ret = dll.StCam_TakeRawSnapShot(camera, imgdata, bpi,
                                    byref(cbytesxferred), byref(cframeno),
                                    cmillisecs)
    if not ret:
        print("Failed to transfer image from camera.")

    # Make image array
    array = (c_ubyte * int(height*bpi) *
             int(width*bpi)).from_address(addressof(imgdata.contents))
             
    # Convert image array to numpy so we can display it easily
    npimg = np.ndarray(buffer=array, dtype=np.uint8, shape=(height, width))
    
    # Show using matplotlib
    plt.imshow(npimg, cmap='gray')
    plt.show()
    
except Exception:
    traceback.print_exc()

# Close the camera
dll.StCam_Close(camera)