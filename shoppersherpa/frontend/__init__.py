'''
Created on Nov 1, 2012

@author: Max Lang
'''
from bottle import BaseTemplate, TEMPLATE_PATH
import os

# set up view directory
curdir = os.path.dirname(os.path.realpath(__file__))
viewdirname = "views"
viewdir = os.path.join(curdir, viewdirname)
TEMPLATE_PATH.append(viewdir)

# add view extension (jinja 2 files)
BaseTemplate.extensions.append("jinja")
