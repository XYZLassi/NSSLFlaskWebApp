from datetime import datetime
from typing import List, Optional

from dataclasses import dataclass, field

from .base_entity import BaseEntity
from .product import ProductData


@dataclass(frozen=True)
class ShoppingListData(BaseEntity):
    name: str = 'no name'
    is_admin: bool = False

    products: List[ProductData] = field(default_factory=list)

    refresh_data: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class ShoppingListCollection:
    lists: List[ShoppingListData] = field(default_factory=list)

    def get_list(self, list_id: int) -> Optional[ShoppingListData]:
        for shopping_list in self.lists:
            if shopping_list.id == list_id:
                return shopping_list
        return None
