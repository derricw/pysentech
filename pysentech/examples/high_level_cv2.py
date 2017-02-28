# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 22:53:51 2016

@author: derricw

high_level_cv2.py

Example for high level camera API using OpenCV to show the image.

Demonstrates how to:

1) Initialize SentechSystem
2) Open a camera
3) Read camera properties
4) Set some camera properties
5) Create and OpenCV window
6) Show the live feed from the camera in the window until ESC pressed.
7) Release the camera

"""
import cv2
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
print("Max image shape: {}".format(cam.max_image_shape))
print("Gain: {}".format(cam.gain))
print("Max Gain: {}".format(cam.max_gain))
print("Exposure: {} seconds".format(cam.exposure))
print("Max Exposure: {} seconds".format(cam.max_exposure))

#import pdb; pdb.set_trace()

# set some image properties
cam.image_height = 1040
cam.pixel_format = "Mono8"

# enter into an opencv live view
cv2.namedWindow("pysentech")

while True:
    img = cam.grab_frame().as_numpy()
    cv2.imshow("pysentech", img)
    
    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        break
    elif k % 256 == 61:
        # + pressed
        cam.gain += 10
    elif k % 256 == 45:
        # - pressed
        cam.gain -= 10

cv2.destroyAllWindows()

# release camera
cam.release()
print("Camera released!")