from fastapi import FastAPI, WebSocket
from fastapi.middleware import Middleware
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from fastapi_pagination import add_pagination
from motor.motor_asyncio import AsyncIOMotorClient
from api.router import api_router
from config import settings
from core.db import pydantic_serializer
from core.mongo_db import init_mongo_db, close_mongo_db, get_mongo_db
from core.utils.services.zeroconf_service import ZeroConfService
from core.utils.services.broadcast_service import service_broadcast
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from api.ws import ws_router

from pymongo import ASCENDING
from pymongo.errors import PyMongoError


service_zeroconf= ZeroConfService(service_name="NITRINOnet_HardwareMonitor", service_type="_http._tcp.local.", port=8000)


class MyApp(FastAPI):
    mongodb_client: AsyncIOMotorClient | None
    mongodb: object | None


def create_app():
    app = MyApp(
        title="HardwareMonitor",
        version="0.1",
        openapi_url="/openapi.json" if settings.DEBUG else None,
        docs_url="/docs" if settings.DEBUG else None,
        debug=settings.DEBUG,
        middleware=[
            Middleware(
                SQLAlchemyMiddleware,
                db_url=settings.DB_ASYNC_CONNECTION_STR,
                engine_args=dict(
                    echo=settings.DEBUG,
                    pool_pre_ping=True,
                    pool_size=settings.POSTGRES_POOL_SIZE_BY_SERVER,
                    max_overflow=settings.POSTGRES_MAX_OVERFLOW,
                    json_serializer=pydantic_serializer,
                ),
                session_args=dict(
                    autoflush=False,
                    autocommit=False,
                ),
            ),
            Middleware(
                SessionMiddleware,
                secret_key=settings.APP_SECRET_KEY,
            ),
            Middleware(
                CORSMiddleware,
                allow_origins=settings.ALLOW_ORIGINS,
                allow_origin_regex=settings.ALLOW_ORIGIN_REGEX,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            ),
        ],
    )

    #app.mount("/ws", ws)


    @app.on_event("startup")
    async def startup_event():
        service_zeroconf.start()
        await service_broadcast.start()
        print("Server is starting up...") # here will be checking signature
        mongo_uri = settings.mongo_url
        #app.mongodb_client = AsyncIOMotorClient(mongo_uri, uuidRepresentation='standard')
        #app.mongodb = app.mongodb_client[settings.MONGO_NAME]
        await init_mongo_db(uri=mongo_uri, db_name=settings.MONGO_NAME)
        app.mongodb = get_mongo_db()


    @app.on_event("shutdown")
    async def shutdown_event():
        service_zeroconf.stop()
        await service_broadcast.stop()
        await close_mongo_db()
        #if app.mongodb_client:
        #    app.mongodb_client.close()
        #    print("Disconnected from MongoDB")



    app.include_router(api_router)
    app.include_router(ws_router)



    # create_admin_panel(app)

    add_pagination(app)

    return app
