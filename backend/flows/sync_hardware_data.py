from prefect import flow, task
from crud.trigger import trigger_crud
from schemas.agent_data import AgentData
from bson import Binary
from core.db import get_db_session
from core.mongo_db import init_mongo_db, close_mongo_db, get_mongo_db
from core.utils.logger import HardwareMonitorLogger as Logger

from motor.motor_asyncio import AsyncIOMotorDatabase
from config import settings

from typing import Dict, Any



logger = Logger(__name__).get_logger()


def extract_value_from_json(data: Dict[str, Any], field: str) -> Any:
    """Extract value from nested JSON using dot notation."""
    keys = field.split('.')
    value = data
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key, None)
        else:
            return None
    return value


@task
async def fetch_existing_data(data: AgentData, mongodb: AsyncIOMotorDatabase):
    """Fetch existing data in MongoDB

    :param data: AgentData
    :param mongodb: MongoDB Session
    """
    agent_uuid = data.UUID
    uuid_binary = Binary(agent_uuid.bytes, subtype=0x04)
    query = {"UUID": uuid_binary}
    existing_doc = await mongodb["agents_data"].find_one(query)
    if existing_doc:
        existing_doc_copy = dict(existing_doc)
        existing_doc_copy["UUID"] = agent_uuid
        old_data = AgentData(**existing_doc_copy)
    else:
        old_data = None

    return old_data, data

@task
async def save_or_update_data(data: AgentData,
                              is_new: bool,
                              mongodb: AsyncIOMotorDatabase):
    """Save or update data in Mongo

    :param data: AgentData
    :param is_new: bool flag for new or existing data
    :param mongodb: MongoDB Session
    """
    agent_uuid = data.UUID
    uuid_binary = Binary(agent_uuid.bytes, subtype=0x04)
    query = {"UUID": uuid_binary}
    update = {"$set": data.dict()}
    if is_new:
        await mongodb["agents_data"].update_one(query, update, upsert=True)
    else:
        await mongodb["agents_data"].update_one(query, update)

@task
async def check_triggers(old_data: AgentData, new_data: AgentData):
    """Check if triggers exist for UUID AgentData

    :param old_data: AgentData
    :param new_data: AgentData
    """
    if old_data and new_data:
        Session = get_db_session()
        async with Session() as session:
            logger.info(f"Trying to get trigger for {new_data.UUID}")
            trigger = await trigger_crud.get_by_uuid(uuid=new_data.UUID, db_session=session)

            if trigger:

                old_data_dict = old_data.dict() if hasattr(old_data, 'dict') else old_data
                new_data_dict = new_data.dict() if hasattr(new_data, 'dict') else new_data

                old_value = extract_value_from_json(old_data_dict, trigger.field)
                new_value = extract_value_from_json(new_data_dict, trigger.field)

                if old_value is not None and new_value is not None:
                    if trigger.check_condition(new_value):
                        logger.info(f"Trigger condition met for {trigger.agent_uuid}")
                    else:
                        logger.info(f"Trigger condition not met for {trigger.agent_uuid}")
            else:
                logger.info(f"No trigger found for {new_data.UUID}")

@flow
async def process_agent_data(data: AgentData):
    """Flow to process data and check triggers"""
    await init_mongo_db(uri=settings.mongo_url, db_name=settings.MONGO_NAME)
    mongodb = get_mongo_db()
    if mongodb is None:
        logger.error("MongoDB connection failed")
        return
    try:
        old_data, new_data = await fetch_existing_data(data, mongodb)
        if old_data and new_data:
            await save_or_update_data(new_data, is_new=False, mongodb=mongodb)
            logger.info(f"Type old data - {type(old_data)}, type new data  - {type(new_data)}")
            await check_triggers(old_data=old_data, new_data=new_data)
        elif new_data:
            await save_or_update_data(new_data, is_new=True, mongodb=mongodb)

    except Exception as e:
        logger.error(f"Error processing agent data: {e}")

    finally:
        await close_mongo_db()






