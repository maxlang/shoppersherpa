# -*- coding: utf-8 -*-
"""
Created on Thu Nov 01 15:28:58 2012

@author: Max Lang
"""

import logging
import os

#TODO: where should logging go?
#TODO:config
curdir = os.path.dirname(os.path.realpath(__file__))
logdirname = "logs"
logdir = os.path.join(curdir, logdirname)
if not os.path.exists(logdir):
    os.mkdir(logdir)
logfilename = "shoppersherpa.log"
logfile = os.path.join(logdir, logfilename)

# root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(logfile)
fh.setLevel(logging.DEBUG)

#console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
# uncomment the following line to add console output
#logger.addHandler(ch)
logger.addHandler(fh)

logger.debug("root logger initialized")

logger2 = logging.getLogger(__name__)

logger2.debug("shoppersherpa initialized")