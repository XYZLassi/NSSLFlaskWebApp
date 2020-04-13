from typing import Iterator, Type

import pytest
from app import create_app
from config import TestConfig
from flask.testing import FlaskClient
from nssl import NSSL


@pytest.fixture()
def config_type() -> Type[TestConfig]:
    return TestConfig


@pytest.fixture()
def config(config_type: Type[TestConfig]):
    return config_type()


@pytest.fixture()
def base_client(config_type: Type[TestConfig]) -> Iterator[FlaskClient]:
    application = create_app(config=config_type)
    with application.test_client(use_cookies=True) as client:
        yield client


@pytest.fixture()
def nssl(config: TestConfig):
    url = config.NSSL_SERVER_URL
    username = config.TEST_USER
    password = config.TEST_USER_PASSWORD

    nssl = NSSL(url)
    result = nssl.login(username, password)
    assert result.success, f'Cannot login for user "{username}"'

    return nssl


@pytest.fixture()
def client(config: TestConfig,
           nssl: NSSL,
           base_client: FlaskClient) -> \
        Iterator[FlaskClient]:
    def test_and_delete_list():
        result = nssl.get_shopping_lists(force=True)
        for shopping_list in result.data.lists:
            if shopping_list == config.TEST_SHOPPING_LIST_NAME:
                nssl.delete_list(shopping_list.id)

    test_and_delete_list()

    base_client.post('/login', data=dict(
        username=config.TEST_USER,
        password=config.TEST_USER_PASSWORD
    ), follow_redirects=True)

    yield base_client

    test_and_delete_list()
