import json
from collections import namedtuple
from collections.abc import Iterable
from types import MethodType
from typing import List, Optional
from urllib.parse import parse_qs
from connect.client import ConnectClient
import pytest
import requests
import responses
import os

from cats.orders.domain.contracts import OrderSource
from cats.subscriptions.domain.contracts import SubscriptionSource

ConnectResponse = namedtuple(
    'ConnectResponse',
    (
        'count', 'query', 'ordering', 'select',
        'value', 'status', 'exception',
    ),
)


def _parse_qs(url):
    if '?' not in url:
        return None, None, None

    url, qs = url.split('?')
    parsed = parse_qs(qs, keep_blank_values=True)
    ordering = None
    select = None
    query = None

    for k in parsed.keys():
        if k.startswith('ordering('):
            ordering = k[9:-1].split(',')
        elif k.startswith('select('):
            select = k[7:-1].split(',')
        else:
            value = parsed[k]
            if not value[0]:
                query = k

    return query, ordering, select


def _mock_kwargs_generator(response_iterator, url):
    res = next(response_iterator)

    query, ordering, select = _parse_qs(url)
    if res.query:
        assert query == res.query, 'RQL query does not match.'
    if res.ordering:
        assert ordering == res.ordering, 'RQL ordering does not match.'
    if res.select:
        assert select == res.select, 'RQL select does not match.'
    mock_kwargs = {
        'match_querystring': False,
    }
    if res.count is not None:
        end = 0 if res.count == 0 else res.count - 1
        mock_kwargs['status'] = 200
        mock_kwargs['headers'] = {'Content-Range': f'items 0-{end}/{res.count}'}
        mock_kwargs['json'] = []

    mock_kwargs.update(_value_arg_validation(res))
    return mock_kwargs


def _value_arg_validation(res):
    result = {}
    if isinstance(res.value, Iterable):
        count = len(res.value)
        end = 0 if count == 0 else count - 1
        result['status'] = 200
        result['json'] = res.value
        result['headers'] = {
            'Content-Range': f'items 0-{end}/{count}',
        }
    elif isinstance(res.value, dict):
        result['status'] = res.status or 200
        result['json'] = res.value
    elif res.value is None:
        if res.exception:
            result['body'] = res.exception
        else:
            result['status'] = res.status
    else:
        result['status'] = res.status or 200
        result['body'] = str(res.value)
    return result


@pytest.fixture
def response():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def logger(mocker):
    return mocker.MagicMock()


@pytest.fixture
def response_factory():
    def _create_response(
            count=None,
            query=None,
            ordering=None,
            select=None,
            value=None,
            status=None,
            exception=None,
    ):
        return ConnectResponse(
            count=count,
            query=query,
            ordering=ordering,
            select=select,
            value=value,
            status=status,
            exception=exception,
        )

    return _create_response


@pytest.fixture
def sync_client_factory():
    def _create_sync_client(connect_responses):
        response_iterator = iter(connect_responses)

        def _execute_http_call(self, method, url, kwargs):
            mock_kwargs = _mock_kwargs_generator(response_iterator, url)
            with responses.RequestsMock() as rsps:
                rsps.add(
                    method.upper(),
                    url,
                    **mock_kwargs,
                )
                self.response = requests.request(method, url, **kwargs)
                if self.response.status_code >= 400:
                    self.response.raise_for_status()

        client = ConnectClient('Key', use_specs=False)
        client._execute_http_call = MethodType(_execute_http_call, client)
        return client

    return _create_sync_client


@pytest.fixture
def live_client_factory():
    def _create_live_client():
        return ConnectClient(
            api_key=os.getenv('API_KEY'),
            endpoint=os.getenv('SERVER_ADDRESS'),
        )

    return _create_live_client


@pytest.fixture
def fake_subscription_source():
    class _MockSubscriptionSource(SubscriptionSource):
        def __init__(self, data: dict):
            self._data = data

        def id(self) -> Optional[str]:
            return self._data.get('id', 'AS-0000-0000-0000')

        def items(self) -> List[dict]:
            return self._data.get('items', [])

    def _make_mock_subscription_source(source: dict) -> SubscriptionSource:
        return _MockSubscriptionSource(source)

    return _make_mock_subscription_source


@pytest.fixture
def fake_order_source():
    class _MockOrderSource(OrderSource):
        def id(self) -> Optional[str]:
            return self._data.get('id')

        def __init__(self, data: dict):
            self._data = data

        def order_type(self) -> str:
            return self._data.get('order_type', 'ASC')

        def categories(self) -> List[int]:
            return self._data.get('categories', [])

        def amount(self) -> int:
            return self._data.get('amount', 0)

    def _make_mock_order_source(source: dict) -> OrderSource:
        return _MockOrderSource(source)

    return _make_mock_order_source


@pytest.fixture
def config():
    return {
        'api_key': os.getenv('CAT_API_KEY'),
        'api_url': os.getenv('CAT_API_URL'),
    }


@pytest.fixture
def load_json():
    def _load_json_file(path: str) -> dict:
        with open(path) as file:
            return json.load(file)

    return _load_json_file


@pytest.fixture
def test_path():
    def _test_path(absolute_path_from_test: str) -> str:
        return os.path.dirname(__file__) + absolute_path_from_test

    return _test_path
