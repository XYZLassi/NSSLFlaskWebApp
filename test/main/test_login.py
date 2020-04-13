from flask.testing import FlaskClient


def test_login(client: FlaskClient):
    return


def test_logout(client: FlaskClient):
    return client.get('/logout')
