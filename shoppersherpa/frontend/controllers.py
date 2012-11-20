from util import form2json
from shoppersherpa.api.api import query
from shoppersherpa import logging
from bottle import (request, get, post, run, jinja2_view as view, static_file,
                    TEMPLATE_PATH, BaseTemplate)
from config import config


# get logger
logger = logging.getLogger(__name__)

# bottle setup
TEMPLATE_PATH.append(config['viewDir'])
logger.debug("added view dir")

# add view extension (jinja 2 files)
BaseTemplate.extensions.append("jinja")
logger.debug("added jinja file extention")

### CONTROLLERS ###


# static files
@get('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=config['staticdir'])


# home page
@get('/')
@view('index.html')
def index():
    return dict()


# keyword search from home page
@post('/search')
#   @view('search.html')
def search():
    return query(form2json(request.forms))


### RUN ###


# code to start test server
def start():
    run(host='localhost', port=8080, debug=True)

if __name__ == "__main__":
    start()