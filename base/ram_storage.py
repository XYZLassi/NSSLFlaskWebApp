from datetime import datetime, timedelta
from typing import Dict, Generic, Optional, TypeVar

from dataclasses import dataclass, field

T = TypeVar('T')


@dataclass(frozen=True)
class RamStorageItem(Generic[T]):
    item: T
    update_time: datetime = field(default_factory=datetime.now)


StorageType = Dict[int, RamStorageItem[T]]


class RamStorage(Generic[T]):
    def __init__(self, expire_time: Optional[timedelta] = None):
        self.expire_time = expire_time
        self._storage: StorageType = dict()

    def add(self, pk: int, item: T):
        self._storage[pk] = RamStorageItem(item=item)

    def get(self, pk: int) -> Optional[T]:
        item = self._storage.get(pk, None)

        if item is None:
            return None

        if self.expire_time and datetime.now() - item.update_time > self.expire_time:
            return None

        return item.item
