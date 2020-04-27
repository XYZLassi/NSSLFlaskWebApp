from app import create_app
from flask_behind_proxy import FlaskBehindProxy

application = create_app()
proxied = FlaskBehindProxy(application)
