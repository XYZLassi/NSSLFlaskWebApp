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
