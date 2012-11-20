import json
from shoppersherpa import logging
from shoppersherpa.models.models import Product, AttrInfo
from shoppersherpa.analysis.calcstats import *
from filters import FilterMerger

#TODO: move logs to a centralized location, make log level configurable
logger = logging.getLogger(__name__)

#TODO: how do I deal with debug logging in doctests?


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

    # decode json
    # Product.objects.select_related()
    jsonQuery = parseJson(jsonString)

    # ensure we passed in keywords
    if 'keywords' not in jsonQuery:
        logger.error("No keywords in query json: %s", jsonQuery)
        raise ValueError("Expecting json with keywords attribute")

    # TODO: enable keywords - get a set of products based on the keywords
    # keywords = jsonQuery['keywords']
    products = Product.objects

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

    selected_attrs = ['size']
    if 'attributes' in jsonQuery:
        selected_attrs = jsonQuery['attributes']

    dep_attrs = ['price', 'ratings_avg']

    response_json = {'attrs': [],
                     'selectedAttrs': selected_attrs,
                     'rawData': [],
                     'topProducts': []}

    for ai in AttrInfo.objects.filter(**{'is_independant': True}):
        ai_json = {}
        response_json['attrs'].append(ai_json)
        ai_json['name'] = ai.name
        ai_json['displayName'] = ai.display_name
        ai_json['helpText'] = ai.help_text
        ai_json['rank'] = ai.rank
        ai_json['isDiscrete'] = ai.is_discrete
        ai_json['units'] = ai.units
        ai_json['options'] = []

        for val in ai.values:
            val_json = {}
            ai_json['options'].append(val_json)
            val_json['value'] = val
            val_json['count'] = attrValDepCount(ai.name, val, None, products)
            val_json['stats'] = []

            for dep in dep_attrs:
                filtered = docSetFilter(products, ai.name, val, dep)
                if len(filtered) == 0:
                    continue

                dep_json = {}
                val_json['stats'].append(dep_json)
                dep_json['name'] = dep
                dep_json['mean'] = docSetMean(filtered, dep)
                dep_json['median'] = docSetMedian(filtered, dep)
                dep_json['stdDev'] = docSetStd(filtered, dep)

    for prod in products:
        prod_json = {}
        response_json['rawData'].append(prod_json)
        for at in selected_attrs + dep_attrs:
            if at in prod.normalized:
                prod_json[at] = prod.normalized[at]

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
    return results[0]


if __name__ == "__main__":
    import doctest
    xxx = query('''{"keywords":"600Hz 1080p used Plasma HDTV",
    "attributes":["size"],
    "filters":[{"attribute":"brand",
                "type":"include",
                "value":["Sony","Toshiba"]},
               {"attribute":"size",
                "type":"range",
                "value":[6,null]}]}''')

    #doctest.testmod()
