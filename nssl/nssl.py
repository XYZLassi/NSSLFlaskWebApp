import json
from typing import Tuple

import requests

from .entites import LoginData


class NSSL:
    def __init__(self, url: str, token: str = None):
        assert url, 'Url must been set'
        self.base_url = url
        self.token = token

    def _post(self, url, payload: dict) -> dict:
        return self._request(url, payload, method='POST')

    def _request(self, url: str, payload: dict, method='GET',
                 headers: dict = None) -> dict:
        if not url.startswith(self.base_url):
            url = self.base_url + url

        if headers is None:
            headers = dict()

        headers['content-type'] = 'application/json; charset=utf-8'

        json_payload = json.dumps(payload)
        response = requests.request(method, url, data=json_payload, headers=headers)

        if response.ok:
            response_value = response.json()
            return response_value
        return dict()

    def login(self, username: str, password: str) -> Tuple[bool, str, LoginData]:
        value = {
            'Username': username,
            'PWHash': password,
        }
        data = self._post('/session', value)
        if data:
            login_data = LoginData(
                id=data['id'],
                username=data['username'],
                token=data['token']
            )

            self.token = login_data.token

            return data['success'], data['error'], login_data
        return False, 'Unknown Error', LoginData()
