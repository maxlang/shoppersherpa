import json
from shoppersherpa import logging
from shoppersherpa.models.models import AttrInfo
from shoppersherpa.analysis.calcstats import *
from filters import FilterMerger

#TODO: move logs to a centralized location, make log level configurable
logger = logging.getLogger(__name__)

#TODO: how do I deal with debug logging in doctests?


def getSingleProductJson(prod, attrs, include_name=False, include_image=False, include_url=True):
    json = {}
    if attrs is None:
        attrs = prod.normalized.keys()

    json['id'] = str(prod.id)
    for at in attrs:
        if at in prod.normalized:
            json[at] = prod.normalized[at]

    if include_image:
        json['imgSrc'] = prod.attr['image']

    if include_name:
        json['name'] = prod.attr['name']

    if include_url:
        #logger.debug(prod.attr)
        json['url'] = prod.attr['url']

    return json


#arguments --
#id: String -- id of product to return
#attrs: list of Strings -- attributes that should be returned (optional include all normalized if omitted)
#image: boolean -- include image URL if true
#name: boolean -- include product name if true
def querySingleProduct(**kwargs):
    if 'id' in kwargs:
        id = kwargs['id']
        prod = Product.objects.with_id(kwargs['id'])

        img = False
        name = False
        if 'image' in kwargs:
            img = kwargs['image']
        if 'name' in kwargs:
            name = kwargs['name']
        if 'url' in kwargs:
            url = kwargs['url']

        if prod is not None:
            attrs = None
            if 'attrs' in kwargs:
                attrs = kwargs['attrs']

            return getSingleProductJson(prod, attrs, name, img, url)

    return None


def parseJson(jsonString):
    """ Parses a json String and logs an error on failure.

    -----------------------------------------
    EXAMPLES:
    -----------------------------------------

    >>> parseJson('{"key":"value","array":[1,2,3]}')
    {u'array': [1, 2, 3], u'key': u'value'}

    # All json strings use double quotes, even for the attributes.
    >>> parseJson("{'key':'value'}")
    Traceback (most recent call last):
    ...
    ValueError: Expecting property name: line 1 column 1 (char 1)

    # The empty string is not valid json, but the empty object is.
    >>> parseJson('')
    Traceback (most recent call last):
        ...
    ValueError: No JSON object could be decoded
    >>> parseJson('{}')
    {}

    """

    try:
        jsonQuery = json.loads(jsonString)
    except ValueError:
        #couldn't decode json
        logger.error("Couldn't decode json: {0}".format(jsonString))
        raise
    return jsonQuery


def argmax(iterable, func, mult=1):
    best = None
    best_val = None
    for x in iterable:
        val = mult * func(x)
        if best is None or val > best_val:
            best_val = val
            best = x
    return best


def argmaxTake(iterable, feature, num, mult=1):
    result = []
    for x in iterable:
        pos = 0
        while pos < len(result) and pos < num and result[pos].normalized[feature] < x.normalized[feature]:
            pos = pos + 1
        if pos < num:
            result.insert(pos, x)
    if len(result) <= num:
        return result
    else:
        return result[:num]


def getTopProducts(doc_set, feature, dep_feature, num_products):
    ai = AttrInfo.lookup(feature)
    if ai is None:
        raise Exception("unknown feature: {0}".format(feature))

    mult = 1
    if ai.name == "price":
        mult = -1

    if not ai.is_discrete:
        buckets = bucketByPercentile(doc_set, feature, num_products)
        return filter(lambda x: x is not None,
                      [argmax(b, lambda x: x.normalized[dep_feature], mult) for b in buckets])

    else:
        bucketed = [filter(lambda x: x.normalized[feature] == v, doc_set) for v in ai.values]
        prods = [argmax(b, lambda x: x.normalized[dep_feature], mult) for b in bucketed]

        prods = filter(lambda x: x is not None, prods)
        return argmaxTake(prods, dep_feature, num_products, mult)


