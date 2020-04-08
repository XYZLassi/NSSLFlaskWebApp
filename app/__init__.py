import importlib
import os

from flask import Flask


def create_app(config=None):
    if config is None:
        module = importlib.import_module('config')
        app_settings = os.environ.get('APP_SETTINGS') or 'ProductionConfig'

        config = getattr(module, app_settings)

    app = Flask(__name__)
    app.config.from_object(config)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    return app
