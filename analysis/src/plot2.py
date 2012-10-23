from mongoengine import *
from models import Product
import matplotlib.pyplot as plt

#connect('test')
#db = connection.test

price = []
size = []

for o in Product.objects:
    attr = o['attr']
    try:
        size.append(attr['screenSizeIn'])
        price.append(attr['regularPrice'])
    except KeyError:
        #size.append(o['screenSizeClassIn'])
        pass
    

plt.plot(size, price, 'ro')
plt.show()