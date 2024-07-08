from broadcaster import Broadcast
import asyncio
from core.utils.logger import HardwareMonitorLogger as Logger

logger = Logger(__name__).get_logger()

class BroadcastHandler:
    def __init__(self, redis_url="redis://localhost:6379"):
        self.broadcast = Broadcast(redis_url)
        self.running = False
        self.tasks = []

    async def start(self):
        await self.broadcast.connect()
        self.running = True
        self.tasks.append(asyncio.create_task(self.subscribe_to_topics()))
        logger.info("Broadcast service started")

    async def stop(self):
        await self.broadcast.disconnect()
        self.running = False
        for task in self.tasks:
            task.cancel()
        logger.info("Broadcast service stopped")

    async def subscribe_to_topic(self, channel):
        async with self.broadcast.subscribe(channel=channel) as subscriber:
            async for event in subscriber:
                logger.info(f"Received message on {channel}: {event.message}")

    async def subscribe_to_topics(self):
        await asyncio.gather(
            self.subscribe_to_topic("agent_updates"),
            self.subscribe_to_topic("agent_alerts"),
        )


    async def send_update(self, data):
        await self.broadcast.publish(channel="agent_updates", message=data)

    async def send_alert(self, data):
        await self.broadcast.publish(channel="agent_alerts", message=data)
