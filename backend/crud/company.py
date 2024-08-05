from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from crud.base import CRUDBase
from crud.license import license_crud
from models.company import Company
from models.user import User
from models.license import License
from schemas.company import ICompanyRead, ICompanyCreate, ICompanyUpdate
from cryptography.hazmat.primitives.asymmetric import rsa


class CRUDCompany(CRUDBase[Company, ICompanyCreate, ICompanyUpdate]):
    async def add_user(
        self,
        *,
        company: Company,
        user: User,
        db_session: AsyncSession | None = None,
    ):
        session = db_session or self.db.session
        await session.refresh(company, attribute_names=["users"])
        company.users.append(user)
        await session.commit()
        return company

    async def get_count_license(self,
                                *,
                                company_id: int,
                                private_key: rsa.RSAPrivateKey,
                                db_session: AsyncSession | None = None) -> int | None:
        """Получение количества лицензий компании по id

        :param company_id: company id
        :param private_key: private key
        :param db_session: database session
        :return: int count of license
        """

        session: AsyncSession = db_session or self.db.session

        # Получение компании по её id через базовый метод get_by_id
        company = await self.get(id=company_id, db_session=session)
        if not company:
            return "Компания не найдена."

        license_obj = await license_crud.get_by_company_id(company_id=company_id, db_session=session)

        if license_obj:
            try:
                decrypted_data = license_obj.decrypt_license(private_key)
                if decrypted_data['inn'] == Company.inn:
                    return decrypted_data['count']
                else:
                    await session.delete(license_obj)
                    await session.commit()
            except Exception as e:
                return f"Ошибка при расшифровке лицензии: {str(e)}"
        else:
            return "Лицензия не найдена."



company_crud = CRUDCompany(Company)


__all__ = [
    "company_crud",
]
