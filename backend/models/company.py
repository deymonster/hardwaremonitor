from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel
from models.base import BaseTableID
from models.company_user import CompanyUser

if TYPE_CHECKING:
    from models.user import User


class CompanyBase(SQLModel):
    name: str
    token: str


class Company(CompanyBase, BaseTableID, table=True):
    users: list["User"] = Relationship(
        back_populates="companies",
        link_model=CompanyUser,
    )
