from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field
from cryptography.hazmat.primitives.asymmetric import rsa
from pydantic import field_validator
from models.base import BaseTableID
from models.company_user import CompanyUser

if TYPE_CHECKING:
    from models.user import User
    from models.license import License


class CompanyBase(SQLModel):
    name: str = Field(..., description="Название компании")
    inn: str = Field(unique = True, index = True, description="ИНН компании")

    def __init__(self, **data):
        if "inn" in data:
            self.validate_inn(data["inn"])
        super().__init__(**data)

    @staticmethod
    def validate_inn(value):
        if len(value) not in (10, 12):
            raise ValueError("ИНН должен содержать 10 или 12 цифр.")
        if not value.isdigit():
            raise ValueError("ИНН должен содержать только цифры.")
        return value


class Company(CompanyBase, BaseTableID, table=True):
    users: list["User"] = Relationship(
        back_populates="companies",
        link_model=CompanyUser,

    )
    license: "License" = Relationship(back_populates="company", sa_relationship_kwargs={"uselist": False})



