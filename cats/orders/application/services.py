from typing import List
from cats.orders.domain.contracts import OrderRepository, OrderSource
from cats.orders.domain.models import Amount, Categories, Order, OrderType
from cats.orders.domain.services import order_builder
from cats.shared.application.services import validator
from cats.shared.domain.models import ID


class OrderCreator:
    def __init__(self, order_repository: OrderRepository):
        self.repository = order_repository

    def __call__(self, source: OrderSource) -> Order:
        return self.create(source)

    def create(self, source: OrderSource) -> Order:
        order = order_builder(source)
        self.repository.save(order)

        return order


def order_validator(source: OrderSource) -> List[Exception]:
    return validator({
        ID: source.id(),
        OrderType: source.order_type(),
        Categories: source.categories(),
        Amount: source.amount(),
    })
