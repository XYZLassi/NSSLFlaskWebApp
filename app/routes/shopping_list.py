import flask
import flask_login
from nssl import NSSL

from ..injector import nssl_inject

bp = flask.Blueprint("shoppinglist", __name__, url_prefix='/shoppingList')


@bp.route('/', methods=['GET'])
@flask_login.login_required
@nssl_inject
def index(nssl: NSSL):
    response = nssl.get_shopping_lists()
    if not response.success:
        flask.flash(response.error)

    return flask.render_template('shopping_list/index.html',
                                 title='Shopping Lists',
                                 shopping_lists=response.data.lists)
