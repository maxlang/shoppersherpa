# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 01:41:02 2012

@author: Max Lang
"""

from shoppersherpa import logging

logger = logging.getLogger(__name__)

# Filters take in json for

class Filter(object):
    """ Filters are initiated using a dictionary based on the original josn query.
    They provide convenience methods to return mongoengine filters.

    The constructor takes in a dictionary with the following keys:
        - attribute: the attribute to filter on
        - type: the filter type (include, exclude or range)
        - value: either a list for include/exclude or a 2-elt tuple for range

    Examples:

    >>> f = Filter({'attribute':'size','type':'range','value':[6,30]})
    >>> f.isRange()
    True
    >>> f.max
    30.0
    >>> f.min
    6.0
    >>> f.toMongo()
    {'normalized__size__lte': 30.0, 'normalized__size__gte': 6.0}

    >>> f2 = Filter({'attribute':'brand', 'type':'exclude','value':['Sony','Samsung','Toshiba']})
    >>> f2.isExclude()
    True
    >>> f2.values
    ['Sony', 'Samsung', 'Toshiba']
    >>> f2.toMongo()
    {'normalized__brand__not__in': ['Sony', 'Samsung', 'Toshiba']}

    """

    def __init__(self, filterDict):
        """Expects a dictionary with attribute, type, and value"""
        self.attribute = filterDict['attribute']
        self.type = filterDict['type']

        self.min = None
        self.max = None

        value = filterDict['value']
        if (not self.attribute
               or self.type not in ('include','exclude','range')
               or not value):
            logger.error("Ill-formed filter: %s", filterDict)
            raise ValueError
        if self.type == "range":
            try:
                if value[0] and float(value[0]):
                    self.min = float(value[0])
                if value[1] and float(value[1]):
                    self.max = float(value[1])
                if not self.min and not self.max:
                    logger.warn("Range filter with no max or min specified: %s",filterDict)
            except ValueError:
                logger.error("Non-float range value in range: %s", value)
                raise
        else:
            self.values = value

    def isInclude(self):
        return self.type == "include"

    def isExclude(self):
        return self.type == "exclude"

    def isRange(self):
        return self.type == "range"

    def toMongo(self,prefix="normalized"):
        """Returns the appropriate mongoengine filter dictionary.

        Prefix is the object containing the attributes.
        """
        d = dict()
        if self.isInclude():
            d["{0}__{1}__in".format(prefix, self.attribute)]=self.values
        elif self.isExclude():
            d["{0}__{1}__not__in".format(prefix, self.attribute)]=self.values
        elif self.isRange():
            if self.min:
                d["{0}__{1}__gte".format(prefix, self.attribute)]=self.min
            if self.max:
                d["{0}__{1}__lte".format(prefix, self.attribute)]=self.max
        return d

class FilterMerger(object):
    ''' Holds a bunch of filters, and merges them when required.

    >>> f = FilterMerger()
    >>> f.merge()
    {}
    >>> f.add({'attribute':'size','type':'range','value':[6,30]})
    >>> f.merge()
    {'normalized__size__lte': 30.0, 'normalized__size__gte': 6.0}
    >>> f.add({'attribute':'brand', 'type':'exclude','value':['Sony','Samsung','Toshiba']})
    >>> f.merge()
    {'normalized__size__lte': 30.0, 'normalized__brand__not__in': ['Sony', 'Samsung', 'Toshiba'], 'normalized__size__gte': 6.0}

   '''

    filters = []
    def add(self,f):
        self.filters.append(Filter(f))

    def merge(self,prefix=None):
        """Given a list of filters, return a dictionary representing the combined
        set of filters formatted for mongoengine"""

        d = dict()

        for f in self.filters:
            args = dict()
            if prefix:
                args['prefix'] = prefix
            d = dict(d.items() + f.toMongo(**args).items())

        return d

if __name__ == "__main__":
    import doctest
    doctest.testmod()