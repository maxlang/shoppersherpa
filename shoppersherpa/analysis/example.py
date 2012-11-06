'''
Created on Oct 22, 2012

@author: Max Lang
'''
from parsing import ParsedProduct
from matplotlib import pyplot
from numpy import array, log, e

size = []          # screenSizeIn or screenSizeClassIn
price = []         # regularPrice
avg_review = []     # customerReviewAverage
num_review = []     # customerReviewCount

# pylint: disable-msg=E1101
for p in ParsedProduct.objects.limit(500):
    try:
        size.append(p.attr['screenSizeIn'])
    except KeyError:
        try:
            size.append(p.attr['screenSizeClassIn'])
        except KeyError:
            continue
    price.append(p.attr['regularPrice'])
    try:
        avg_review.append(p.attr['customerReviewAverage'])
    except KeyError:
        avg_review.append(0)
        num_review.append(0)
        continue
    num_review.append(p.attr['customerReviewCount'])

print 'done'

# convert to numpy arrays
size = array(size)
price = array(price)
avg_review = array(avg_review)
num_review = array(num_review)

pyplot.figure(1)
pyplot.scatter(size, price, ((num_review / 10) ** 2) + 20, (avg_review ** 2))
cbar = pyplot.colorbar()
cbar.set_label("average review squared")
pyplot.title("larger size = more reviews")
pyplot.ylim(ymin=0)
pyplot.ylabel("price")
pyplot.xlabel("size")

pyplot.figure(2)
pyplot.scatter(price, avg_review, (size / 5) ** 2, log(num_review))
pyplot.ylim(ymin=0)
cbar2 = pyplot.colorbar()
cbar2.set_label("log(num reviews)")
pyplot.xlabel("price")
pyplot.ylabel("average review")
pyplot.title("larger point = larger tv (quadratic)")

pyplot.figure(3)
pyplot.scatter(num_review, avg_review, e ** (size / 10),
               log(price))

pyplot.ylim(ymin=0)
cbar3 = pyplot.colorbar()
cbar3.set_label("log price")
pyplot.title("larger point = larger tv (exponential)")
pyplot.ylabel("average review")
pyplot.xlabel("number of reviews")
pyplot.show()
