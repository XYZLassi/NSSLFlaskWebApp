import flask

bp = flask.Blueprint('main', __name__)


@bp.route('/', methods=['GET'])
def index():
    return flask.render_template('main/index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    from ..forms.user import LoginForm

    form = LoginForm()
    if form.validate_on_submit():
        return flask.redirect(flask.url_for('main.index'))

    return flask.render_template('main/login.html', title='Login', form=form)
