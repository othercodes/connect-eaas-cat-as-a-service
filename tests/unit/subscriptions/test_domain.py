import pytest
from cats.subscriptions.domain.exceptions import SubscriptionBuildingFailure
from cats.subscriptions.domain.models import Subscription
from cats.subscriptions.domain.services import subscription_builder, subscription_validator


def test_should_successfully_validate_subscription_valid_arguments(fake_subscription_source):
    source = fake_subscription_source({
        'id': 'AS-0000-0000-0000',
        'item': ['https://cdn2.thecatapi.com/images/rqIRpFc3V.jpg'],
    })

    errors, valid = subscription_validator(source)

    assert len(errors) == 0
    assert len(valid) == 2


def test_should_successfully_validate_subscription_invalid_arguments(fake_subscription_source):
    source = fake_subscription_source({
        'id': 'INVALID-ID',
        'items': [1, 2, 3],
    })

    errors, valid = subscription_validator(source)

    assert len(errors) == 2
    assert len(valid) == 0


def test_should_success_building_a_subscription(fake_subscription_source):
    source = fake_subscription_source({
        'id': 'AS-0000-0000-0000',
        'items': [
            {'id': 'rqIRpFc3V', 'url': 'https://cdn2.thecatapi.com/images/rqIRpFc3V.jpg'},
        ],
    })

    subscription = subscription_builder(source)

    assert isinstance(subscription, Subscription)


def test_should_fail_building_a_subscription(fake_subscription_source):
    source = fake_subscription_source({
        'id': 'AS-0000-0000-0000',
        'items': [1, 2, 3],
    })

    with pytest.raises(SubscriptionBuildingFailure):
        subscription_builder(source)
