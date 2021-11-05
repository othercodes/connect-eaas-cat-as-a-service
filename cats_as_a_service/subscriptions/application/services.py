from typing import List
from cats_as_a_service.shared.application.services import validator
from cats_as_a_service.shared.domain.models import ID
from cats_as_a_service.subscriptions.domain.contracts import SubscriptionSource
from cats_as_a_service.subscriptions.domain.models import Items


def subscription_validator(source: SubscriptionSource) -> List[Exception]:
    return validator({
        ID: source.id(),
        Items.from_list: source.items(),
    })
