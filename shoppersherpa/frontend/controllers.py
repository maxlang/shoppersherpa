import os

from json import dumps
from shoppersherpa.api.api import query
from shoppersherpa import logging
from bottle import (request, get, post, run, jinja2_view as view,static_file,
                    BaseTemplate, TEMPLATE_PATH)

logger = logging.getLogger(__name__)

# set up view directory
curdir = os.path.dirname(os.path.realpath(__file__))
logger.debug("frontend dir: %s",curdir)
viewdirname = "views"
viewdir = os.path.join(curdir, viewdirname)
logger.debug("view dir: %s",viewdir)
TEMPLATE_PATH.append(viewdir)
logger.debug("added view dir")
staticdirname = "static"
staticdir = os.path.join(curdir, staticdirname)
logger.debug("view dir: %s",staticdir)


# add view extension (jinja 2 files)
BaseTemplate.extensions.append("jinja")
logger.debug("added jinja extention")

# static files
@get('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=staticdir)

# home page
@get('/')
@view('index.html')
def index():
    return dict()

# keyword search
@post('/search')
#   @view('search.html')
def search():
    q = request.forms.get('q')
    return query(dumps({'keywords':q}))


def start():
    run(host='localhost', port=8080, debug=True)

if __name__ == "__main__":
    start()
