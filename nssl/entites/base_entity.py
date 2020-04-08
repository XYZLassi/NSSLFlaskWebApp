from dataclasses import dataclass


@dataclass(frozen=True)
class BaseEntity:
    id: int = 0
