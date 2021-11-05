import pytest
from cats_as_a_service.orders.domain.exceptions import OrderBuildingFailure
from cats_as_a_service.orders.domain.models import Order
from cats_as_a_service.orders.domain.services import order_builder


def test_should_success_building_a_order(fake_order_source):
    source = fake_order_source({
        'id': 'AS-0000-0000-0000',
        'order_type': 'ASC',
        'categories': [14, 15],
        'amount': 5,
    })

    order = order_builder(source)

    assert isinstance(order, Order)


def test_should_fail_building_a_order(fake_order_source):
    source = fake_order_source({
        'id': 'AS-0000-0000-0000',
        'order_type': 'ASC',
        'categories': [14, 15],
        'amount': 'Invalid amount',
    })

    with pytest.raises(OrderBuildingFailure):
        order_builder(source)
