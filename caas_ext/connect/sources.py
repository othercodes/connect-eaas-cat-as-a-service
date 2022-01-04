from typing import List, Optional

from connect.processors_toolkit.requests import RequestBuilder

from cats.orders.domain.contracts import OrderSource


class ConnectOrderSource(OrderSource):
    def __init__(self, request: RequestBuilder):
        self._request = request

    def id(self) -> Optional[str]:
        subscription_id = self._request.asset().asset_param('CAT_SUBSCRIPTION_ID', 'value')
        return self._request.asset().asset_id() if subscription_id == '' else subscription_id

    def order_type(self) -> str:
        return self._request.asset().asset_param('ORDER_TYPE', 'value')

    def categories(self) -> List[int]:
        categories = self._request.asset().asset_param('CATEGORIES', 'structured_value')
        return [int(k) for k, v in categories.items() if v]

    def amount(self) -> int:
        try:
            return int(next(filter(
                lambda item: int(item.get('quantity', 0)) > 0,
                self._request.asset().asset_items(),
            )).get('quantity', 0))
        except StopIteration:
            return 0
