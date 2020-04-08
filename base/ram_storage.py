from typing import Dict, Generic, Optional, TypeVar

T = TypeVar('T')
StorageType = Dict[int, T]


class RamStorage(Generic[T]):
    def __init__(self):
        self._storage: StorageType = dict()

    def add(self, pk: int, item: T):
        self._storage[pk] = item

    def get(self, pk: int) -> Optional[T]:
        return self._storage.get(pk, None)
