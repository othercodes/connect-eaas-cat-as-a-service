from cats_as_a_service.shared.domain.models import ID
from cats_as_a_service.subscriptions.domain.contracts import SubscriptionSource
from cats_as_a_service.subscriptions.domain.exceptions import SubscriptionException
from cats_as_a_service.subscriptions.domain.models import Items, Subscription


def subscription_builder(source: SubscriptionSource) -> Subscription:
    try:
        return Subscription(
            id=ID(source.id()),
            items=Items.from_list(source.items()),
        )
    except (ValueError, TypeError) as ex:
        raise SubscriptionException.building_failure(str(ex))
