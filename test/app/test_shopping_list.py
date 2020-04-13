import pytest
from config import TestConfig
from flask.testing import FlaskClient
from nssl import NSSL


def test_index_shopping_list(client: FlaskClient):
    result = client.get('/shoppingList', follow_redirects=True)
    return result


def test_create_shopping_list(config: TestConfig, client: FlaskClient):
    result = client.post('/shoppingList',
                         data=dict(
                             name=config.TEST_SHOPPING_LIST_NAME,
                         ),
                         follow_redirects=True)
    assert config.TEST_SHOPPING_LIST_NAME in result.data.decode('utf-8')


def test_show_shopping_list(config: TestConfig,
                            nssl: NSSL,
                            client: FlaskClient):
    list_response = nssl.add_list(config.TEST_SHOPPING_LIST_NAME)
    assert list_response.success
    shopping_list = list_response.data

    return client.get(f'/shoppingList/{shopping_list.id}')


def test_delete_shopping_list(config: TestConfig,
                            nssl: NSSL,
                            client: FlaskClient):
    list_response = nssl.add_list(config.TEST_SHOPPING_LIST_NAME)
    assert list_response.success
    shopping_list = list_response.data

    return client.get(f'/shoppingList/delete/{shopping_list.id}')