"""
expects json in the following format:

"""
def query(jsonString):
    """ Parses a parses a json query and returns a json response.

    The json query has the following attributes:
        - keywords: The string of keywords to use to search the database
        - attributes: (Optional) the list of attributes being compared
                      This will effect which attributes are returned for most
                      products (not the top products).
        - filters: (Optional) The filters to use to filter the results

    Filters in turn have the following format:
        - attribute: the attribute name to filter on
        - type: the type of filter, one of 'include', 'exclude' or 'range'
        - value: a list of values to include/exclude
                 or a two element list representing a min/max range
        NOTE: the min or the max value may be null

    Example input:

    '{"keywords":"600Hz 1080p used Plasma HDTV",\
    "attributes":["size"],\
    "filters":[{"attribute":"brand",\
                "type":"include",\
                "value":["Sony","Toshiba"]},\
               {"attribute":"size",\
                "type":"range",\
                "value":[6,null]}]}'

    """

    logger.debug(jsonString)

    # decode json
    # Product.objects.select_related()
    jsonQuery = parseJson(jsonString)

    # ensure we passed in keywords
    if 'keywords' not in jsonQuery:
        logger.error("No keywords in query json: %s", jsonQuery)
        raise ValueError("Expecting json with keywords attribute")

    # TODO: enable keywords - get a set of products based on the keywords
    # keywords = jsonQuery['keywords']
    products = Product.objects.only("normalized", "attr.name", "attr.image", "attr.url")
    #products = Product.objects

    # TODO: should this stuff happen in the API? Or in helper functions?
    if 'filters' in jsonQuery:
        merger = FilterMerger()

        for f in jsonQuery['filters']:
            merger.add(f)

        # filter the products based on the filters
        d = merger.merge()
        products = products.filter(**d)
    else:
        logger.info("No filters in query json: %s", jsonQuery)

    products = [p for p in products]

    selected_attrs = ['size_class']
    if 'attributes' in jsonQuery:
        selected_attrs = jsonQuery['attributes']

    dep_attrs = ['price', 'ratings_avg']

    all_relevant_attrs = selected_attrs + dep_attrs

    #TODO: populate absolute stats automatically
    response_json = {'attrs': {},
                     'selectedAttrs': selected_attrs,
                     'rawData': [],
                     'topProducts': [],
                     'absoluteStats': {'priceMax': 9999.98,
                                      'priceMin': 69.99,
                                      'priceRange': 9999.98 - 69.99,
                                      'sizeMax': 92,
                                      'sizeMin': 8,
                                      'sizeRange': 92 - 8}}

    for ai in AttrInfo.objects.filter(**{'is_independant': True}):
        all_relevant_attrs.append(ai.name)
        if ai.rank < 0:
            continue

        ai_json = {}
        response_json['attrs'][ai.name] = ai_json
        ai_json['name'] = ai.name
        ai_json['displayName'] = ai.display_name
        ai_json['helpText'] = ai.help_text
        ai_json['rank'] = ai.rank
        ai_json['isDiscrete'] = ai.is_discrete
        ai_json['units'] = ai.units
        ai_json['options'] = []

        for val in ai.values:
            val_filtered = docSetFilter(products, ai.name, val, None)
            if len(val_filtered) == 0:
                val_json = {}
                ai_json['options'].append(val_json)
                val_json['value'] = val
                val_json['count'] = 0
                val_json['stats'] = {}
            else:
                val_json = {}
                ai_json['options'].append(val_json)
                val_json['value'] = val
                val_json['count'] = len(val_filtered)
                val_json['stats'] = {}

                for dep in dep_attrs + selected_attrs:
                    dep_filtered = docSetFilter(val_filtered, None, None, dep)
                    if len(dep_filtered) == 0:
                        continue

                    vector = docSetToVector(val_filtered, None, None, dep)

                    dep_json = {}
                    val_json['stats'][dep] = dep_json
                    dep_json['name'] = dep
                    dep_json['mean'] = numpy.mean(vector)
                    dep_json['median'] = numpy.median(vector)
                    dep_json['stdDev'] = numpy.std(vector)
                    dep_json['min'] = numpy.min(vector)
                    dep_json['max'] = numpy.max(vector)

    for prod in products:
        prod_json = getSingleProductJson(prod, all_relevant_attrs)
        response_json['rawData'].append(prod_json)

    if len(selected_attrs) > 0:
        response_json['topProducts'] = [getSingleProductJson(p, None, True, True,True)
                                        for p in getTopProducts(products, selected_attrs[0], 'price', 5)]

        #response_json['topProducts'] = \
        #[dict(p.normalized.copy(), id=str(p.id), imgSrc=p.attr['image'], name=p.attr['name'])
        # for p in getTopProducts(products, selected_attrs[0], 'price', 5)]

    print "done"
    return response_json


"""
    # get attribute data
        attributeData = []

    # get selected attributes
        selectedAttributes = []

    # get raw product data
        productData = []

    # get top products
        exampleProducts = []

    # combine
        result = {}
        result['attributes'] = attributeData
        result['selected'] = selectedAttributes
        result['products'] = productData
        result['examples'] = exampleProducts
    return result
"""


# get info on a single product
def product(jsonString):
    # decode json
    jsonQuery = parseJson(jsonString)
    results = Product.objects.filter(**jsonQuery)
    if len(results) == 0:
        return None
    return {'product':getSingleProductJson(results[0], None, True, True,True),'units':dict([(a.name,a.units) for a in AttrInfo.objects])}


if __name__ == "__main__":
    import doctest

    zzz = querySingleProduct(id='50cbf6527e59cb27d866bd62', image=True)
    mmm = querySingleProduct(id='50cbf6527e59cb27d866bd62', attrs=('size_class', 'refresh'))

    xxx = query('''{"keywords":"600Hz 1080p used Plasma HDTV",
    "attributes":["size_class", "refresh"],
    "filters":[{"attribute":"brand",
                "type":"include",
                "value":["Sony","Toshiba"]},
               {"attribute":"size_class",
                "type":"range",
                "value":[6,null]}]}''')
    yyy = query('''{"keywords":"televisions"}''')
    #xxx = query('{"keywords":"600Hz 1080p used Plasma HDTV"}')
    pass
    #doctest.testmod()
