from pymongo import Connection

connection = Connection()
db = connection.test

price = []
size = []

for o in db.products.find():
  try:
    size.append(o['screenSizeIn'])
    price.append(o['offers'][0]['price_history'][0]['regularPrice'])
  except KeyError:
    #size.append(o['screenSizeClassIn'])
    pass
    
import matplotlib.pyplot as plt
plt.plot(size, price, 'ro')
plt.show()