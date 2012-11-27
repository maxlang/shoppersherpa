# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 02:27:49 2012

@author: Max Lang
"""
from json import dumps
from shoppersherpa import logging

logger = logging.getLogger(__name__)

def form2json(bottleForm):
    return dumps(dict(bottleForm))