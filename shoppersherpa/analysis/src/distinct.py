# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 17:04:58 2012

@author: Max Lang
"""
from parsing import ParsedProduct

# pylint: disable-msg=E1101
for p in ParsedProduct.objects.distinct('attr.tvType'):
    print p
