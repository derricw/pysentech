import re
import os
from ctypes import *


def find_dll(header_file, arch="64"):
    abs_path = os.path.abspath(header_file)
    include_folder = os.path.dirname(abs_path)
    root_folder = os.path.dirname(include_folder)
    bin_folder = os.path.join(root_folder, "bin")
    dll_path = os.path.join(bin_folder, "x{}/StCamD.dll".format(arch))
    return dll_path
    
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
    'HANDLE': c_ulong,
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
    def __init__(self, header_file):
        self.header_file = header_file
        self.dll = windll.LoadLibrary(find_dll(header_file))
        
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
        for k, v in functions.iteritems():
            cfunc = getattr(self.dll, k)
            cfunc.__name__ = k
            cfunc.__doc__ = "{}\n arg_types:{}\n arg_names:{}\n returns:{}\n".format(k,
                v['arg_types'], v['arg_names'], v['ret_type'])
            try:
                cfunc.argtypes = [types[t] for t in v['arg_types']]
                #pass
            except KeyError:
                # Can't parse types appropriately        
                #print v['arg_types']
                pass
            try:
                cfunc.restype = types[v['ret_type']]
            except KeyError:
                print("Couldn't parse return type for: {}".format(k))
                
            setattr(self, k, cfunc)
        
    

if __name__ == "__main__":
    dot_h_file = r"C:\Users\derricw\Downloads\StandardSDK(v3.08)\StandardSDK(v3.08)\include\StCamD.h"
    dll = SentechDLL(dot_h_file)
            

