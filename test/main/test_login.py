from flask.testing import FlaskClient


def test_login(client: FlaskClient):
    username = client.application.config['TEST_USER']
    password = client.application.config['TEST_USER_PASSWORD']
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def test_logout(nssl_client: FlaskClient):
    return nssl_client.get('/logout')
