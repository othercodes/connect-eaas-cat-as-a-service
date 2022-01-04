from typing import List
from cats.shared.application.services import validator
from cats.shared.domain.models import ID
from cats.subscriptions.domain.contracts import SubscriptionSource
from cats.subscriptions.domain.models import Items


def subscription_validator(source: SubscriptionSource) -> List[Exception]:
    return validator({
        ID: source.id(),
        Items.from_list: source.items(),
    })
