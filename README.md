ShopperSherpa
=============

Environment setup on Windows (assumes you already have python, and git installed):
1) Install mongodb using instructions here: http://docs.mongodb.org/manual/tutorial/install-mongodb-on-windows/
2) Setup pip:
(taken from: http://stackoverflow.com/questions/4750806/how-to-install-pip-on-windows)
 - Download the last pip version from here: http://pypi.python.org/pypi/pip#downloads
 - Uncompress it
 - Download the last easy installer for Windows: (download the .exe at the bottom of http://pypi.python.org/pypi/setuptools ). Install it.
 - go to the uncompressed pip directory and: python setup.py install
 - Add your python c:\Python2x\Scripts to the path
 - I recommend you install svn and mercurial to allow easier use of pip

===============

Python libraries to install:
- numpy
- scipy
- matplotlib
- django
- pymongo
- mongoengine

===============

Eclipse tips:

- enable pylint and pep8 for code style help
- add "--generated-members=objects" to the list of arguments to pass to pylint (mongoengine generates these fields)
- add mongoengine to your forced builtins (Interpreter - Python > Forced Builtins tab)
- I remcommend looking through the pydev editor options and choosing some things that make sense
- In the general text editor options, I recommend showing the print margins (General > Editors > Text Editors)
