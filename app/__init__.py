import importlib
import os

from flask import Flask

from flask_login import LoginManager

login = LoginManager()


def create_app(config=None, load_views=None):
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

    load_views = app.config['LOAD_VIEWS'] if load_views is None else load_views
    if load_views:
        from .routes.main import bp as bp_main
        app.register_blueprint(bp_main)

        from .routes.shopping_list import bp as bp_shopping_list
        app.register_blueprint(bp_shopping_list)

    return app


@login.user_loader
def user_loader(user_id):
    from .context import UserStorage
    return UserStorage.get(int(user_id))
