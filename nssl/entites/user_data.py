from dataclasses import dataclass

from .base_entity import BaseEntity


@dataclass(frozen=True)
class UserData(BaseEntity):
    username: str = 'anonymous'
    token: str = ''
