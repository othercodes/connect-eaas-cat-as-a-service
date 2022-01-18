import pytest
from cats.orders.domain.exceptions import OrderBuildingFailure
from cats.orders.domain.models import Order
from cats.orders.domain.services import order_builder, order_validator


def test_should_successfully_validate_order_valid_arguments(fake_order_source):
    source = fake_order_source({
        'id': 'AS-0000-0000-0000',
        'order_type': 'ASC',
        'categories': [14, 15],
        'amount': 5,
    })

    errors, valid = order_validator(source)

    assert len(errors) == 0
    assert len(valid) == 4


def test_should_successfully_validate_order_invalid_arguments(fake_order_source):
    source = fake_order_source({
        'id': 'INVALID-ID',
        'order_type': 'INVALID-ORDER-TYPE',
        'categories': ["INVALID-CATEGORY"],
        'amount': "INVALID-AMOUNT",
    })

    errors, valid = order_validator(source)

    assert len(errors) == 4
    assert len(valid) == 0


def test_builder_should_success_building_a_order(fake_order_source):
    source = fake_order_source({
        'id': 'AS-0000-0000-0000',
        'order_type': 'ASC',
        'categories': [14, 15],
        'amount': 5,
    })

    order = order_builder(source)

    assert isinstance(order, Order)


def test_builder_should_fail_building_a_order(fake_order_source):
    source = fake_order_source({
        'id': 'AS-0000-0000-0000',
        'order_type': 'ASC',
        'categories': [14, 15],
        'amount': 'Invalid amount',
    })

    with pytest.raises(OrderBuildingFailure):
        order_builder(source)
