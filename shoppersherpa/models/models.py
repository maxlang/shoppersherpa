# -*- coding: utf-8 -*-
"""
Created on Thu Nov 01 13:07:10 2012

@author: Max Lang
"""
from mongoengine import (
    DictField, ListField, StringField, DecimalField, IntField, MapField,
    DateTimeField, URLField, EmbeddedDocument, EmbeddedDocumentField,
    BooleanField, DynamicDocument,connect)

#TODO: make mongoengine models so you can reference dict elts like attributes
# like bottle configdict

#TODO: move away from models
#TODO: make db configurable
connect('test')

class Product(DynamicDocument):
    attr = DictField()
    normalized = DictField()
    meta = {'allow_inheritance': True}


class Attr(EmbeddedDocument):
    attrname = StringField()

    def __unicode__(self):
        return self.attrname + ": "


class ParsedProduct(Product):
    attr = DictField()
    parsedAttr = ListField(EmbeddedDocumentField(Attr))
    keywords = MapField(IntField())

    meta = {'allow_inheritance': True}


class ValueAttr(Attr):
    value = DecimalField()

    def __unicode__(self):
        return super(ValueAttr, self).__unicode__() + unicode(self.value)

    def getKeywords(self):
        return []

    def getValue(self):
        return self.value


class UOMAttr(ValueAttr):
    units = StringField()

    def __unicode__(self):
        return super(UOMAttr, self).__unicode__() + " " + unicode(self.units)
        #return super(ValueAttr,self).__unicode__() + " " + self.units

    def getKeywords(self):
        return []


class AttrInfo(DynamicDocument):
    name = StringField()
    display_name = StringField()
    help_text = StringField()
    rank = IntField()
    is_discrete = BooleanField()
    is_independant = BooleanField()
    units = StringField()
    values = ListField()
    meta = {'allow_inheritance': True}

    def __unicode__(self):
        return "{0}) {1}: {2} {3}".format(self.rank,
                                          self.display_name,
                                          self.values,
                                          self.units)

    @staticmethod
    def lookup(name):
        ais = [x for x in AttrInfo.objects.filter(**{'name': name})]
        if len(ais) != 1:
            return None
        else:
            return ais[0]


class DateTimeAttr(ValueAttr):
    value = DateTimeField()

    def getKeywords(self):
        return []


class RatioAttr(Attr):
    top = DecimalField()
    bottom = DecimalField()

    def __unicode__(self):
        return (super(RatioAttr, self).__unicode__() + unicode(self.top) + ":"
                + unicode(self.bottom))

    def getKeywords(self):
        return [unicode(self.top) + ":" + unicode(self.bottom)]


class DualRatioAttr(RatioAttr):
    top2 = DecimalField()
    bottom2 = DecimalField()

    def __unicode__(self):
        return (super(DualRatioAttr, self).__unicode__() +
                " and " + unicode(self.top2) + ":" + unicode(self.bottom2))

    def getKeywords(self):
        return [unicode(self.top) + ":" + unicode(self.bottom),
                unicode(self.top2) + ":" + unicode(self.bottom2)]


#TODO: should this use UOMAttr instead?
class DimensionAttr(Attr):
    x = EmbeddedDocumentField(ValueAttr)
    y = EmbeddedDocumentField(ValueAttr)
    z = EmbeddedDocumentField(ValueAttr)
    units = StringField()

    def __unicode__(self):
        string = (super(DimensionAttr, self).__unicode__() +
                  unicode(self.x.value) + " " +
                  self.units + " by " + unicode(self.y.value) + " " +
                  self.units)
        if self.z:
            string += unicode(self.z.value) + " " + self.units
        return string

    def getKeywords(self):
        values = [self.x.value, self.y.value]
        if self.z:
            values.append(self.z.value)
        values.sort()
        return ["x".join(values)]


class UOMDescriptionAttr(UOMAttr):
    description = StringField()

    def __unicode__(self):
        return (super(UOMDescriptionAttr, self).__unicode__() +
                " - " + self.description)

    def getKeywords(self):
        return []


class ListAttr(Attr):
    values = ListField(StringField())

    def __unicode__(self):
        string = ""
        for value in self.values:
            string += value + " , "
        return super(ListAttr, self).__unicode__() + string

    def getKeywords(self):
        return []


class StringAttr(ValueAttr):
    value = StringField()

    def getKeywords(self):
        return [self.value]


class DescriptionAttr(ValueAttr):
    value = StringField()

    def getKeywords(self):
        return []


class URLAttr(ValueAttr):
    value = URLField()

    def getKeywords(self):
        return []
