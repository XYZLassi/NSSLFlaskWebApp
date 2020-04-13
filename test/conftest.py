from typing import Iterator

import pytest
from app import create_app
from config import TestConfig
from flask.testing import FlaskClient


@pytest.fixture()
def client() -> Iterator[FlaskClient]:
    application = create_app(config=TestConfig)
    with application.test_client() as client:
        yield client


@pytest.fixture()
def nssl_client(client: FlaskClient) -> FlaskClient:
    username = client.application.config['TEST_USER']
    password = client.application.config['TEST_USER_PASSWORD']

    client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

    return client
