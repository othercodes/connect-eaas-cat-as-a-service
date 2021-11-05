from typing import List, Optional
from cats_as_a_service.shared.domain.models import ID
from cats_as_a_service.shared.infrastructure.http import HTTPClient
from cats_as_a_service.subscriptions.domain.contracts import (
    SubscriptionRepository,
    SubscriptionSource,
)
from cats_as_a_service.subscriptions.domain.models import Subscription
from cats_as_a_service.subscriptions.domain.services import subscription_builder


class HTTPSubscriptionSource(SubscriptionSource):
    def __init__(self, data: dict):
        self._data = data

    def id(self) -> Optional[str]:
        return self._data.get('id')

    def items(self) -> List[str]:
        return self._data.get('items', [])


class HTTPSubscriptionRepository(HTTPClient, SubscriptionRepository):
    def find(self, id: ID) -> Subscription:
        response = self._get_favourites(id.value)

        return subscription_builder(HTTPSubscriptionSource({
            'id': id.value,
            'items': [{'id': item['id'], 'url': item['image']['url']} for item in response.json()],
        }))
