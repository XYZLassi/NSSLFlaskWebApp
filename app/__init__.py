import importlib
import os
from functools import lru_cache

from flask import Flask
from flask_login import LoginManager

login = LoginManager()


def create_app(config=None, load_views=None) -> Flask:
    if config is None:
        module = importlib.import_module('config')
        app_settings = os.environ.get('APP_SETTINGS') or 'ProductionConfig'

        config = getattr(module, app_settings)

    app = Flask(__name__)
    app.config.from_object(config)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    login.init_app(app)
    login.login_view = "main.login"

    # AutoLogin for Debug
    if app.config['DEBUG'] and app.config['TEST_AUTO_LOGIN']:
        @lru_cache()
        def get_default_user():
            from nssl import NSSL
            from .models.user import User
            from .context import UserStorage

            nssl = NSSL(app.config['NSSL_SERVER_URL'])
            response = nssl.login(app.config['AUTO_LOGIN_USER'],
                                  app.config['AUTO_LOGIN_PASSWORD'])
            user = User(user_data=response.data)
            UserStorage.add(user.user_id, user)
            return user

        login.anonymous_user = get_default_user

    load_views = app.config['LOAD_VIEWS'] if load_views is None else load_views
    if load_views:
        from .filters import bp as bp_filters
        app.register_blueprint(bp_filters)

        from .routes.main import bp as bp_main
        app.register_blueprint(bp_main)

        from .routes.shopping_list import bp as bp_shopping_list
        app.register_blueprint(bp_shopping_list)

    return app


@login.user_loader
def user_loader(user_id):
    from .context import UserStorage
    return UserStorage.get(int(user_id))
