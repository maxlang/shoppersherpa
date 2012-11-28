# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 14:54:18 2012

@author: Max Lang
"""

from bottle import Jinja2Template
from shoppersherpa import logging

logger = logging.getLogger(__name__)

def sortedkeys(d, key=None):
    if key is None:
        return d
    else:
        return sorted(d,key=lambda v:d[v][key])

def sortedvalues(d, key=None):
    if key is None:
        return d
    else:
        return sorted(d.values(),key=lambda v:v[key])

def values(d):
    return d.values();

def jinjaSetup():
    filters = Jinja2Template.settings['filters'] = {}
    filters['sortedkeys'] = sortedkeys
    filters['sortedvalues'] = sortedvalues
    filters['values'] = values