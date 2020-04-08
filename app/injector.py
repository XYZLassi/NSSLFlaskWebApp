from functools import wraps

import flask
import flask_login
from nssl import NSSL

from .models.user import User


def nssl_inject(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        app = flask.current_app
        user: User = flask_login.current_user

        token = None

        if not user.is_anonymous:
            token = user.token

        nssl = NSSL(app.config['NSSL_SERVER_URL'], token=token)
        return func(nssl, *args, **kwargs)

    return wrapper
