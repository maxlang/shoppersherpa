from shoppersherpa.models.models import Product
import numpy
#from shoppersherpa.models import ParsedProduct


def convertToVector(doc_set, field):
    ls = []
    for prod in doc_set:
        if field in prod.normalized and prod.normalized[field] is not None:
            ls.append(prod.normalized[field])
    return numpy.array([ls])


def makeParamDict(indep = None, val = None, dep = None, min_ratings = None):
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


#returns a numpy array of a dependant attribute (like price, ratings avg) for a
#given independant attribute-value pair (e.g. tvType='LED Flat-Screen')
def getArrayForAttrVal(indep, val, dep, min_ratings = None):
    param_dict = makeParamDict(indep, val, dep, min_ratings)
    arr = convertToVector(Product.objects(**param_dict), dep)
    return arr


def attrValMedian(indep, val, dep, min_ratings = None):
    return numpy.median(getArrayForAttrVal(indep, val, dep, min_ratings))


def attrValStd(indep, val, dep, min_ratings = None):
    return numpy.std(getArrayForAttrVal(indep, val, dep, min_ratings))


def attrValVar(indep, val, dep, min_ratings=None):
    return numpy.var(getArrayForAttrVal(indep, val, dep, min_ratings))


def attrValMean(indep, val, dep, min_ratings=None):
    return numpy.mean(getArrayForAttrVal(indep, val, dep, min_ratings))


def docSetMedian(doc_set, dep):
    return numpy.median(convertToVector(doc_set, dep))


def docSetStd(doc_set, dep):
    return numpy.std(convertToVector(doc_set, dep))


def docSetVar(doc_set, dep):
    return numpy.var(convertToVector(doc_set, dep))


def docSetMean(doc_set, dep):
    return numpy.mean(convertToVector(doc_set, dep))


def attrValDepCount(indep, val=None, dep=None, min_ratings=None):
    pd = makeParamDict(indep, val, dep, min_ratings)
    return Product.objects(**pd).count()


def hasDepCount(dep, min_ratings=None):
    pd = makeParamDict(None, None, dep, min_ratings)
    return Product.objects(**pd).count()


if __name__ == "__main__":
    attrValMean('tv_type', 'Projection', 'price')
