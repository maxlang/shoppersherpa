import json
import logging

#TODO: move logs to a centralized location, make log level configurable
logging.basicConfig(filename='api.log',level=logging.DEBUG)

"""
expects json in the following format:
    {keywords:"600Hz 1080p used Plasma HDTV",
     filters:[{attribute:"brand",filterType:"include",filterValue:["Sony","Toshiba"]},
              {attribute:"size",filterType:"range",filterValue:[30,6]}]}
"""


def query(keywords=None,filters=None,jsonString=None):
    if jsonString and (filters or keywords):
        logging.warn("Couldn't decode json: " + jsonString)

    if jsonString:
        try:
            jsonQuery = json.loads(jsonString)
        except ValueError:
            #couldn't decode json
            logging.warn("Couldn't decode json: " + jsonString)
