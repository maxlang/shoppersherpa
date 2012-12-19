from util import form2json
from shoppersherpa.api.api import query
from shoppersherpa import logging
from bottle import (request, get, post, route,
                    run, jinja2_view as view, static_file,
                    TEMPLATE_PATH, BaseTemplate, default_app)
from config import Config
from jinjaSetup import jinjaSetup
from cork import Cork
from beaker.middleware import SessionMiddleware

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

#cork setup

aaa = Cork(config['corkConfigDir'])

### CONTROLLERS ###


# static files
@get('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=config['staticDir'])


# home page
@get('/')
@view('index.html')
def index():
    aaa.require(fail_redirect='/login')
    return dict()


# keyword search from home page
@post('/search')
@view('search.html')
def search():
    aaa.require(fail_redirect='/login')
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

### CORK ROUTES ###

#logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

# Use users.json and roles.json in the local example_conf directory
aaa = Cork(config['corkConfigDir'])

app = default_app()
session_opts = {
    'session.type': 'cookie',
    'session.validate_key': True,
    'session.cookie_expires': True,
    'session.timeout': 3600 * 24, # 1 day
    'session.encrypt_key': 'please use a random key and keep it secret!',
}
app = SessionMiddleware(app, session_opts)

# #  Bottle methods  # #

def postd():
    return request.forms

def post_get(name, default=''):
    return request.POST.get(name, default).strip()

@post('/login')
def login():
    """Authenticate users"""
    username = post_get('username')
    password = post_get('password')
    aaa.login(username, password, success_redirect='/', fail_redirect='/login')


@route('/logout')
def logout():
    aaa.logout(success_redirect='/login')



@route('/auth')
def auth():
    """Only authenticated users can see this"""
    aaa.require(fail_redirect='/login')
    return 'Welcome! <a href="/admin">Admin page</a> <a href="/logout">Logout</a>'

# Static pages

@route('/login')
@view('login_form')
def login_form():
    """Serve login form"""
    return {}

@route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    return '<p>Sorry, you are not authorized to perform this action</p>'


### CONFIG CORK ###
session_opts = {
        'session.type': 'cookie',
        'session.validate_key': True,
    }

# Setup Beaker middleware to handle sessions and cookies
app = default_app()
app = SessionMiddleware(app, session_opts)

### RUN ###

# code to start test server
def start(reload=False):
    #TODO - there ought to be a better way to do this than using globals
    # perhaps using app.config or bottle.config or something
    global config
    config = Config(debug=True)
    run(app=app, host='localhost', port=8080, debug=True, reloader=reload)

if __name__ == "__main__":
    start()