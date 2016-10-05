# pysentech

pysentech wraps the Sentech C API for USB cameras.  It has been tested with the current (v3.08) version of the Sentech USB StandardSDK.

## Installation

Download and unzip the Sentech StandardSDK for your USB camera.

Install pysentech by running:

    $python setup.py install

Or using pip:

    $pip install pysentech

## Dependencies

There are no hard dependencies for controlling cameras and acquiring frames.  However some of the examples use OpenCV, numpy, and PIL to display images.

## Usage

### Low Level

pysentech *can* be used as a low level wrapper for the C dll using ctypes.  Using it like this is not recommended, but see the "low_level" examples in the examples folder to see how this can be done.

### High Level

Because the Sentech SDK doesn't install itself, you have to provide the SDK folder.  It should contain an "include" folder.  It will then try to find the StCamD.dll and StCamD.h file location.

    >>> from pysentech import SentechSystem

    >>> system = SentechSystem("sentch/sdk/folder")

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

![alt text](https://github.com/derricw/pysentech/blob/master/pysentech/examples/sentechmpl.png "mpl image")

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
1. Python3 support.
1. Acquire and test with a color camera.
1. Implement high-level methods for the SDK's built-in AVI writing for easy movie recording.
1. Get callbacks working.  They are currently the only part of the dll that I haven't implemented.