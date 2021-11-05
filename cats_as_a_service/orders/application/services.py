from typing import List
from cats_as_a_service.orders.domain.contracts import OrderSource
from cats_as_a_service.orders.domain.models import Amount, Categories, OrderType
from cats_as_a_service.shared.application.services import validator
from cats_as_a_service.shared.domain.models import ID


def order_validator(source: OrderSource) -> List[Exception]:
    return validator({
        ID: source.id(),
        OrderType: source.order_type(),
        Categories: source.categories(),
        Amount: source.amount(),
    })
