from broadcaster import Broadcast
import asyncio
import json
from fastapi import WebSocket
from core.utils.logger import HardwareMonitorLogger as Logger

logger = Logger(__name__).get_logger()

class BroadcastHandler:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.broadcast = Broadcast(redis_url)
        self.running = False
        self.tasks = []

    async def start(self):
        """Start broadcast service """
        await self.broadcast.connect()
        self.running = True
        logger.info("Broadcast service started")

    async def stop(self):
        """Stop braodcast service """
        await self.broadcast.disconnect()
        self.running = False
        logger.info("Broadcast service stopped")

    async def subscribe_to_topic(self, channel, websocket: WebSocket = None):
        """Get messages from a channel and send them to the websocket"""
        async with self.broadcast.subscribe(channel=channel) as subscriber:
            async for event in subscriber:
                if websocket:
                    await websocket.send_text(event.message)

    async def handle_websocket_agent_data(self, websocket: WebSocket, channel):
        """Get message from the websocket and send it to the channel"""
        async for message in websocket.iter_text():
            #try:
            #    data = json.loads(message)
            await self.broadcast.publish(channel=channel, message=message)
            await websocket.send_text(message)


service_broadcast = BroadcastHandler()