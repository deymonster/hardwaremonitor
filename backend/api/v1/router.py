from fastapi import APIRouter


from .endpoints import (
    auth,
    user,
    company,
    agent_data,
    trigger
)

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)

api_router.include_router(
    user.router,
    prefix="/user",
    tags=["user"],
)

api_router.include_router(
    company.router,
    prefix="/company",
    tags=["company"],
)

api_router.include_router(
    agent_data.router,
    prefix="/agent_data",
    tags=["agent_data"],
)

api_router.include_router(
    trigger.router,
    prefix="/trigger",
    tags=["trigger"],
)






