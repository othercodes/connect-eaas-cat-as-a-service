import pytest
from cats_as_a_service.subscriptions.domain.exceptions import SubscriptionBuildingFailure
from cats_as_a_service.subscriptions.domain.models import Subscription
from cats_as_a_service.subscriptions.domain.services import subscription_builder


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
