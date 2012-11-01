#from parsing import ParsedProduct
#from numpy import array, log, e

import numpy
from numpy import *
from scipy import *
from parsing import ParsedProduct
from matplotlib import pyplot


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

    if Hx + Hy == 0:
        return 0
    return I / ((Hx + Hy) / 2)


def getIdxIfExists(val, idx_dict):
    if val not in idx_dict:
        idx_dict[val] = len(idx_dict)
    return idx_dict[val]


def make_discrete_array(attr_name, dataset):
    attr_arr = []
    attr_vals = {}

    for p in dataset:
        try:
            attr_arr.append(getIdxIfExists(p.attr[attr_name], attr_vals))
        except KeyError:
            print "Key error for " + p.attr

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
                    break

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

    if (mini is not None and maxi is not None and maxi != mini):
        bkt_size = (maxi - mini) / (num_buckets - 1)
        return arange(mini + bkt_size, maxi, bkt_size, dtype=float)
    else:
        return []


def filter_set_for_attrs(dataset, attr_list):
    out_arr = []

    for p in dataset:
        failed = False
        for atr in attr_list:
            if not atr in p.attr or p.attr[atr] is None:
                failed = True
                break

        if not failed:
            out_arr.append(p)

    return out_arr


if __name__ == "__main__":
    print 'ready'

    my_xvars = ('screenSizeClassIn', 'tvType', 'verticalResolution')
    #my_yvars = (('regularPrice', range(0, 10000, 100)), ('customerReviewAverage'))
    my_yvars = ('screenSizeClassIn', ('regularPrice', (156.25, 312.5, 625, 1250, 2500, 5000)), ('customerReviewAverage', (2.01, 3.01, 4.26, 4.51, 4.76)))

    #prods = []
    #for p in ParsedProduct.objects.all():
    #    prods.append(p)

    prods = ParsedProduct.objects.select_related()

    for xvar in my_xvars:
        for yvar in my_yvars:
            my_dataset = filter_set_for_attrs(prods, (xvar, yvar[0]))

            x_arr = make_discrete_array(xvar, my_dataset)
            y_arr = None

            if len(yvar) > 1:
                #bkts = make_even_buckets(yvar[0], my_dataset, yvar[1])
                y_arr = make_bucket_array(yvar[0], my_dataset, yvar[1])
                pass
            else:
                y_arr = make_discrete_array(yvar, my_dataset)

            if y_arr is None:
                print "y_arr is None"

            print "%s, %s: %f" % (xvar, yvar, nmi(x_arr, y_arr))
"""
    Example from http://nlp.stanford.edu/IR-book
    /html/htmledition/evaluation-of-clustering-1.html
    print nmi(array([1,1,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3])
              ,array([1,1,1,1,2,1,2,2,2,2,3,1,3,3,3,2,2]))
"""
