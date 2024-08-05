from typing import TYPE_CHECKING, Optional
from sqlmodel import Relationship, SQLModel, Field
from enum import Enum
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from models.base import BaseTable
from models.company import Company
from models.company_user import CompanyUser


class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserBase(SQLModel):
    email: str = Field(..., unique=True, index=True)
    telegram_id: Optional[str] = Field(default=None, index=True)
    role: Optional[RoleEnum] = Field(RoleEnum.USER, description="Role of the user")



class User(UserBase, SQLModelBaseUserDB, BaseTable, table=True):
    companies: list["Company"] = Relationship(
        back_populates="users",
        link_model=CompanyUser,
    )
