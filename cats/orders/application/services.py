from typing import List
from cats.orders.domain.contracts import OrderSource
from cats.orders.domain.models import Amount, Categories, OrderType
from cats.shared.application.services import validator
from cats.shared.domain.models import ID


def order_validator(source: OrderSource) -> List[Exception]:
    return validator({
        ID: source.id(),
        OrderType: source.order_type(),
        Categories: source.categories(),
        Amount: source.amount(),
    })
