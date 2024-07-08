from typing import Generic, Optional, TypeVar
from fastapi_pagination import LimitOffsetPage
from pydantic import BaseModel

T = TypeVar("T")


class INextCursor(BaseModel):
    offset: int
    limit: int


class IResponsePaginated(LimitOffsetPage[T], Generic[T]):
    next: Optional[INextCursor] = None
