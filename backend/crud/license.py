from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from crud.base import CRUDBase
from models.license import License
from models.user import User
from schemas.license import ILicenseRead, ILisenseCreate, ILicenseUpdate
from cryptography.hazmat.primitives.asymmetric import rsa



class LicenseCRUD(CRUDBase[License, ILisenseCreate, ILicenseUpdate]):
    async def get_by_company_id(
        self,
        company_id: int,
        db_session: AsyncSession | None = None
    ) -> License | None:
        session: AsyncSession = db_session or self.db.session
        query = select(self.model).where(self.model.company_id == company_id)
        response = await session.execute(query)
        return response.scalar_one_or_none()


license_crud = LicenseCRUD(License)


__all__ = [
    "license_crud",
]