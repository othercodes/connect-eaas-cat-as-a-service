from cats.orders.domain.contracts import OrderRepository, OrderSource
from cats.orders.domain.models import Order
from cats.orders.domain.services import order_builder


class OrderCreator:
    def __init__(self, order_repository: OrderRepository):
        self.repository = order_repository

    def __call__(self, source: OrderSource) -> Order:
        return self.create(source)

    def create(self, source: OrderSource) -> Order:
        order = order_builder(source)
        self.repository.save(order)

        return order
