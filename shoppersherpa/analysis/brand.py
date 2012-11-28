# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 15:40:43 2012

@author: Max Lang
"""
from matplotlib import pyplot
from shoppersherpa.api.api import query

price = []
rating = []

b = query('{"keywords":"televisions"}')['attrs']['brand']

for option in b['options']:
    for stat in option['stats']:
        if 'price' in option['stats'] and 'ratings_avg' in option['stats']:
            price.append(option['stats']['price']['mean'])
            rating.append(option['stats']['ratings_avg']['mean'])

pyplot.scatter(rating,price)
pyplot.show()