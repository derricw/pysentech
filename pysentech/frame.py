# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 23:18:42 2016

@author: derricw
"""

from ctypes import *
import ctypes
import os

if 'nt' in os.name:
    #windows
    malloc = ctypes.cdll.msvcrt.malloc
    free = ctypes.cdll.msvcrt.free
else:
    raise NotImplementedError("Only Windows supported right now.  Come back later.")

import warnings

try:
    import numpy as np
except ImportError as e:
    warnings.warn("Failed to import numpy. You will be unable to convert frames to ndarrays.")
    
try:
    from PIL import Image
except ImportError as e:
    warnings.warn("Failed to import PIL. You will be unable to convert frames to PIL images.")

# Bytes per pixel
BPP = {
    "Mono8": 1,
    "BGR24": 3,
    "BGR32": 4,
}

# PIL Pixel types
PIL_FORMATS = {
    "Mono8": "L",
    "BGR24": "RGB",  #TODO: figure out how to fix PIL colors
    "BGR32": "RGBA",
}

class _SentechFrame(object):
    """
    A frame from a Sentech camera.  Contains an image buffer and methods to
        convert it easily into ndarrays and PIL images, etc.

    """
    def __init__(self,
                 width,
                 height,
                 bpi,
                 camera,  # annoying that this needs to be here think of a better way
                 pixel_format="Mono8",
                 ):
        self.width = width
        self.height = height
        self.pixel_format = pixel_format
        self.bpi = bpi
        self.bpp = BPP[self.pixel_format]
        self.camera = camera
        self._setup_buffer()
        
    def _setup_buffer(self):
        """ Allocate memory for image """
        # python 2
        #self.imgpointer = malloc(self.bpi)
        #self.buffer = cast(self.imgpointer, POINTER(c_byte))

        # should work in python 2 and 3
        self.buffer = cast(create_string_buffer(self.bpi), POINTER(c_byte))
        
    def _release_buffer(self):
        """ Release memory for image """
        # python 2
        # free(self.imgpointer)
        del self.buffer
        
    def as_array(self):
        """ Returns a ctypes array of the proper shape. """
        return (c_ubyte * int(self.height*self.bpi) *
                int(self.width*self.bpi)).from_address(addressof(self.buffer.contents))
        
    def as_numpy(self):
        """ Returns numpy img. """
        return np.ndarray(buffer=self.as_array(),
                          dtype=np.uint8,
                          shape=(self.height, self.width))
        
        
    def as_pil(self):
        """ Returns PIL img. """
        pformat = PIL_FORMATS[self.pixel_format]
        return Image.frombuffer(pformat,
                                (self.width, self.height), 
                                self.as_array(),
                                "raw",
                                pformat,
                                0, 1)  #TODO: what do these do?

    def to_file(self, path):
        """ Saves an image to a file. 

        args:
            path (str): file path for image
        """
        path = path.encode()
        cpixformat = c_ulong()
        self.camera.StCam_GetPreviewPixelFormat(cpixformat)
        if not self.camera.dll.StCam_SaveImageA(self.camera.handle,
                                                self.width,
                                                self.height,
                                                cpixformat,
                                                self.buffer,
                                                path,
                                                0):
            raise IOError("Couldn't save file to: {}".format(path))
        
    def __del__(self):
        self._release_buffer()
