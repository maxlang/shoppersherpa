# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 02:27:49 2012

@author: Max Lang
"""
from shoppersherpa import logging
from bottle import TEMPLATE_PATH, BaseTemplate
import os

logger = logging.getLogger(__name__)

# set up view directory
curdir = os.path.dirname(os.path.realpath(__file__))
logger.debug("frontend dir: %s", curdir)
viewdirname = "views"
viewdir = os.path.join(curdir, viewdirname)
logger.debug("view dir: %s", viewdir)
TEMPLATE_PATH.append(viewdir)
logger.debug("added view dir")
staticdirname = "static"
staticdir = os.path.join(curdir, staticdirname)
logger.debug("static dir: %s", staticdir)

# add view extension (jinja 2 files)
BaseTemplate.extensions.append("jinja")
logger.debug("added jinja extention")