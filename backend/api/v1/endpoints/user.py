from fastapi import APIRouter

from core.user_management import fastapi_users
from schemas.user import IUserRead, IUserUpdate


router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(IUserRead, IUserUpdate),
)

# TODO - изменить эндпойнты чтобы при регистрации пользователя была проверка на роль, если роль не равна админу,то роль по умолчанию user
