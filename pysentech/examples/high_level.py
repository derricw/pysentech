# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 22:10:26 2016

@author: derricw

high_level.py

Example for high level camera API.

Demonstrates how to:

1) Initialize SentechSystem
2) Open a camera
3) Read camera properties
4) Set some camera properties
5) Grab a frame
6) Save a frame to a file
7) Release the camera

"""
from pysentech import SentechSystem

# initialize SentechSystem
sdk_folder = r"C:\Users\derricw\Downloads\StandardSDK(v3.08)\StandardSDK(v3.08)"
system = SentechSystem(sdk_folder)
#system = SentechSystem()  # or this, if you have set SENTECHPATH env variable
print("Cameras: {}".format(system.camera_count()))

# open a camera
cam = system.get_camera(0)

# get some camera into
print("Camera model: {}".format(cam.model))
print("Driver version: {}".format(cam.driver_version))

# get some image properties
print("Image size: {} bytes".format(cam.image_size))
print("Image pixel format: {}".format(cam.pixel_format))
print("Image shape: {}".format(cam.image_shape))
print("Image gain: {}".format(cam.gain))
print("Max image shape: {}".format(cam.max_image_shape))

# set some image properties
cam.image_height = 1040
cam.gain = 2

# grab a frame
frame = cam.grab_frame()

# save it to a file
img_path = "test_img.png"
frame.to_file(img_path)
print("Frame saved to '{}'".format(img_path))

# release camera
cam.release()
print("Camera released!")