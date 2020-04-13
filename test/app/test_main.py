from config import TestConfig
from flask.testing import FlaskClient


def test_login(config: TestConfig, base_client: FlaskClient):
    return base_client.post('/login', data=dict(
        username=config.TEST_USER,
        password=config.TEST_USER_PASSWORD
    ), follow_redirects=True)


def test_logout(client: FlaskClient):
    return client.get('/logout')
