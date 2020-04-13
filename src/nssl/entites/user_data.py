from typing import List

from dataclasses import dataclass, field

from .base_entity import BaseEntity


@dataclass(frozen=True)
class UserData(BaseEntity):
    username: str = 'anonymous'
    token: str = ''
    lists: List[int] = field(default_factory=list)
