#parse.py
from mongoengine import (
     DictField, ListField, StringField, DecimalField, IntField, MapField,
     DateTimeField, URLField, EmbeddedDocument, EmbeddedDocumentField)

from models import Product
from datetime import datetime
import re
from django.core.validators import URLValidator

urlValidator = URLValidator(verify_exists=False)


class Attr(EmbeddedDocument):
    attrname = StringField()

    def __unicode__(self):
        return self.attrname + ":"


class ParsedProduct(Product):
    attr = DictField()
    parsedAttr = ListField(EmbeddedDocumentField(Attr))
    keywords = MapField(IntField())

    meta = {'allow_inheritance': True}


class ValueAttr(Attr):
    value = DecimalField()

    def __unicode__(self):
        return self.attrname + ": " + unicode(self.value)

    def getKeywords(self):
        return []

    def getValue(self):
        return self.value


class UOMAttr(ValueAttr):
    units = StringField()

    def __unicode__(self):
        return self.attrname + ": " + unicode(self.value) + " " + unicode(self.units)
        #return super(ValueAttr,self).__unicode__() + " " + self.units

    def getKeywords(self):
        return []


class DateTimeAttr(ValueAttr):
    value = DateTimeField()

    def getKeywords(self):
        return []


class RatioAttr(Attr):
    top = DecimalField()
    bottom = DecimalField()

    def __unicode__(self):
        return self.attrname + ": " + unicode(self.top) + ":" + unicode(self.bottom)

    def getKeywords(self):
        return [unicode(self.top) + ":" + unicode(self.bottom)]


class DualRatioAttr(RatioAttr):
    top2 = DecimalField()
    bottom2 = DecimalField()

    def __unicode__(self):
        return (self.attrname + ": " + unicode(self.top) + ":" + unicode(self.bottom) +
                " and " + unicode(self.top2) + ":" + unicode(self.bottom2))

    def getKeywords(self):
        return [unicode(self.top) + ":" + unicode(self.bottom),
                unicode(self.top2) + ":" + unicode(self.bottom2)]


class DimensionAttr(Attr):
    x = EmbeddedDocumentField(ValueAttr)
    y = EmbeddedDocumentField(ValueAttr)
    z = EmbeddedDocumentField(ValueAttr)
    units = StringField()

    def __unicode__(self):
        string = (self.attrname + ": " + unicode(self.x.value) + " " +
            self.units + " by " + unicode(self.y.value) + " " + self.units)
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
        return self.attrname + ": " + unicode(self.value) + " " + \
                    unicode(self.units) + " - " + self.description

    def getKeywords(self):
        return []


class ListAttr(Attr):
    values = ListField(StringField())

    def __unicode__(self):
        string = ""
        for value in self.values:
            string += value + " , "
        return self.attrname + ": " + string

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


