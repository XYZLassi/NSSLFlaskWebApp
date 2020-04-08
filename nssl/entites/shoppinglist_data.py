from typing import List

from dataclasses import dataclass, field

from .base_entity import BaseEntity


@dataclass(frozen=True)
class ShoppingListData(BaseEntity):
    name: str = 'no name'
    is_admin: bool = False


@dataclass(frozen=True)
class ShoppingListCollection(BaseEntity):
    lists: List[ShoppingListData] = field(default_factory=list)
