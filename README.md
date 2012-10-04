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

4) From gitbash run 'source environment-setup.bash' from powershell run 'environment-setup.ps1'

5) To use the virtual environment, run 'source ./Scripts/activate' from bash and for powershell cd to 'Scripts' and run './activate.ps1'

If something messes up, you can run 'environment-delete.ps1' to start over (should work in both, just deletes everything)