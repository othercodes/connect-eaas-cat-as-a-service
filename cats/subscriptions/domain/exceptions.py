from __future__ import annotations

from typing import List

from cats.shared.domain.exceptions import CatAsAServiceException


class SubscriptionException(CatAsAServiceException):
    @staticmethod
    def building_failure(message: str, errors: List[Exception]) -> SubscriptionBuildingFailure:
        return SubscriptionBuildingFailure(message, errors)


class SubscriptionBuildingFailure(SubscriptionException):
    def __init__(self, message: str, errors: List[Exception]):
        self.message = message
        self.errors = errors

        super().__init__(f"{self.message} Errors: {self.errors}")
