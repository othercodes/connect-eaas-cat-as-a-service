from cats_as_a_service.orders.domain.contracts import OrderRepository
from cats_as_a_service.orders.domain.models import Order
from cats_as_a_service.shared.infrastructure.http import HTTPClient
import itertools


class HTTPOrderRepository(HTTPClient, OrderRepository):
    def save(self, order: Order) -> None:
        current = self._get_favourites(order.id.value)
        current_amount = int(current.headers.get('pagination-count', 0))
        current_items = [{'id': item['id'], 'url': item['image']['url']} for item in current.json()]

        if current_amount < order.amount.value:
            new_amount = order.amount.value - current_amount

            items = self._search_images(
                order_type=order.order_type.value,
                categories=order.categories.value,
                limit=new_amount,
            )

            for item in items.json():
                self._create_favourite(str(item['id']), order.id.value)

        elif current_amount > order.amount.value:
            amount_to_remove = current_amount - order.amount.value
            items_to_remove = itertools.islice(current_items, amount_to_remove)

            for item in items_to_remove:
                self._delete_favourite(str(item['id']))
