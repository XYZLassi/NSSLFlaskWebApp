import pytest
from config import TestConfig
from flask.testing import FlaskClient


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
