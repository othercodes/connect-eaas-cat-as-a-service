from cats_as_a_service.subscriptions.domain.models import ID, Subscription
from cats_as_a_service.subscriptions.infrastructure.http import HTTPSubscriptionRepository


def test_should_successfully_find_a_subscription(config):
    repository = HTTPSubscriptionRepository(api_key=config['api_key'], api_url=config['api_url'])

    subscription = repository.find(ID('AS-0000-0000-0000'))

    assert isinstance(subscription, Subscription)
