from typing import List
from bson import Binary

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import LimitOffsetParams
from sqlmodel import col, select

from core.exceptions import NotFound
from core.utils.services.broadcast_service import service_broadcast
from deps.mongo_db import get_mongo_db
from schemas.agent_data import AgentData
from schemas.response import IResponsePaginated
from core.utils.logger import HardwareMonitorLogger as Logger
from pymongo.errors import PyMongoError

from services.agent_data import AgentTriggerService

logger = Logger(__name__).get_logger()

router = APIRouter(
    generate_unique_id_function=lambda route: f"agent_data_{route.name}",
)

@router.post(
    path=""
)
async def create(
    payload: AgentData,
    mongodb=Depends(get_mongo_db)
):
    try:
        await AgentTriggerService.run_agent_trigger(data=payload)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    #try:
    #    agent_uuid = payload.UUID
    #    logger.info(f"Creating data for UUID {agent_uuid}")

    #    uuid_binary = Binary(agent_uuid.bytes, subtype=0x04)
    #   query = {"UUID": uuid_binary}
    #    existing_doc = await mongodb["agents_data"].find_one(query)


    #    if existing_doc:
    #        logger.info(f"Found existing data for UUID {agent_uuid}")
    #        update = {"$set": payload.dict()}
    #        result = await mongodb["agents_data"].update_one(query, update)

    #        if result.matched_count > 0 and result.modified_count > 0:
    #            logger.info(f"Data updated for UUID {agent_uuid}")
    #            message = "Data updated in MongoDB"
    #        else:
    #            logger.info(f"No changes to data for UUID {agent_uuid}")
    #            message = "No changes to data in MongoDB"
    #    else:
    #        logger.info(f"New data for UUID {agent_uuid}")
    #        update = {"$set": payload.dict()}
    #        result = await mongodb["agents_data"].update_one(query, update, upsert=True)
    #        message = "New data inserted into MongoDB"

    #    return {"status": "success", "message": message}


    #except PyMongoError as e:
    #    logger.error(f"Error saving data to MongoDB: {e}")
    #    raise HTTPException(
    #        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #        detail="Failed to save data")


@router.get(
    path="/list",
    response_model=List[AgentData]
)
async def get_list(
    mongodb=Depends(get_mongo_db)
):
    try:
        cursor = mongodb["agents_data"].find()
        records = []
        async for record in cursor:
            record = AgentData(**record)
            records.append(record)
        return records
    except PyMongoError as e:
        logger.error(f"Error retrieving data from MongoDB: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve data")
