from mongoengine import *
from mongomodels import Product
import matplotlib.pyplot as plt

connection = Connection()
db = connection.test

price = []
size = []

for o in Product.objects.find():
    attr = o['attr']
    try:
        size.append(attr['screenSizeIn'])
        price.append(attr['regularPrice'])
    except KeyError:
        #size.append(o['screenSizeClassIn'])
        pass
    

plt.plot(size, price, 'ro')
plt.show()