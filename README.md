# pysentech

pysentech wraps the Sentech C API for USB cameras.  It has been tested with the current (v3.08) version of the Sentech USB StandardSDK.  It (currently) only works for Windows.

## Installation

Download and unzip the Sentech StandardSDK for your USB camera.

Install pysentech by running:

    $python setup.py install

## Usage

### Low Level

pysentech *can* be used as a low level wrapper for the C dll using ctypes.  Using it like this is not recommended, but see the "low_level" examples in the examples folder to see how this can be done.

### High Level

Because the Sentech SDK doesn't install itself, you have to provide the path to the StCamD.h header file.  It should be in the "include" folder.  It will try to find StCamD.dll based on the header file location.  If it can't be found you will have to supply the path to StCamD.dll as well.

    >>> from pysentech import SentechSystem

    >>> system = SentechSystem("path/to/header/file.h")

Check for cameras using:

    >>> system.camera_count()

    1

Get a camera by its index:

    >>> cam = system.get_camera(0)

Cameras have several properties:

    >>> cam.gain
    
    0

    >>> cam.gain = 50

    >>> cam.image_shape

    (1360, 1040)

    >>> cam.model

    STC-MB152USB

Get the current frame using:

    >>> frame = cam.grab_frame()

Frames can be cast as various types for your convenience:

    >>> np_img = frame.as_numpy()

    >>> pil_img = frame.as_pil()

Or saved to a file using the SDK's file-saving functions:

    >>> frame.to_file("test_img.png")

The high-level camera objects still have access to all of the low-level functions if you are confortable with ctypes, so you don't have to worry about losing functionality if you find something that hasn't been implemented in the high-level api:

    >>> cmode = c_ushort()

    >>> cam.StCam_GetBinningSumMode(byref(cmode))

    >>> cmode.value

    0

## Known Issues

1. I don't have a color camera, so I can't test color.  I'd love some help with this.

## TODO LIST

1. Figure out how to rope in the SDK's message dll to get better error messages.
1. Acquire and test with a color camera.
1. Implement high-level methods for the SDK's built-in AVI writing for easy movie recording.
1. Get callbacks working.  They are currently the only part of the dll that I haven't implemented.