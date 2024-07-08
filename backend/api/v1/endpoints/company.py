from fastapi import APIRouter, Depends
from fastapi_pagination import LimitOffsetParams
from sqlmodel import col, select

from core.exceptions import NotFound
from core.utils.sqlmodel import relations
from deps.user import current_active_user
from enums.common import ListOrderEnum
from models.company import Company
from crud.company import company_crud
from models.company_user import CompanyUser
from models.user import User
from schemas.company import ICompanyCreate, ICompanyRead, ICompanyUpdate
from schemas.response import IResponsePaginated

router = APIRouter(
    generate_unique_id_function=lambda route: f"company_{route.name}",
)


@router.get(
    path="",
    response_model=IResponsePaginated[ICompanyRead],
)
async def get_list(
    order_by: str = "id",
    order: ListOrderEnum = ListOrderEnum.descendent,
    params: LimitOffsetParams = Depends(),
    user: User = Depends(current_active_user),
):
    query = select(Company).where(
        relations(Company.users).any(col(User.id) == user.id),
    )

    page = await company_crud.get_multi_paginated_ordered(
        query=query,
        params=params,
        order_by=order_by,
        order=order,
    )

    return page


@router.post(
    path="/list",
    response_model=list[ICompanyRead],
)
async def get_list_by_ids(
    list_ids: list[int],
):
    items = await company_crud.get_by_ids_ordered(
        list_ids=list_ids,
    )

    return items


@router.get(
    path="/{id}",
    response_model=ICompanyRead,
)
async def get_by_id(
    id: int,
):
    company = await company_crud.get(
        id=id,
    )

    if not company:
        raise NotFound

    return company


@router.post(
    path="",
    response_model=ICompanyRead,
)
async def create(
    payload: ICompanyCreate,
    user: User = Depends(current_active_user),
):
    company = await company_crud.create(
        obj_in=payload,
    )

    company = await company_crud.add_user(
        company=company,
        user=user,
    )

    return company


@router.put(
    path="/{id}",
    response_model=ICompanyRead,
)
async def update(
    id: int,
    payload: ICompanyUpdate,
):
    company = await company_crud.get(
        id=id,
    )

    if not company:
        raise NotFound

    company_updated = await company_crud.update(
        obj_current=company,
        obj_new=payload,
    )

    return company_updated


@router.delete(
    path="/{id}",
    response_model=ICompanyRead,
)
async def delete(
    id: int,
):
    company = await company_crud.get(
        id=id,
    )

    if not company:
        raise NotFound

    company_deleted = await company_crud.delete(id=company.id)

    return company_deleted
