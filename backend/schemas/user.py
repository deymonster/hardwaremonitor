from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from typing import Optional
from models.user import RoleEnum


class IUserRead(BaseUser):
    telegram_id: str
    role: RoleEnum


class IUserCreate(BaseUserCreate):
    telegram_id: str
    role: Optional[RoleEnum] = RoleEnum.USER


class IUserUpdate(BaseUserUpdate):
    telegram_id: str
    role: Optional[RoleEnum]
