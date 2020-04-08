from typing import Optional

from dataclasses import dataclass

from .base_entity import BaseEntity


@dataclass(frozen=True)
class ProductData(BaseEntity):
    name: Optional[str] = None
    gtin: Optional[str] = None
    amount: int = 0
