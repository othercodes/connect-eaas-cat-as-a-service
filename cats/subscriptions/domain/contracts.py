from abc import ABCMeta, abstractmethod
from typing import List, Optional
from cats.shared.domain.models import ID
from cats.subscriptions.domain.models import Subscription


class SubscriptionSource(metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def id(self) -> Optional[str]:
        pass

    @abstractmethod
    def items(self) -> List[dict]:
        pass


class SubscriptionRepository(metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def find(self, id: ID) -> Optional[Subscription]:
        pass
