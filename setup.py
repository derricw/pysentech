from setuptools import setup, find_packages
import os, sys, glob, fnmatch

setup(name="pysentech",
      version=0.1,
      description="pysentech is a python wrapper for the Sentech USB Camera SDK",
      long_description=""" pysentech is a python wrapper for the Sentech USB Camera SDK.
        It features a low-level interface for interacting with the C dll directly, and a high-level
        interface with more pythonic camera and frame objects.
      """,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Microsoft :: Windows',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.7',
          'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
          'Topic :: Multimedia :: Video :: Display',
          'Topic :: Software Development :: Libraries :: Python Modules'],
      author='derricw',
      author_email='derricw@gmail.com',
      url='https://github.com/derricw/pysentech',
      download_url="https://github.com/derricw/pysentech/tarball/0.1",
      license='MIT',
      packages=['pysentech'],
      zip_safe=False,
)