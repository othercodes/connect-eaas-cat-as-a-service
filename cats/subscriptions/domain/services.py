from typing import Any, List, Tuple

from cats.shared.domain.services import validator
from cats.shared.domain.models import ID
from cats.subscriptions.domain.contracts import SubscriptionSource
from cats.subscriptions.domain.exceptions import SubscriptionException
from cats.subscriptions.domain.models import Items, Subscription


def subscription_validator(source: SubscriptionSource) -> Tuple[List[Exception], List[Any]]:
    return validator(
        [ID, Items.from_list],
        [source.id(), source.items()],
    )


def subscription_builder(source: SubscriptionSource) -> Subscription:
    errors, members = subscription_validator(source)
    if len(errors) > 0:
        raise SubscriptionException.building_failure(
            'Unable to create a Subscription due to invalid data.',
            errors,
        )

    return Subscription(*members)
