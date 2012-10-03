ShopperSherpa
=============

Environment setup on Windows (assumes you already have python, and git installed):
1) Install mercurial from here: http://mercurial.selenic.com/
2) Setup pip:
(taken from: http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows)
 - Download the last pip version from here: http://pypi.python.org/pypi/pip#downloads
 - Uncompress it
 - Download the last easy installer for Windows: (download the .exe at the bottom of http://pypi.python.org/pypi/setuptools ). Install it.
 - go to the uncompressed pip directory and: python setup.py install
 - Add your python c:\Python2x\Scripts to the path
3) Setup mingw:
(taken from: http://stackoverflow.com/questions/2817869/error-unable-to-find-vcvarsall-bat)
- Install mingw32 to C:\mingw\
- Add mingw32's bin directory to your environment variable: append PATH with C:\MinGW\bin;
- Edit ( create if not existing ) distutils.cfg located at C:\Python2x\Lib\distutils\distutils.cfg to be:

    [build]
    compiler=mingw32

4) From inside the git repository run 'environment-setup.ps1' from the commandline (should work in gitbash or windows powershell)
NOTE: there will be one multiline error (in powershell "source is not recognized..." and in gitbash "@echo: command not found...")


If something messes up, you can run 'environment-delete.ps1' to start over.