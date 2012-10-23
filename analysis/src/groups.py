'''
Created on Oct 23, 2012

@author: Max Lang
'''

from parsing import ParsedProduct

real = {}
discrete = {}
units = {}

for p in ParsedProduct.objects:
    for a in p.parsedAttr:
        name = a.attrname
        # check for unit clash
        if hasattr(a, 'units'):
            if name in units:
                if units[name] != a.units:
                    print p.attr['name']
                    print "UNIT CLASH:"
                    print "attribute: ", name
                    print "previous unit:", units[name]
                    print "current unit:", a.units
                    print "full attribute: ", a

            else:
                units[name] = a.units