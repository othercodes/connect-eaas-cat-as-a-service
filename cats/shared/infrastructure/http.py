from typing import List

from requests import Response

from cats.shared.domain.exceptions import CatAsAServiceException
import requests


class HTTPClient:
    def __init__(self, api_key: str, api_url: str):
        self._api_key = api_key
        self._api_url = api_url

    def _search_images(self, order_type: str, categories: List[int], limit: int) -> Response:
        response = requests.get(
            url=self._api_url + 'v1/images/search',
            headers={
                'x-api-key': self._api_key,
            },
            params={
                'size': 'full',
                'order': order_type,
                'category_ids[]': categories,
                'limit': limit,
                'page': 0,
            },
        )

        if response.status_code != 200:
            raise CatAsAServiceException(response.text)

        return response

    def _get_favourites(self, sub_id) -> Response:
        response = requests.get(
            url=self._api_url + 'v1/favourites',
            headers={
                'x-api-key': self._api_key,
            },
            params={
                'sub_id': sub_id,
            },
        )

        if response.status_code != 200:
            raise CatAsAServiceException(response.text)

        return response

    def _create_favourite(self, image_id: str, sub_id: str) -> Response:
        response = requests.post(
            url=self._api_url + 'v1/favourites',
            headers={
                'x-api-key': self._api_key,
            },
            json={
                'image_id': image_id,
                'sub_id': sub_id,
            },
        )

        if response.status_code != 200:
            raise CatAsAServiceException(response.text)

        return response

    def _delete_favourite(self, favourite_id: str) -> None:
        response = requests.delete(
            url=self._api_url + 'v1/favourites/' + favourite_id,
            headers={
                'x-api-key': self._api_key,
            },
        )

        if response.status_code != 200:
            raise CatAsAServiceException(response.text)
