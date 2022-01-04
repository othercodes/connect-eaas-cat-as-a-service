from cats.orders.domain.contracts import OrderSource
from cats.orders.domain.exceptions import OrderException
from cats.orders.domain.models import Amount, Categories, Order, OrderType
from cats.shared.domain.models import ID


def order_builder(source: OrderSource) -> Order:
    try:
        return Order(
            id=ID(source.id()),
            order_type=OrderType(source.order_type()),
            categories=Categories(source.categories()),
            amount=Amount(source.amount()),
        )
    except ValueError as ex:
        raise OrderException.building_failure(str(ex))
