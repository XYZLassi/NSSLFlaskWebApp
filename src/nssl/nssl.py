import json
from typing import List, Optional

import dataclasses
import requests
from base import RamStorage
from dacite import from_dict

from .entites import ShoppingListCollection, ShoppingListData, UserData
from .response_data import BaseResponseData, ResponseData

UserCash: RamStorage[UserData] = RamStorage[UserData]()
ShoppingListCash: RamStorage[ShoppingListData] = RamStorage[ShoppingListData]()


class NSSL:
    def __init__(self, url: str, user_id: int = None, token: str = None):
        assert url, 'Url must been set'
        self.base_url = url
        self.user_id = user_id
        self.token = ''

        if token:
            self.token = token
        elif user := UserCash.get(user_id):
            self.token = user.token

    def _post(self, url, payload: dict) -> dict:
        return self._request(url, payload, method='POST')

    def _put(self, url, payload: dict) -> dict:
        return self._request(url, payload, method='PUT')

    def _get(self, url, payload: dict = None) -> dict:
        return self._request(url, payload)

    def _delete(self, url, payload: dict = None) -> dict:
        return self._request(url, payload, method='DELETE')

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
        try:
            result_dict = self._post('/session', payload)
            result_data = from_dict(UserData, result_dict['data']) \
                if result_dict['success'] else UserData()

            result: ResponseData[UserData] = ResponseData[UserData](
                success=result_dict['success'],
                error=result_dict['error'],
                data=result_data
            )
        except Exception as ex:
            # Todo: Logging
            return ResponseData[UserData](
                success=False,
                error='API Error',
                data=None
            )

        if result.success:
            self.token = result_data.token
            self.user_id = result_data.id
            UserCash.add(result_data.id, result_data)

        return result

    def add_list(self, name: str) -> ResponseData[ShoppingListData]:
        args = {
            'Name': name,
        }
        try:
            result_dict = self._post('/shoppinglists', args)
            result_data = from_dict(ShoppingListData, result_dict['data'])

            result_data = dataclasses.replace(result_data, is_admin=True)

            return ResponseData(
                success=result_dict['success'],
                error=result_dict['error'],
                data=result_data,
            )
        except Exception as ex:
            # Todo: Logging
            return ResponseData(
                success=False,
                error='API Error',
                data=None,
            )

    def rename_list(self, list_id: int, new_name: str) \
            -> ResponseData[ShoppingListData]:
        args = {
            'Name': new_name,
        }

        data: Optional[ShoppingListData] = None

        try:
            result_dict = self._put(f'/shoppinglists/{list_id}', args)
            if result_dict['success'] and (data := ShoppingListCash.get(list_id)):
                data = dataclasses.replace(data, name=new_name)
                ShoppingListCash.add(list_id, data)

            return ResponseData(
                success=result_dict['success'],
                error=result_dict['error'],
                data=data
            )
        except Exception as ex:
            # Todo: Logging
            return ResponseData(
                success=False,
                error='API Error',
                data=None
            )

    def delete_list(self, list_id: int) -> BaseResponseData:
        try:
            result_dict = self._delete(f'/shoppinglists/{list_id}')

            if result_dict['success']:
                ShoppingListCash.remove(list_id)
                # Todo: remove list from UserCache

            return BaseResponseData(
                success=result_dict['success'],
                error=result_dict['error']
            )
        except Exception as ex:
            # Todo: Logging
            return BaseResponseData(
                success=False,
                error='API Error',
            )

    def get_list(self, list_id: int, already_bought: bool = False) \
            -> ResponseData[ShoppingListData]:
        try:
            result_dict = self._get(f'/shoppinglists/{list_id}/{already_bought}')

            result_data: Optional[ShoppingListData] = None
            if result_dict['success']:
                result_data = from_dict(ShoppingListData, result_dict['data'])

            ShoppingListCash.add(result_data.id, result_data)

            return ResponseData[ShoppingListData](
                success=result_dict['success'],
                error=result_dict['error'],
                data=result_data
            )
        except Exception as ex:
            # Todo: Error Login
            return ResponseData[ShoppingListData](
                success=False,
                error='API Error',
                data=None
            )

    def get_shopping_lists(self, force=False) -> ResponseData[ShoppingListCollection]:
        try:
            if not force and self.user_id:
                user = UserCash.get(self.user_id)
                if user:
                    lists = list(ShoppingListCash.items(user.lists))
                    if lists:
                        collection = ShoppingListCollection(lists=lists)

                        return ResponseData[ShoppingListCollection](
                            success=True,
                            cached=True,
                            error='',
                            data=collection
                        )

            result_dict = self._get('/shoppinglists')

            result_data = from_dict(ShoppingListCollection, result_dict['data']) \
                if result_dict['success'] else ShoppingListCollection()

            user_list_ids: List[int] = list()
            for shopping_list in result_data.lists:
                user_list_ids.append(shopping_list.id)
                ShoppingListCash.add(shopping_list.id, shopping_list)

            if self.user_id:
                user = UserCash.get(self.user_id)
                user = dataclasses.replace(user, lists=user_list_ids)
                UserCash.add(user.id, user)

            result: ResponseData[ShoppingListCollection] = \
                ResponseData[ShoppingListCollection](
                    success=result_dict['success'],
                    error=result_dict['error'],
                    data=result_data
                )

            return result
        except Exception as ex:
            # Todo: Logging
            return ResponseData[ShoppingListCollection](
                success=False,
                error='API Error',
                data=None
            )

    def add_product_to_list(self, list_id: int, name: str, amount: int,
                            gtin: str = None) \
            -> ResponseData[ShoppingListData]:
        args = {
            'ProductName': name,
            'Amount': amount,
            'GTin': gtin
        }

        data: Optional[ShoppingListData] = None

        try:
            result_dict = self._post(f'/shoppinglists/{list_id}/products/', args)
            if result_dict['success']:
                # Todo: better performance
                data = self.get_list(list_id).data

            return ResponseData(
                success=result_dict['success'],
                error=result_dict['error'],
                data=data
            )
        except Exception as ex:
            # Todo: Login
            return ResponseData(
                success=False,
                error='API Error',
                data=None
            )

    def change_list_product(self, list_id: int, product_id: int,
                            new_amount: int = None,
                            new_name: str = None) \
            -> ResponseData[ShoppingListData]:

        base_list_response = self.get_list(list_id)
        if not base_list_response.success:
            return ResponseData(
                success=False,
                error=base_list_response.error,
                data=None
            )

        base_list = base_list_response.data
        base_product = base_list.get_product(product_id)
        if base_product is None:
            return ResponseData(
                success=False,
                error=f'Product not founded with id {product_id}',
                data=None)

        change_amount = new_amount - base_product.amount

        args = {
            'NewName': new_name or base_product.name,
            'Change': change_amount or 0,
        }

        try:
            result_dict = self._put(f'/shoppinglists/{list_id}/products/{product_id}',
                                    args)
            if result_dict['success']:
                # Todo: better performance
                data = self.get_list(list_id).data

            return ResponseData(
                success=result_dict['success'],
                error=result_dict['error'],
                data=data
            )
        except Exception as ex:
            return ResponseData(
                success=False,
                error='API Error',
                data=None
            )
