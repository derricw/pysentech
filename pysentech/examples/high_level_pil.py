# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 23:14:06 2016

@author: derricw

high_level_pil.py

Example for high level camera API using PIL

Demonstrates how to:

1) Initialize SentechSystem
2) Open a camera
3) Read camera properties
4) Set some camera properties
5) Grab a frame
6) Get a PIL image from frame and show it
7) Release the camera

"""
from pysentech import SentechSystem

# initialize SentechSystem
dot_h_file = r"C:\Users\derricw\Downloads\StandardSDK(v3.08)\StandardSDK(v3.08)\include\StCamD.h"
system = SentechSystem(dot_h_file)
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
print("Max image shape: {}".format(cam.max_image_shape))

# set some image properties
cam.image_height = 1040
cam.pixel_format = "Mono8"

# grab a frame
frame = cam.grab_frame()

# get a PIL image and show it
pil_img = frame.as_pil()
pil_img.show()

# release camera
cam.release()
print("Camera released!")