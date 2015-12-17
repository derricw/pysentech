# -*- coding: utf-8 -*-
"""
Created on Mon Dec 07 22:04:46 2015

@author: derricw
"""
from ctypes import *
malloc = ctypes.cdll.msvcrt.malloc  #windows
free = ctypes.cdll.msvcrt.free  #windows
import traceback

from error import SentechError

#Args that will be passed by reference
POINTER_ARGS = [
    "PWORD",
    "PDWORD",
    "PBYTE",
    "PSHORT",
    "PLONG",
    "PFLOAT",
]

PIXEL_FORMATS = {
    1: "Mono8",
    4: "BGR24",
    8: "BGR32",
}

def make_method(cam, function, arg_types, ret_type, dll):
    """
    Makes a SentechCamera method out of a DLL function.  Automatically passes
        pointer arguments by reference.

    TODO: automatically handle exception raising if return type is BOOL        
        
    """
    method_arg_types = arg_types[1:]
    def method(*args, **kwargs):
        args = [a if method_arg_types[i] not in POINTER_ARGS else byref(a) for i,
                a in enumerate(args) ]
        result = function(cam.handle, *args, **kwargs)
        if ret_type == "BOOL":
            if not result:
                raise SentechError(cam.handle, dll)
        return result
    return method

class SentechCamera(object):
    """
    A sentech camera instance.
    """
    def __init__(self, index, dll):
        self.dll = dll
        self.handle = self.dll.StCam_Open(index)
        
        self._setup_low_level()
        
        self._frame_buffer = None
        self._setup_frame_buffer()
                
    def _setup_low_level(self):
        """
        Takes all dll functions with the camera handle as their first argument
            and makes them into methods of SentechCamera.  This way we still
            retain all low-level functality.
        """
        for k, v in self.dll.functions.iteritems():
            args = v["arg_names"]
            if (len(args) > 0) and (args[0] == "hCamera"):
                method_name = k
                method = make_method(self, v['function'], v['arg_types'],
                                     v['ret_type'], self.dll)
                setattr(self, method_name, method)
                
    def _setup_frame_buffer(self):
        if self._frame_buffer:
            free(self._frame_buffer)
        
    @property        
    def image_size(self):
        size = c_ulong()
        self.StCam_GetRawDataSize(size)
        return size.value

    @property
    def pixel_format(self):        
        cpixformat = c_ulong()
        self.StCam_GetPreviewPixelFormat(cpixformat)
        return PIXEL_FORMATS[cpixformat.value]
    @pixel_format.setter
    def pixel_format(self, value):
        if value not in PIXEL_FORMATS.values():
            raise KeyError("Invalid pixel format, try: {}".format(PIXEL_FORMATS.values()))
        for k, v in PIXEL_FORMATS.iteritems():
            if v == value:
                self.StCam_SetPreviewPixelFormat(k)
        
    @property
    def image_shape(self):
        """
        Gets the current image shape.
        """
        cwidth, cheight = c_ulong(), c_ulong()
        creserved = c_ulong()
        cscanmode = c_ushort()
        coffsetx, coffsety = c_ulong(), c_ulong()
        
        self.StCam_GetImageSize(creserved, cscanmode, coffsetx, coffsety,
                                cwidth, cheight)
        return cwidth.value, cheight.value
    @image_shape.setter
    def image_shape(self, value):
        """
        Sets the image shape.
        
        Warning: Not all sentech USB cameras will let you set
            their width.
        """
        width, height = value
        offsetx, offsety = self.image_offsets
        self.StCam_SetImageSize(0, 8, offsetx, offsety, width, height)
        
    @property
    def image_offsets(self):
        """
        Gets the current image offsets.
        """
        cwidth, cheight = c_ulong(), c_ulong()
        creserved = c_ulong()
        cscanmode = c_ushort()
        coffsetx, coffsety = c_ulong(), c_ulong()
        
        self.StCam_GetImageSize(creserved, cscanmode, coffsetx, coffsety,
                                cwidth, cheight)
        return coffsetx.value, coffsety.value
    @image_offsets.setter
    def image_offsets(self, value):
        """
        Sets the image offsets.
        
        Warning: Not all sentech USB camsers will let you set x offset.   
        """
        offsetx, offsety = value
        width, height = self.image_shape
        self.StCam_SetImageSize(0, 8, offsetx, offsety, width, height)

    @property
    def image_height(self):
        _, height = self.image_shape
        return height
    @image_height.setter
    def image_height(self, value):
        width, _ = self.image_shape
        self.image_shape = width, value
    
    @property
    def image_width(self):
        width, _  = self.image_shape
        return width
    @image_width.setter
    def image_width(self, value):
        _, height = self.image_shape
        self.image_shape = value, height
    
    @property    
    def max_image_shape(self):
        cwidth, cheight = c_ulong(), c_ulong()
        self.StCam_GetMaximumImageSize(cwidth, cheight)
        return cwidth.value, cheight.value
        
    @property
    def model(self):
        name = c_char_p(" "*100)
        self.StCam_GetProductNameA(name, len(name.value))
        return name.value
            
    @property
    def camera_version(self):
        usb_vendor_id = c_ushort()
        usb_product_id = c_ushort()
        fpga_version = c_ushort()
        firm_version = c_ushort()
        self.StCam_GetCameraVersion(usb_vendor_id, usb_product_id,
                                    fpga_version, firm_version)
        return {"usb_vendor_id": usb_vendor_id.value,
                "usb_product_id": usb_product_id.value,
                "fpga_version": fpga_version.value,
                "firm_version": firm_version.value}
            
    @property
    def driver_version(self):
        fileversionms = c_ulong()
        fileversionls = c_ulong()
        prodversionms = c_ulong()
        prodversionls = c_ulong()
        self.StCam_GetDriverVersion(fileversionms, fileversionls,
                                    prodversionms, prodversionls)
        return ("{}.{}".format(fileversionms.value, fileversionls.value),
                "{}.{}".format(prodversionms.value, prodversionls.value))

            
    def reset_settings(self):
        self.StCam_ResetSetting()
    
    def save_settings(self, path):
        """
        Save camera settings to a specified path.

        DOESNT WORK YET        
        """
        self.StCam_SaveSettingFileA(path)

    def load_settings(self, path):
        """
        Load camera settings from path.
        
        DOESNT WORK YET        
        """
        self.StCam_LoadSettingFileA(path)
            
    def release(self):
        self.StCam_Close()
        
    def __del__(self):
        self.release()
        


    
        
if __name__ == "__main__":
    
    from pysentech import SentechDLL
    dot_h_file = r"C:\Users\derricw\Downloads\StandardSDK(v3.08)\StandardSDK(v3.08)\include\StCamD.h"
    dll = SentechDLL(dot_h_file)
    
    camera = SentechCamera(0, dll)
    print camera.model
    print camera.camera_version
    print camera.driver_version
    print camera.image_size
    print camera.pixel_format
    print camera.image_shape
    print camera.max_image_shape
    camera.pixel_format = "Mono8"
    print camera.pixel_format
    camera.release()