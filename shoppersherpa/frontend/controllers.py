from util import form2json
from shoppersherpa.api.api import query
from shoppersherpa import logging
from bottle import (request, get, post, run, jinja2_view as view, static_file,
                    TEMPLATE_PATH, BaseTemplate)
from config import Config
from jinjaSetup import jinjaSetup

### CONFIG ###
global config
config = Config()

# get logger
logger = logging.getLogger(__name__)

# bottle setup
TEMPLATE_PATH.append(config['viewDir'])
logger.debug("added view dir")

# add view extension (jinja 2 files)
BaseTemplate.extensions.append("jinja")
logger.debug("added jinja file extention")

# adde custom jinja functions/filters
jinjaSetup()

### CONTROLLERS ###


# static files
@get('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=config['staticDir'])


# home page
@get('/')
@view('index.html')
def index():
    return dict()


# keyword search from home page
@post('/search')
@view('search.html')
def search():
    jsonQuery = form2json(request.forms)
    """
    jsonQuery = '''{"keywords":"600Hz 1080p used Plasma HDTV",
    "attributes":["size_class", "refresh"],
    "filters":[{"attribute":"brand",
                "type":"include",
                "value":["Sony","Toshiba"]},
               {"attribute":"size_class",
                "type":"range",
                "value":[6,null]}]}'''
    """
    queryResult = query(jsonQuery)

    #return the form input and the query result
    return dict(list(queryResult.items()) +
                list(request.forms.items()))

### RUN ###

# code to start test server
def start(reload=False):
    #TODO - there ought to be a better way to do this than using globals
    # perhaps using app.config or bottle.config or something
    global config
    config = Config(debug=True)
    run(host='localhost', port=8080, debug=True,reloader=reload)

if __name__ == "__main__":
    start()