from shoppersherpa.models.models import Product
import numpy
#from shoppersherpa.models import ParsedProduct

'''
def convertToVector(doc_set, field):
    ls = []
    for prod in doc_set:
        if field in prod.normalized and prod.normalized[field] is not None:
            ls.append(prod.normalized[field])
    return numpy.array([ls])
'''
'''
def makeParamDict(indep=None, val=None, dep=None, min_ratings=None):
    param_dict = {}
    if indep is not None:
        if val is None:
            param_dict["normalized.{0}".format(indep)] = {'$exists': True, '$ne': None}
        else:
            param_dict["normalized.{0}".format(indep)] = val

    if dep is not None:
        param_dict["normalized.{0}".format(dep)] = {'$exists': True, '$ne': None}
        if min_ratings is not None:
            param_dict['normalized.ratings_num'] = {'ratings_num': {'$gte': min_ratings} }

    return param_dict
'''

#returns a numpy array of a dependant attribute (like price, ratings avg) for a
#given independant attribute-value pair (e.g. tvType='LED Flat-Screen')
'''
def getArrayForAttrVal(indep, val, dep, doc_set=None, min_ratings=None):
    if doc_set is None:
        doc_set = Product.objects
    param_dict = makeParamDict(indep, val, dep, min_ratings)
    arr = convertToVector(doc_set.filter(**param_dict), dep)
    return arr
'''


def docSetFilter(doc_set, indep=None, val=None, dep=None):
    cur = doc_set
    if doc_set is None:
        cur = Product.objects

    if indep is not None:
        if val is not None:
            cur = [x for x in cur if x.normalized[indep] == val]
        else:
            cur = [x for x in cur if indep in x.normalized and x.normalized[indep] is not None]
    if dep is not None:
        cur = [x for x in cur if dep in x.normalized and x.normalized[dep] is not None]

    return cur


def docSetToVector(doc_set, indep, val, dep):
    arr = docSetFilter(doc_set, indep, val, dep)
    return numpy.array([x.normalized[dep] for x in arr])


def attrValMedian(indep, val, dep, doc_set=None, min_ratings=None):
    return numpy.median(docSetToVector(doc_set, indep, val, dep))


def attrValStd(indep, val, dep, doc_set=None, min_ratings=None):
    return numpy.std(docSetToVector(doc_set, indep, val, dep))


def attrValVar(indep, val, dep, doc_set=None, min_ratings=None):
    return numpy.var(docSetToVector(doc_set, indep, val, dep))


def attrValMean(indep, val, dep, doc_set=None, min_ratings=None):
    return numpy.mean(docSetToVector(doc_set, indep, val, dep))


def docSetMedian(doc_set, dep):
    return numpy.median(docSetToVector(doc_set, None, None, dep))


def docSetStd(doc_set, dep):
    return numpy.std(docSetToVector(doc_set, None, None, dep))


def docSetVar(doc_set, dep):
    return numpy.var(docSetToVector(doc_set, None, None, dep))


def docSetMean(doc_set, dep):
    return numpy.mean(docSetToVector(doc_set, None, None, dep))


def attrValDepCount(indep, val=None, dep=None, doc_set=None):
    len(docSetFilter(doc_set, indep, val, dep))


if __name__ == "__main__":
    attrValMean('tv_type', 'Projection', 'price')
