from fastapi import APIRouter, Depends

from schemas.trigger import ITriggerCreate, ITriggerRead
from crud.trigger import trigger_crud


router = APIRouter(
    generate_unique_id_function=lambda route: f"trigger_{route.name}",
)


@router.post(
    path="",
    response_model=ITriggerCreate,
)
async def create(
        payload: ITriggerCreate
) -> ITriggerRead:
    trigger = await trigger_crud.create(
        obj_in=payload
    )

    return trigger