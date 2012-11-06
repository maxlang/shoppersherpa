from bottle import route, run, jinja2_view as view
from shoppersherpa.models.models import Product

@route('/')
@view('index.html')
def index():
    return dict(products=Product.objects(attr__tvType="Projection"))


def start():
    run(host='localhost', port=8080, debug=True)
