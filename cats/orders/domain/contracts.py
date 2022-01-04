from abc import ABCMeta, abstractmethod
from typing import List, Optional
from cats.orders.domain.models import Order


class OrderSource(metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def id(self) -> Optional[str]:
        pass

    @abstractmethod
    def order_type(self) -> str:
        pass

    @abstractmethod
    def categories(self) -> List[int]:
        pass

    @abstractmethod
    def amount(self) -> int:
        pass


class OrderRepository(metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def save(self, order: Order) -> None:
        pass
