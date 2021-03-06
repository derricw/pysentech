"""
sentechdll.py

Python wrapper for Sentech C DLL.
"""
import re
import os
import sys
from ctypes import *
from ctypes.wintypes import *

from .error import SentechSystemError


def find_dll(header_file):
    """
    Attemps to find the StCamD.dll for the appropriate archetecture given the
        location of the header file ("StCamD.h")

    args:
        header_file (str): path to header file.

    returns:
        str: path to dll for appropriate arch
    """
    if sys.maxsize > 2**32:
        arch = "64"
    else:
        arch = "32"
    abs_path = os.path.abspath(header_file)
    include_folder = os.path.dirname(abs_path)
    root_folder = os.path.dirname(include_folder)
    bin_folder = os.path.join(root_folder, "bin")
    dll_path = os.path.join(bin_folder, "x{}/StCamD.dll".format(arch))
    if os.path.isfile(dll_path):
        return dll_path
    else:
        raise IOError("Couldn't find StCamD.dll.  Please find it manually and enter the path as a kwarg.")
    
#Types to define
types = {
    'BOOL': c_bool,
    'BOOL*': c_bool,
    'LONG': c_long,
    'ULONG': c_ulong,
    'PLONG': POINTER(c_long),
    'DOUBLE': c_double,
    'WCHAR': c_wchar,
    'UINT': c_uint,
    'WORD': c_ushort,
    'DWORD': c_ulong,
    #'HANDLE': c_ulong,
    'HANDLE': POINTER(HANDLE),
    'PWORD': POINTER(c_ushort),
    'PDWORD': POINTER(c_ulong),
    'HWND*': POINTER(c_ulong),
    'HWND': c_ulong,
    'HMENU': c_ulong,
    'BYTE': c_byte,
    'PBYTE': POINTER(c_byte),
    'HDC*': POINTER(c_ulong),
    'PSTR': c_char_p,
    'PWSTR': c_wchar_p,
    'PCSTR': c_char_p,
    'PCWSTR': c_wchar_p,
    'HDC': c_ulong,
    'FLOAT': c_float,
    'PFLOAT': POINTER(c_float),
    'SHORT': c_short,
    'PSHORT': POINTER(c_short),
    'LPVOID': c_void_p,
    'VOID': c_void_p,
}


class SentechDLL(object):
    """
    Auto-generated python library using the C DLL.

    args:
        sdk_folder (Optional[str]): Sentech SDK folder
            (probably something like: '/blah/blah/StandardSDK(v3.08)')
            If nothing is provided, then SENTECHPATH env variable is used.
    """
    def __init__(self, sdk_folder=""):
        if not sdk_folder:
            try:
                sdk_folder = os.environ['SENTECHPATH']
            except KeyError:
                raise SentechSystemError("Couldn't find Sentech SDK. Use sdk_folder kwarg or set SENTECHPATH environment varialble.")

        self.header_file = os.path.join(sdk_folder, "include/StCamD.h")
        if not os.path.isfile(self.header_file):
            raise SentechSystemError("No header file located @ {}".format(self.header_file))
        self.path = find_dll(self.header_file)

        self.dll = windll.LoadLibrary(self.path)  #WINDOWS
        
        self._load_constants()
        self._load_functions()
        
    def _load_constants(self):
        with open(self.header_file, "r") as hfile:
    
            # Get all constants and their values
            define = re.compile(r'\#define\s+(\S+)\s+(".*"|\S+)')            
            for line in hfile:
                m = define.match(line)
                if m:
                    name = m.group(1)
                    value = m.group(2)
                    try:
                        exec("self.{}={}".format(name, value))
                    except NameError:
                        pass
                    except SyntaxError:
                        pass
                    
    def _load_functions(self):
        # Get all function names
        with open(self.header_file, "r") as hfile:
            functions = {}
            
            for line in hfile:
                if " WINAPI " in line:
                    ret_type, func = line.split(" WINAPI ")
                    func_name, func_args = func.split("(")
                    
                    func_args = func_args.split(")")[0]
                    func_args = [f.strip(" ") for f in func_args.split(",")]
                    func_arg_types = [f.split(" ")[0] for f in func_args]
                    try:
                        func_arg_names = [f.split(" ")[1] for f in func_args]
                    except IndexError:
                        func_arg_names = []
                        pass
                    functions[func_name] = {'arg_types': func_arg_types,
                                            'arg_names': func_arg_names,
                                            'ret_type': ret_type,}
        # Set up their return and arg types
        for k, v in functions.items():
            cfunc = getattr(self.dll, k)
            cfunc.__name__ = k
            cfunc.__doc__ = "{}\n arg_types:{}\n arg_names:{}\n returns:{}\n".format(k,
                v['arg_types'], v['arg_names'], v['ret_type'])
            try:
                cfunc.argtypes = [types[t] for t in v['arg_types']]
                pass
            except KeyError:
                # Can't parse types appropriately        
                #print v['arg_types']
                pass
            try:
                cfunc.restype = types[v['ret_type']]
                #print(cfunc.restype)
            except KeyError:
                print("Couldn't parse return type for: {}".format(k))
            functions[k]['function'] = cfunc
            setattr(self, k, cfunc)
        self.functions = functions
        
    

if __name__ == "__main__":
    sentech_folder = r"C:\Users\derricw\Downloads\StandardSDK(v3.08)\StandardSDK(v3.08)"
    dll = SentechDLL(sentech_folder)

