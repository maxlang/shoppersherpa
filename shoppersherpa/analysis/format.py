# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 11:32:47 2012

@author: Max Lang
"""
from shoppersherpa.models.models import Product

keys = sorted(Product.objects.first().normalized.keys())

print ", ".join(keys)

for p in Product.objects:
    s = p.attr['name'].replace(",",".") + ", "
    for k in keys:
        s += str(unicode(p.normalized[k]).strip(u'\x99')) + ", "
    s = s.strip(', ')
    print s

print "done"