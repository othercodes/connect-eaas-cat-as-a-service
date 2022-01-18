from typing import Any, List, Tuple

from cats.orders.domain.contracts import OrderSource
from cats.orders.domain.exceptions import OrderException
from cats.orders.domain.models import Amount, Categories, Order, OrderType
from cats.shared.domain.services import validator
from cats.shared.domain.models import ID


def order_validator(source: OrderSource) -> Tuple[List[Exception], List[Any]]:
    return validator(
        [ID, OrderType, Categories, Amount],
        [source.id(), source.order_type(), source.categories(), source.amount()],
    )


def order_builder(source: OrderSource) -> Order:
    errors, members = order_validator(source)
    if len(errors) > 0:
        raise OrderException.building_failure(
            'Unable to create a Order due to invalid data.',
            errors,
        )

    return Order(*members)
