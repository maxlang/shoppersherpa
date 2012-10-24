'''
Created on Oct 23, 2012

@author: Max Lang
'''

from parsing import ParsedProduct

real = {}
discrete = {}
units = {}

#TODO: add type fudge factor, eg for dimension units

for p in ParsedProduct.objects:
    for a in p.parsedAttr:
        name = a.attrname
        # check for unit clash
        if hasattr(a, 'units'):
            unit = a.units.lower()
            # convert from years to days where possible
            if ((unit in ['year', 'years'])
                    and hasattr(a, 'value')):
                a.value = a.value * 365
                a.units = 'days'
                p.save()

            if name in units:
                # assume default units if units are empty
                if not units[name] and units:
                    units[name] = units

                elif (unit and units[name] != unit):
                    #check for 1 off
                    if (unit[:-1] == units[name]
                            or unit == units[name][:-1]):
                        print "NEAR MISS"
                        print "attribute: ", name
                        print "previous unit:", units[name]
                        print "current unit:", unit
                    else:
                        print p.attr['name']
                        print "***UNIT CLASH***"
                        print "attribute: ", name
                        print "previous unit:", units[name]
                        print "current unit:", unit
                        print "full attribute: ", a

            else:
                units[name] = unit
                print p.attr['name']
                print "attribute: ", name
                print "unit: ", unit
                print "full attribute: ", a
