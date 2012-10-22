#normalize.py
from mongoengine import EmbeddedDocument, DecimalField, StringField, DictField,
from models import Product
from datetime import datetime
import re
from django.core.validators import URLValidator

urlValidator = URLValidator(verify_exists=False)


class Attr(EmbeddedDocument):
    attrname = StringField()

    def __str__(self):
        return self.attrname + ":"  


class ParsedProduct(Product):
    attr = DictField()
    parsedAttr = ListField(EmbeddedDocumentField(Attr))
    keywords = MapField(IntField())

    meta = {'allow_inheritance': True}


class ValueAttr(Attr):
    value = DecimalField()

    def __str__(self):
      return self.attrname + ": " + str(self.value)
  
class UOMAttr(ValueAttr):
    units = StringField()
    
    def __str__(self):
      return self.attrname + ": " + str(self.value) + " " + str(self.units)
      #return super(ValueAttr,self).__str__() + " " + self.units

class DateTimeAttr(ValueAttr):
    value = DateTimeField()

class RatioAttr(Attr):
    top = DecimalField()
    bottom = DecimalField()
    
    def __str__(self):
      return self.attrname + ": " + str(self.top) + ":" + str(self.bottom)

class DualRatioAttr(RatioAttr):
    top2 = DecimalField()
    bottom2 = DecimalField()
    
    def __str__(self):
      return self.attrname + ": " + str(self.top) + ":" + str(self.bottom) + " and " + str(self.top2) + ":" + str(self.bottom2)

class DimensionAttr(Attr):
    x = EmbeddedDocumentField(UOMAttr)
    y = EmbeddedDocumentField(UOMAttr)
    z = EmbeddedDocumentField(UOMAttr)
    
    def __str__(self):
      s = self.attrname + ": " + str(self.x.value) + " " + self.x.units + " by " + str(self.y.value) + " " + self.y.units
      if self.z:
        s = s + str(self.z.value) + " " + self.z.units
      return s

class UOMDescriptionAttr(UOMAttr):
    description = StringField()
    def __str__(self):
      return self.attrname + ": " + str(self.value) + " " + str(self.units) + " - " + self.description

class ListAttr(Attr):
    values = ListField(StringField())

    def __str__(self):
        s = ""
        for v in self.values:
            s = s + v + " , "
        return self.attrname + ": " + s

class DescriptionAttr(ValueAttr):
    value = StringField()

class URLAttr(ValueAttr):
    value = URLField()

# clear out old values
for p in ParsedProduct.objects:
    p.parsedAttr = None
    p.keywords = None
    p.save()


