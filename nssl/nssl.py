import json
from typing import Optional

import requests
from dacite import from_dict

from .entites import ShoppingListCollection, UserData
from .response_data import ResponseData


class NSSL:
    def __init__(self, url: str, token: str = None):
        assert url, 'Url must been set'
        self.base_url = url
        self.token = token

    def _post(self, url, payload: dict) -> dict:
        return self._request(url, payload, method='POST')

    def _get(self, url, payload: dict = None) -> dict:
        return self._request(url, payload)

    def _request(self, url: str, payload: dict = None, method='GET',
                 headers: dict = None) -> dict:
        if not url.startswith(self.base_url):
            url = self.base_url + url

        if headers is None:
            headers = dict()

        headers['content-type'] = 'application/json; charset=utf-8'
        if self.token:
            headers['X-Token'] = self.token

        json_payload = json.dumps(payload)
        response = requests.request(method, url, data=json_payload, headers=headers)

        success = False
        error = response.status_code
        data: Optional[dict] = None

        if response.ok:
            data = response.json()
            success = data.pop('success') if 'success' in data else True
            error = data.pop('error') if 'error' in data else ''

        return {
            'success': success,
            'error': error,
            'data': data
        }

    def login(self, username: str, password: str) -> ResponseData[UserData]:
        payload = {
            'Username': username,
            'PWHash': password,
        }
        result_dict = self._post('/session', payload)
        result_data = from_dict(UserData, result_dict['data']) \
            if result_dict['success'] else UserData()

        result: ResponseData[UserData] = ResponseData[UserData](
            success=result_dict['success'],
            error=result_dict['error'],
            data=result_data
        )

        if result.success:
            self.token = result_data.token

        return result

    def get_shopping_lists(self) -> ResponseData[ShoppingListCollection]:
        result_dict = self._get('/shoppinglists')

        result_data = from_dict(ShoppingListCollection, result_dict['data']) \
            if result_dict['success'] else ShoppingListCollection()

        result: ResponseData[ShoppingListCollection] = \
            ResponseData[ShoppingListCollection](
                success=result_dict['success'],
                error=result_dict['error'],
                data=result_data
            )

        return result
