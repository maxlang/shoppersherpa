'''
Created on Oct 22, 2012

@author: Max Lang
'''

from parsing import ParsedProduct

for a in ParsedProduct.objects.first().parsedAttr:
    print a

for p in ParsedProduct.objects:
    p.attr
