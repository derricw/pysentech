# -*- coding: utf-8 -*-
"""
Created on Mon Dec 07 22:04:46 2015

@author: derricw
"""
from ctypes import *
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

def make_method(cam, function, arg_types):
    """
    Makes a SentechCamera method out of a DLL function.  Automatically passes
        pointer arguments by reference.

    TODO: automatically handle exception raising if return type is BOOL        
        
    """
    method_arg_types = arg_types[1:]
    def method(*args, **kwargs):
        args = [a if method_arg_types[i] not in POINTER_ARGS else byref(a) for i, a in enumerate(args) ]
        return function(cam.handle, *args, **kwargs)
    return method

class SentechCamera(object):
    """
    A sentech camera instance.
    """
    def __init__(self, index, dll):
        self.dll = dll
        self.handle = self.dll.StCam_Open(index)
        
        self._setup_low_level()
                
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
                method = make_method(self, v['function'], v['arg_types'])
                setattr(self, method_name, method)
                
    def _get_image_size(self):
        size = c_ulong()
        if self.StCam_GetRawDataSize(size):
            return size.value
        else:
            raise SenpyError("Couldn't get image size")
    
    def __del__(self):
        self.release()
        
    @property
    def model(self):
        name = c_char_p(" "*100)
        if self.StCam_GetProductNameA(name, len(name.value)):
            return name.value
        else:
            raise SenpyError("Couldn't get model #")
            
    @property
    def camera_version(self):
        usb_vendor_id = c_ushort()
        usb_product_id = c_ushort()
        fpga_version = c_ushort()
        firm_version = c_ushort()
        if self.StCam_GetCameraVersion(usb_vendor_id, usb_product_id,
                                       fpga_version, firm_version):
            return {"usb_vendor_id": usb_vendor_id.value,
                    "usb_product_id": usb_product_id.value,
                    "fpga_version": fpga_version.value,
                    "firm_version": firm_version.value}
        else:
            raise SenpyError("Couldn't get camera version")
            
    @property
    def driver_version(self):
        fileversionms = c_ulong()
        fileversionls = c_ulong()
        prodversionms = c_ulong()
        prodversionls = c_ulong()
        if self.StCam_GetDriverVersion(fileversionms, fileversionls,
                                       prodversionms, prodversionls):
            return ("{}.{}".format(fileversionms.value, fileversionls.value),
                    "{}.{}".format(prodversionms.value, prodversionls.value))
        else:
            raise SenpyError("Couldn't get camera version")
            
    def reset_settings(self):
        if not self.StCam_ResetSetting():
            raise SenpyError("Couldn't reset settings.")
    
    def save_settings(self, path):
        """
        Save camera settings to a specified path.

        DOESNT WORK YET        
        
        """
        if not self.StCam_SaveSettingFileA(path):
            raise SenpyError("Couldn't save settings.")

    def load_settings(self, path):
        """
        Load camera settings from path.
        
        DOESNT WORK YET        
        
        """
        if not self.StCam_LoadSettingFileA(path):
            raise SenpyError("Couldn't load camera settings.")
    
    def release(self):
        self.StCam_Close()
        
    
        
if __name__ == "__main__":
    
    from senpy import SentechDLL
    dot_h_file = r"C:\Users\derricw\Downloads\StandardSDK(v3.08)\StandardSDK(v3.08)\include\StCamD.h"
    dll = SentechDLL(dot_h_file)
    
    camera = SentechCamera(0, dll)
    print camera.model
    print camera.camera_version
    print camera.driver_version
    print camera._get_image_size()
    camera.release()