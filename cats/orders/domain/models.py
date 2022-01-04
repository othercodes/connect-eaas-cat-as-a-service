from dataclasses import dataclass
from enum import Enum, unique
from typing import List
from cats.shared.domain.models import ID


@dataclass(frozen=True)
class Categories:
    value: List[int]

    def __post_init__(self):
        self._invariant_categories_must_be_a_list_of_integers()

    def _invariant_categories_must_be_a_list_of_integers(self) -> None:
        if not all(isinstance(category, int) for category in self.value):
            raise ValueError(f'Invalid category list <{self.value}>, must be a list of integer.')


@dataclass(frozen=True)
class Amount:
    value: int

    def __post_init__(self):
        self._invariant_amount_must_be_positive_integer()

    def _invariant_amount_must_be_positive_integer(self) -> None:
        if not isinstance(self.value, int) or self.value < 0:
            raise ValueError(f'Invalid amount value <{self.value}>, must be a positive integer.')


@unique
class OrderType(Enum):
    RANDOM = 'RANDOM'
    ASC = 'ASC'
    DESC = 'DESC'


class Order:
    def __init__(self, id: ID, order_type: OrderType, categories: Categories, amount: Amount):
        self.id = id
        self.order_type = order_type
        self.categories = categories
        self.amount = amount

    def __str__(self) -> str:
        return "{id}: ({order_type}, {categories}) x{amount}".format(
            id=self.id.value,
            order_type=self.order_type.value,
            categories=self.categories.value,
            amount=self.amount.value,
        )
