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

        user_id = None

        if not user.is_anonymous:
            user_id = user.user_id

        nssl = NSSL(app.config['NSSL_SERVER_URL'], user_id=user_id)
        return func(nssl, *args, **kwargs)

    return wrapper
