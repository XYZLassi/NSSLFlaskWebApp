import flask
from nssl import NSSL

from ..injector import nssl_inject

bp = flask.Blueprint("shoppinglist", __name__, url_prefix='/shoppingList')


@bp.route('/', methods=['GET'])
@nssl_inject
def index(nssl: NSSL):
    return flask.render_template('shopping_list/index.html')
