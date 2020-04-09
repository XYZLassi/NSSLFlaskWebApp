from typing import Generic, Optional, TypeVar

from dataclasses import dataclass

T = TypeVar('T')


@dataclass(frozen=True)
class BaseResponseData:
    success: bool = False
    error: str = 'Unknown Error'


@dataclass(frozen=True)
class ResponseData(Generic[T], BaseResponseData):
    cached: bool = False

    data: Optional[T] = None
