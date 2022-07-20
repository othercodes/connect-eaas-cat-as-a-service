from typing import List

from requests import Response, delete, get, post

from cats.shared.infrastructure.exceptions import (
    CatServerError,
    CatClientError,
    CatConfigurationError,
)


def _check_response(response: Response) -> Response:
    if response.status_code >= 500:
        raise _make_server_error(response)

    if response.status_code >= 400:
        raise _make_client_error(response)

    return response


def _make_server_error(response: Response) -> CatServerError:
    return CatServerError(
        response.json().get('message'),
        str(response.status_code),
        {'response': response}
    )


def _make_client_error(response: Response) -> CatClientError:
    return CatClientError(
        response.json().get('message'),
        str(response.status_code),
        {'response': response}
    )


class HTTPClient:
    def __init__(self, cat_api_key: str, cat_api_url: str):
        if not cat_api_key:
            raise CatConfigurationError('Missing api key.', 'MISSING_PARAMETER', 'cat_api_key')
        self._api_key = cat_api_key

        if not cat_api_url:
            raise CatConfigurationError('Missing api url.', 'MISSING_PARAMETER', 'cat_api_url')
        self._api_url = cat_api_url

    def _search_images(self, order_type: str, categories: List[int], limit: int) -> Response:
        response = get(
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

        _check_response(response)

        return response

    def _get_favourites(self, sub_id) -> Response:
        response = get(
            url=self._api_url + 'v1/favourites',
            headers={
                'x-api-key': self._api_key,
            },
            params={
                'sub_id': sub_id,
            },
        )

        _check_response(response)

        return response

    def _create_favourite(self, image_id: str, sub_id: str) -> Response:
        response = post(
            url=self._api_url + 'v1/favourites',
            headers={
                'x-api-key': self._api_key,
            },
            json={
                'image_id': image_id,
                'sub_id': sub_id,
            },
        )

        _check_response(response)

        return response

    def _delete_favourite(self, favourite_id: str) -> None:
        response = delete(
            url=self._api_url + 'v1/favourites/' + favourite_id,
            headers={
                'x-api-key': self._api_key,
            },
        )

        _check_response(response)
