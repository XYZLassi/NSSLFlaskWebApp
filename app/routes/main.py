import flask
import flask_login
from nssl import NSSL

bp = flask.Blueprint('main', __name__)


@bp.route('/', methods=['GET'])
def index():
    return flask.render_template('main/index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    from ..models.user import User
    from ..forms.user import LoginForm
    from ..context import UserStorage

    form = LoginForm()
    if form.validate_on_submit():
        app = flask.current_app
        nssl = NSSL(app.config['NSSL_SERVER_URL'])
        success, error, login_data = nssl.login(form.username.data, form.password.data)
        if success:
            user = User(login_data=login_data)
            UserStorage.add(user.user_id, user)

            flask_login.login_user(user)

            return flask.redirect(flask.url_for('main.index'))

        flask.flash(error)

    return flask.render_template('main/login.html', title='Login', form=form)


@bp.route('/logout', methods=['GET'])
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('main.index'))
