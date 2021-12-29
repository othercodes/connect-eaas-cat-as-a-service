from typing import List
from cats_as_a_service.orders.domain.contracts import OrderRepository, OrderSource
from cats_as_a_service.orders.domain.models import Amount, Categories, OrderType
from cats_as_a_service.orders.domain.services import order_builder
from cats_as_a_service.shared.application.services import validator
from cats_as_a_service.shared.domain.models import ID


def order_validator(source: OrderSource) -> List[Exception]:
    return validator({
        ID: source.id(),
        OrderType: source.order_type(),
        Categories: source.categories(),
        Amount: source.amount(),
    })


class OrderCreator:
    def __init__(self, order_repository: OrderRepository):
        self.__repository = order_repository

    def create(self, source: OrderSource) -> ID:
        order = order_builder(source)
        self.__repository.save(order)

        return order.id
