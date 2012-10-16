#normalize.py

from mongomodels import *
import time
from time import mktime

class Product(DynamicDocument):
  attr = DictField()
  normAttr = DictField()

for p in Product.objects:
  p.normAttr = None
  p.save()

for p in Product.objects:
  for key in p.attr:
    value = p.attr[key]
    try:
      p.normAttr[key] = float(value)
      continue
    except:
      #print value, "is not a float"
      pass
    try:
      t = time.strptime(value, "%Y-%m-%dT%H:%M:%S")
      p.normAttr[key]=mktime(t)
      continue
    except:
      #print value, "is not a datetime"
      pass
    try:
      t = time.strptime(value, "%Y-%m-%d")
      p.normAttr[key]=mktime(t)
      continue
    except:
      #print value, "is not a date"
      pass
    try:
      value = value.replace(".",",").replace("$","&")
      keywords = value.split()
      for keyword in keywords:
        if keyword in p.normAttr:
          p.normAttr[keyword] = p.normAttr[keyword]+1
        else:
          p.normAttr[keyword]=1
    except:
      print value, "is not a string"
      print key, ":", value
  p.save()


    
