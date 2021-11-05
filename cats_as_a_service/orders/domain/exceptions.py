from __future__ import annotations
from cats_as_a_service.shared.domain.exceptions import CatAsAServiceException


class OrderException(CatAsAServiceException):
    @staticmethod
    def building_failure(message: str) -> OrderBuildingFailure:
        return OrderBuildingFailure(message)


class OrderBuildingFailure(OrderException):
    pass
