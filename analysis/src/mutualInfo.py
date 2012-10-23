#from parsing import ParsedProduct
#from numpy import array, log, e

import numpy
from numpy import *
from scipy import *
from models import Product


#Mutual information
def mutual_info(x, y):
    N = double(x. size)
    I = 0.0
    eps = numpy.finfo(float).eps
    for l1 in unique(x):
        for l2 in unique(y):
            #Find the intersections
            l1_ids = nonzero(x == l1)[0]
            l2_ids = nonzero(y == l2)[0]
            pxy = (double(intersect1d(l1_ids, l2_ids).size) / N) + eps
            I += pxy * log2(pxy / ((l1_ids.size / N) * (l2_ids.size / N)))
    return I


#Normalized mutual information
def nmi(x, y):
    N = x.size
    I = mutual_info(x, y)
    Hx = 0
    for l1 in unique(x):
        l1_count = nonzero(x == l1)[0].size
        Hx += -(double(l1_count) / N) * log2(double(l1_count) / N)
    Hy = 0
    for l2 in unique(y):
        l2_count = nonzero(y == l2)[0].size
        Hy += -(double(l2_count) / N) * log2(double(l2_count) / N)
    return I / ((Hx + Hy) / 2)


def getIdxIfExists(val, idx_dict):
    if val not in idx_dict:
        idx_dict[val] = len(idx_dict)
    return idx_dict[val]


def make_discrete_array(attr_name, dataset):
    attr_arr = []
    attr_vals = {}

    for p in dataset:
        attr_arr.append(getIdxIfExists(p.attr[attr_name], attr_vals))

    return array(attr_arr)


def make_bucket_array(attr_name, dataset, buckets):
    attr_arr = []

    for p in dataset:
        val = p.attr[attr_name]

        if val > buckets[-1]:
            attr_arr.append(len(buckets))
        else:
            for i in range(len(buckets)):
                if val < buckets[i]:
                    attr_arr.append(i)

        return array(attr_arr)


def make_even_buckets(attr_name, dataset, num_buckets):
    mini = None
    maxi = None

    for p in dataset:
        val = p.attr[attr_name]
        if mini is None or val < mini:
            mini = val
        if maxi is None or val > maxi:
            maxi = val

        if (min is not None and max is not None and max != min):
            bkt_size = (max - min) / (num_buckets - 1)
            return range(min + bkt_size, max, bkt_size)
        else:
            return []

if __name__ == "__main__":
    size_arr = make_discrete_array('screenSizeClassIn', Product.objects)
    bkts = make_even_buckets('regularPrice', Product.objects, 8)
    price_arr = make_bucket_array('regularPrice', Product.objects, bkts)

    print nmi(size_arr, price_arr)

    #Example from http://nlp.stanford.edu/IR-book
    #/html/htmledition/evaluation-of-clustering-1.html
    #print nmi(array([1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3])
    #          ,array([1,1,1,1,2,1,2,2,2,2,3,1,3,3,3,2,2]))
    
    
    