from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from models.base import BaseTableID

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import json

if TYPE_CHECKING:
    from models.company import Company


class LicenseBase(SQLModel):
    company_id: int = Field(foreign_key="company.id")
    file: bytes
    created_at: str

    def decrypt_license(self, private_key: rsa.RSAPrivateKey) -> dict:
        decrypted_data = private_key.decrypt(
            self.file,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()
        return json.loads(decrypted_data)

class License(LicenseBase, BaseTableID, table=True):
    company: "Company" = Relationship(back_populates="license")


