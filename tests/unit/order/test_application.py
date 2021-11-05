from cats_as_a_service.orders.application.services import order_validator


def test_should_successfully_validate_order_valid_arguments(fake_order_source):
    source = fake_order_source({
        'id': 'AS-0000-0000-0000',
        'order_type': 'ASC',
        'categories': [14, 15],
        'amount': 5,
    })

    validation_result = order_validator(source)

    assert len(validation_result) == 0


def test_should_successfully_validate_order_invalid_arguments(fake_order_source):
    source = fake_order_source({
        'id': 'INVALID-ID',
        'order_type': 'INVALID-ORDER-TYPE',
        'categories': ["INVALID-CATEGORY"],
        'amount': "INVALID-AMOUNT",
    })

    validation_result = order_validator(source)

    assert len(validation_result) == 4
