ShopperSherpa
=============

Environment setup on Windows (assumes you already have python, and git installed):
1) Install mercurial from here: http://mercurial.selenic.com/
2) Install mongodb using instructions here: http://docs.mongodb.org/manual/tutorial/install-mongodb-on-windows/
3) Setup pip:
(taken from: http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows)
 - Download the last pip version from here: http://pypi.python.org/pypi/pip#downloads
 - Uncompress it
 - Download the last easy installer for Windows: (download the .exe at the bottom of http://pypi.python.org/pypi/setuptools ). Install it.
 - go to the uncompressed pip directory and: python setup.py install
 - Add your python c:\Python2x\Scripts to the path

4) From inside the git repository run 'environment-setup.ps1' from the commandline (should work in gitbash or windows powershell)
NOTE: there will be some errors because some lines only work in powershell and vice versa


If something messes up, you can run 'environment-delete.ps1' to start over.