for p in Product.objects:
    tempattr = p.attr
    p.delete()
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
      except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        #pass
    
      #numbers with commas
      try:
        p.parsedAttr.append(ValueAttr(attrname=key, value=float(v.replace(",", ""))))
        #print "comma float: ", v
        continue
      except ValueError:
        pass
      except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        #pass
    
      #datetime
      try:
        p.parsedAttr.append(DateTimeAttr(attrname=key, value=datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")))
        #print "datetime: ", v
        continue
      except ValueError:
        pass
      except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        #pass
      
      #TODO: zero out time
      #date
      try:
        p.parsedAttr.append(DateTimeAttr(attrname=key, value=datetime.strptime(v, "%Y-%m-%d")))
        #print "date: ", v
        continue
      except ValueError:
        pass
      except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        #pass
    
      # Value with units
      try:
        match = re.match(r"^([-0-9.,]+)([^0-9]*)$", v)
        if(match):
          p.parsedAttr.append(UOMAttr(attrname=key, value=float(match.group(1).replace(",", "")) , units=match.group(2)))
          #print "unit val: ", v
          continue
      except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        #pass
    
      # Ratios
      try:
        match = re.match(r"^([-0-9.,]+):([-0-9.,]+)$", v)
        if(match):
          p.parsedAttr.append(RatioAttr(attrname=key, top=float(match.group(1).replace(",", "")), bottom=float(match.group(2).replace(",", ""))))
          #print "ratio: ", v
          continue
      except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        #pass
    
      # Dimensions
      try:
        match = re.match(r"^([-0-9.,]+)\s*([^0-9]*)\s?(?:x|\*|by|BY|By)\s?([-0-9.,]+)\s*([^0-9]*)(?:\s?(?:x|\*|by|BY|By)\s?([-0-9.,]+)\s*([^0-9]*))?$", v)
        
        if(match):
          dims = DimensionAttr(attrname=key)
          dims.x = UOMAttr(value=float(match.group(1).replace(",", "")), units=match.group(2))
          dims.y = UOMAttr(value=float(match.group(3).replace(",", "")), units=match.group(4))
          if(match.group(5)):
            dims.z = UOMAttr(value=float(match.group(5).replace(",", "")), units=match.group(6))
          p.parsedAttr.append(dims)
          #print dims.x.value,dims.x.units,"x",dims.y.value,dims.y.units
          #if dims.z:
            #print "x",dims.z.value,dims.z.units
          #print "dimensions: ", v
          continue
      except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        #pass
    
      #compound fractions with units
      try:
        match = re.match(r"^([-0-9.,]+)(?: | ?- ?| ?and ?)([0-9.]*) ?/ ?([0-9.]*)([^0-9.]*)$", v)
        if(match):
          p.parsedAttr.append(UOMAttr(attrname=key, value=float(match.group(1).replace(",", "")) + (float(match.group(2)) / float(match.group(3))), units=match.group(4)))
          #print float(match.group(1).replace(",",""))+(float(match.group(2))/float(match.group(3)))
          #print "compound fraction: ", v
          continue
      except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        #pass
        
      # URL
      try:
        urlValidator(v)
        p.parsedAttr.append(URLAttr(attrname=key, value=v))
        #print "url: ", v
        continue
      except ImportError:
        pass
      except Exception as inst:
        print type(inst)
        print inst.args
        print inst
        #pass

    # Value with units and description
    try:
      match = re.match(r"^([-0-9.,]+)\s?([^\s0-9]*)\s+([^;\\/,:-_]*)$", v)
      if(match):
        p.parsedAttr.append(UOMDescriptionAttr(attrname=key, value=float(match.group(1).replace(",", "")), units=match.group(2), description=match.group(3)))
        #print "unit val + desc: ", v
        continue
    except Exception as inst:
      print type(inst)
      print inst.args
      print inst
      #pass

    #dual ratios
    try:
      match = re.match(r"^([-0-9.,]+):([-0-9.,]+)(?: ?and ?| ?, ?|\|)([-0-9.,]+):([-0-9.,]+)$", v)
      if(match):
        p.parsedAttr.append(DualRatioAttr(attrname=key, top=float(match.group(1).replace(",", "")), bottom=float(match.group(2).replace(",", "")),
                             top2=float(match.group(3).replace(",", "")), bottom2=float(match.group(4).replace(",", ""))))
        #print "dual ratio: ", v
        continue
    except Exception as inst:
      print type(inst)
      print inst.args
      print inst
      #pass

    delimeters = [",", ".", "/", "\\", ";", ":", " ", "-", "_"]
    counts = {}

    counts = dict([(d, v.count(d)) for d in delimeters])

    # Simple String
    if max(counts.values()) == 0:
      p.parsedAttr.append(DescriptionAttr(attrname=key, value=v))
      #print "simple string: ", v
      continue

    # Only spaces
    nonSpaceCounts = counts.copy()
    del nonSpaceCounts[' ']
    nonSpaceMax = max(nonSpaceCounts.values())
    if nonSpaceMax == 0:
      p.parsedAttr.append(DescriptionAttr(attrname=key, value=v))
      #print "only spaces string: ", v
      continue

    # Mostly spaces
    magicMarginOfError = 7.5               
    if (nonSpaceMax <= 1) or (counts[" "] / nonSpaceMax > magicMarginOfError):
      p.parsedAttr.append(DescriptionAttr(attrname=key, value=v))
      #print "mostly spaces string: ", v
      continue

    #List
    if (nonSpaceMax >= 3 and (counts[" "] / nonSpaceMax < 5.5)):
      delimeter = nonSpaceCounts.keys()[nonSpaceCounts.values().index(max(nonSpaceCounts.values()))]
      p.parsedAttr.append(ListAttr(attrname=key, values=map(lambda str: str.strip(), v.split(delimeter))))
      print "list of strings: ", v
      continue

    p.parsedAttr.append(DescriptionAttr(attrname=key, value=v))
    print "description or couldn't parse: ", v
    print counts

    p.save()
##for p in Product.objects:
##  for key in p.attr:
##    value = p.attr[key]
##    if if isinstance(['asdf'], basestring):

    