if __name__ == "__main__":
    print 'removing old data'

    print "Product count ", len(ParsedProduct.objects)

    # clear out old values
    for p in ParsedProduct.objects:
        p.parsedAttr = None
        p.keywords = None
        p.save()

    print 'adding new data'

    for prod in Product.objects:
        tempattr = prod.attr
        p = ParsedProduct(attr=tempattr)
        for key in p.attr:
            #print "parsing: ", key
            v = p.attr[key]
            #float, int, and bool
            try:
                p.parsedAttr.append(ValueAttr(attrname=key, value=float(v)))
                #print "float: ", v
                continue
            except ValueError:
                pass

            #numbers with commas
            try:
                p.parsedAttr.append(
                ValueAttr(attrname=key,
                          value=float(v.replace(",", ""))))
                #print "comma float: ", v
                continue
            except ValueError:
                pass

            #datetime
            try:
                p.parsedAttr.append(DateTimeAttr(
                    attrname=key,
                    value=(datetime.strptime(v, "%Y-%m-%dT%H:%M:%S"))))
                #print "datetime: ", v
                continue
            except ValueError:
                pass

            #date
            try:
                date = datetime.strptime(v, "%Y-%m-%d")
                #zero out the time
                date.replace(hour=0, minute=0, second=0, microsecond=0)

                p.parsedAttr.append(DateTimeAttr(
                    attrname=key,
                    value=date))

                #print "date: ", v
                continue
            except ValueError:
                pass

            # Value with units
            match = re.match(r"^([-0-9.,]+)[\s]*([^\s0-9.]*)\.?\s*$", v)
            if(match):
                p.parsedAttr.append(UOMAttr(attrname=key,
                    value=float(match.group(1).replace(",", "")),
                    units=match.group(2)))
                print "unit val: ", v
                continue

            # Ratios
            match = re.match(r"^([-0-9.,]+):([-0-9.,]+)$", v)
            if(match):
                p.parsedAttr.append(RatioAttr(
                  attrname=key,
                  top=float(match.group(1).replace(",", "")),
                  bottom=float(match.group(2).replace(",", ""))))
                #print "ratio: ", v
                continue

            # Dimensions
            match = re.match(r'''
                             ^([-0-9.,]+)        # Starts with a decimal number
                             \s*                 # Any number of spaces
                             ([^0-9.]*)          # Non numeric string (units)
                             \.?\s*              # An optional string
                             (?:x|\*|by|BY|By)   # a multiplication symbol
                             \s?                 # another optional space
                             ([-0-9.,]+)         # second number
                             \s*
                             ([^0-9.]*)           # second units
                             (?:                 # optional third dimension
                                 \.?\s*
                                 (?:x|\*|by|BY|By)
                                 \s?
                                 ([-0-9.,]+)
                                 \s*
                                 ([^0-9.]*)
                             )?                 # end of string
                             \s*
                             $''',
                             v,
                             flags=re.X)

            if(match):
                if ((match.group(2).strip() == match.group(4).strip())
                        and (not match.group(6)
                             or match.group(2).strip() == match.group(6).strip())):
                    dims = DimensionAttr(attrname=key,
                                         units=match.group(2).strip())
                    dims.x = ValueAttr(
                        value=float(match.group(1).replace(",", "")))
                    dims.y = ValueAttr(
                        value=float(match.group(3).replace(",", "")))
                    if(match.group(5)):
                        dims.z = ValueAttr(
                            value=float(match.group(5).replace(",", "")))
                    p.parsedAttr.append(dims)
                    print "dimensions: ", v
                    continue
                else:
                    print "UNIT MISMATCH: "
                    print v
                    print match.group(2), match.group(4), match.group(6)

            #compound fractions with units

            match = re.match(r'''
                              ^([-0-9.,]+)
                              (?:\ |\ ?-\ ?|\ ?and\ ?)       #escaped spaces
                              ([0-9.]*)
                              \ ?/\ ?                        #escaped spaces
                              ([0-9.]*)
                              ([^0-9.\s]*)\.?\s*$''',
                              v,
                              flags=re.X)
            if(match):
                fractionValue = (float(match.group(1).replace(",", "")) +
                    (float(match.group(2)) / float(match.group(3))))

                uomattr = UOMAttr(attrname=key,
                                 value=fractionValue,
                                 units=match.group(4))

                p.parsedAttr.append(uomattr)
                #print float(match.group(1).replace(",",""))+
                #            (float(match.group(2))/float(match.group(3)))
                print "compound fraction: ", v
                continue

            # URL
            try:
                urlValidator(v)
                p.parsedAttr.append(URLAttr(attrname=key, value=v))
                #print "url: ", v
                continue
            except ImportError:
                pass

            # Value with units and description
            match = re.match(r"^([-0-9.,]+)\s*([^\s+0-9.]+)\.?\s+([^;\\/,:-_]*)$",
                             v)
            if(match):
                p.parsedAttr.append(UOMDescriptionAttr(
                    attrname=key,
                    value=float(match.group(1).replace(",", "")),
                    units=match.group(2),
                    description=match.group(3)))
                print "unit val + desc: ", v
                print match.group(1)
                print match.group(2)
                print match.group(3)
                continue

            #dual ratios
            match = re.match(r'''
                             ^([-0-9.,]+)
                             :
                             ([-0-9.,]+)
                             (?:\ ?and\ ?|\ ?,\ ?|\|)
                             ([-0-9.,]+)
                             :
                             ([-0-9.,]+)$''',
                             v,
                             flags=re.X)
            if(match):
                p.parsedAttr.append(DualRatioAttr(
                    attrname=key,
                    top=float(match.group(1).replace(",", "")),
                    bottom=float(match.group(2).replace(",", "")),
                    top2=float(match.group(3).replace(",", "")),
                    bottom2=float(match.group(4).replace(",", ""))))
                #print "dual ratio: ", v
                continue

            delimeters = [",", ".", "/", "\\", ";", ":", " ", "-", "_"]
            counts = {}

            counts = dict([(d, v.count(d)) for d in delimeters])

            # Simple String
            if max(counts.values()) == 0:
                p.parsedAttr.append(StringAttr(attrname=key, value=v))
                #print "simple string: ", v
                continue

            # Only spaces
            nonSpaceCounts = counts.copy()
            del nonSpaceCounts[' ']
            nonSpaceMax = max(nonSpaceCounts.values())
            if nonSpaceMax == 0:
                if(counts[' '] > 2):
                    p.parsedAttr.append(DescriptionAttr(attrname=key, value=v))
                else:
                    p.parsedAttr.append(StringAttr(attrname=key, value=v))
                #print "only spaces string: ", v
                continue

            # Mostly spaces
            magicMarginOfError = 7.5
            if ((nonSpaceMax <= 1)
                or (counts[" "] / nonSpaceMax > magicMarginOfError)):
                p.parsedAttr.append(DescriptionAttr(attrname=key, value=v))
                #print "mostly spaces string: ", v
                continue

            #List
            if (nonSpaceMax >= 3 and (counts[" "] / nonSpaceMax < 5.5)):
                delimeterIndex = nonSpaceCounts.values().index(
                    max(nonSpaceCounts.values()))
                delimeter = nonSpaceCounts.keys()[delimeterIndex]
                p.parsedAttr.append(ListAttr(
                     attrname=key,
                     values=[s.strip() for s in v.split(delimeter)]))
                #print "list of strings: ", v
                continue

            p.parsedAttr.append(DescriptionAttr(attrname=key, value=v))
            print "description or couldn't parse: ", v
            print counts

        p.save()
        prod.delete()

    print 'done'

##for p in Product.objects:
##  for key in p.attr:
##    value = p.attr[key]
##    if if isinstance(['asdf'], basestring):
