# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 18:33:43 2012

@author: Max Lang

Currently, if shoppersherpa isn't on the python path, bottle's reload won't work.
Since I've only added shoppersherpa to the path manually (eg in my IDE) but not
for my os, and I don't want to add it to the os path, this serves as a convenient
workaround.

"""

from shoppersherpa.frontend.controllers import start

start(reload=True)