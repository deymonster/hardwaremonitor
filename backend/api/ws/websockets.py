from typing import List
from broadcaster import Broadcast
import json
import anyio
from fastapi import WebSocket, WebSocketDisconnect, APIRouter, BackgroundTasks
from core.redis import redis_client
import logging
import asyncio
from core.utils.services.broadcast_service import service_broadcast

# Setup logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

ws_router = APIRouter()

#redis_url="redis://localhost:6379"
#broadcast = Broadcast(redis_url)

#broadcast.connect()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def receive_message(self, websocket: WebSocket):
        data = await websocket.receive_text()
        return data

agent_manager = ConnectionManager()
frontend_manager = ConnectionManager()


@ws_router.websocket("/ws/receiver")
async def websocket_agent(websocket: WebSocket):
    await agent_manager.connect(websocket)
    try:
        await service_broadcast.handle_websocket_agent_data(websocket=websocket, channel="agents")
    except WebSocketDisconnect:
        agent_manager.disconnect(websocket)
        logger.info("Client disconnected")

@ws_router.websocket("/ws/sender")
async def websocket_sender(websocket: WebSocket):
    await frontend_manager.connect(websocket)
    try:
        await service_broadcast.subscribe_to_topic(websocket=websocket, channel="agents")
    except WebSocketDisconnect:
        frontend_manager.disconnect(websocket)
        logger.info("Client disconnected")


@ws_router.websocket("/ws/agents")
async def websocket_connect(websocket: WebSocket, background_tasks: BackgroundTasks):
    await agent_manager.connect(websocket)
    agent_id = None
    try:
        while True:
            data = await agent_manager.receive_message(websocket)
            message = json.loads(data)
            agent_id = message.get("UUID")
            await redis_client.set(agent_id, json.dumps(message))
            await redis_client.publish("agents", json.dumps({agent_id: message}))
            await agent_manager.broadcast(f"Message text was: {data}")
            #logger.info(f"Message text was: {data} from {run_id}")

    except WebSocketDisconnect:
        agent_manager.disconnect(websocket)
        await agent_manager.broadcast(f"Client {agent_id} disconnected")

@ws_router.websocket("/ws/frontend")
async def websocket_frontend(websocket: WebSocket):
    await frontend_manager.connect(websocket)
    task = None
    try:
        async def reader():
            pubsub = redis_client.pubsub()
            await pubsub.subscribe("agents")
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    await frontend_manager.broadcast(message)

        task = asyncio.create_task(reader())
        while True:
            data = await frontend_manager.receive_message(websocket)
            message = json.loads(data)
            if message.get("action") == "get_keys":
                keys = await redis_client.keys('*')
                await frontend_manager.send_message(json.dumps(keys), websocket)
            elif message.get("action") == "get_value" and message.get("key"):
                key = message["key"]
                value = await redis_client.get(key)
                await websocket.send_text(json.dumps({"key": key, "value": value}))

    except WebSocketDisconnect:
        frontend_manager.disconnect(websocket)
        if task:
            task.cancel()





