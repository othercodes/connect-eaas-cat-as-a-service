from cats_as_a_service.subscriptions.application.services import subscription_validator


def test_should_successfully_validate_subscription_valid_arguments(fake_subscription_source):
    source = fake_subscription_source({
        'id': 'AS-0000-0000-0000',
        'item': ['https://cdn2.thecatapi.com/images/rqIRpFc3V.jpg'],
    })

    validation_result = subscription_validator(source)

    assert len(validation_result) == 0


def test_should_successfully_validate_subscription_invalid_arguments(fake_subscription_source):
    source = fake_subscription_source({
        'id': 'INVALID-ID',
        'items': [1, 2, 3],
    })

    validation_result = subscription_validator(source)

    assert len(validation_result) == 2
