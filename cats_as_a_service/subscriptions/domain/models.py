from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
from cats_as_a_service.shared.domain.models import ID


@dataclass(frozen=True)
class Item:
    id: str
    url: str


@dataclass(frozen=True)
class Items:
    value: List[Item]

    def __post_init__(self):
        self._invariant_value_must_be_a_list_of_items()

    def _invariant_value_must_be_a_list_of_items(self) -> None:
        if len(self.value) > 0 and not all(isinstance(item, Item) for item in self.value):
            raise ValueError(f'Invalid items <{self.value}>, must be a list of pair id and url.')

    @classmethod
    def from_list(cls, items: List[Dict[str, str]]) -> Items:
        return cls([Item(item['id'], item['url']) for item in items])


class Subscription:
    def __init__(self, id: ID, items: Items):
        self.id = id
        self.items = items
