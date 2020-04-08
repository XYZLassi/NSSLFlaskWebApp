import flask

bp = flask.Blueprint('main', __name__)


@bp.route('/', methods=['GET'])
def index():
    return flask.render_template('main/index.html')
