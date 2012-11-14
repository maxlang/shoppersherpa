import json
import logging
import shoppersherpa

#TODO: move logs to a centralized location, make log level configurable
logger = logging.getLogger(__name__)


def decodeJson(jsonString):
    """ Decodes a json String and logs an error on failure.

    -----------------------------------------
    EXAMPLES:
    -----------------------------------------

    >>> decodeJson('{"keyword":"television"}')
    {u'keyword': u'television'}
    >>> decodeJson('')
    Traceback (most recent call last):
        ...
    ValueError: No JSON object could be decoded
    >>> decodeJson('{}')
    {}
    >>> decodeJson('this is not json')
    Traceback (most recent call last):
        ...
    ValueError: No JSON object could be decoded
    >>> decodeJson('{"keywords":"600Hz 1080p used Plasma HDTV","filters":[{"attribute":"brand","filterType":"include","filterValue":["Sony","Toshiba"]},{"attribute":"size","filterType":"range","filterValue":[30,6]}]}')
    {u'keywords': u'600Hz 1080p used Plasma HDTV', u'filters': [{u'attribute': u'brand', u'filterValue': [u'Sony', u'Toshiba'], u'filterType': u'include'}, {u'attribute': u'size', u'filterValue': [30, 6], u'filterType': u'range'}]}

    -----------------------------------------
    NOTE: All json strings use double quotes, even for the attributes.
    -----------------------------------------

    >>> decodeJson('{keywords:"television"}')
    Traceback (most recent call last):
    ...
    ValueError: Expecting property name: line 1 column 1 (char 1)

    -----------------------------------------
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
        - filters: (Optional) The filters to use to filter the results

    Filters in turn have the following format:
        - attribute: the attribute name to filter on
        - type: the type of filter, one of 'include', 'exclude' or 'range'
        - value: a list of values to include/exclude
                 or a two element list representing a min/max range
        NOTE: the min or the max value may be null

    Example:

    {keywords:"600Hz 1080p used Plasma HDTV",
     filters:[{attribute:"brand",type:"include",value:["Sony","Toshiba"]},
              {attribute:"size",type:"range",value:[6,null]}]}

    """

    # decode json
    jsonQuery = decodeJson(jsonString)

    # ensure we passed in keywords
    if 'keywords' not in jsonQuery:
        logger.error("No keywords in query json: %s",jsonQuery)
        raise ValueError("Expecting json with keywords attribute")

    keywords = jsonQuery['keywords']

    if 'filters' in jsonQuery:
        pass
    else:
        logger.info("No filters in query json: %s", jsonQuery)

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)