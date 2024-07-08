from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from models.base import BaseTable
from models.company import Company
from models.company_user import CompanyUser


class UserBase(SQLModel):
    pass


class User(UserBase, SQLModelBaseUserDB, BaseTable, table=True):
    companies: list["Company"] = Relationship(
        back_populates="users",
        link_model=CompanyUser,
    )
