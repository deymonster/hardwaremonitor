from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING
from pymongo.errors import PyMongoError
from core.utils.logger import HardwareMonitorLogger as Logger

logger = Logger(__name__).get_logger()

mongo_client: AsyncIOMotorClient | None = None
mongo_db = None

async def init_mongo_db(uri: str, db_name: str):
    """Init mongo DB Session

    :param uri: MongoDB URI
    :param db_name: Database name
    """
    global mongo_client, mongo_db
    mongo_client = AsyncIOMotorClient(uri, uuidRepresentation='standard')
    mongo_db = mongo_client[db_name]
    try:
        await mongo_db["agents_data"].create_index([("UUID", ASCENDING)])
        logger.info("Index created")
    except PyMongoError as e:
        logger.error(f"Error creating index - {e}")

async def close_mongo_db():
    """Close mongo DB Session
    """
    global mongo_client, mongo_db
    if mongo_client:
        mongo_client.close()
        mongo_client = None
        mongo_db = None

def get_mongo_db():
    """Get mongo DB Session

    :return: MongoDB Session
    """
    return mongo_db

