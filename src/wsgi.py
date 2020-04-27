from app import create_app
from flask_behind_proxy import FlaskBehindProxy

app = create_app()
application = FlaskBehindProxy(app)
