from __future__ import annotations
from cats.shared.domain.exceptions import CatAsAServiceException


class SubscriptionException(CatAsAServiceException):
    @staticmethod
    def building_failure(message: str) -> SubscriptionBuildingFailure:
        return SubscriptionBuildingFailure(message)


class SubscriptionBuildingFailure(SubscriptionException):
    pass
