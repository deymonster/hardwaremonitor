from broadcaster import Broadcast, BroadcastBackend, Event
import asyncio
import json
from typing import Any, Tuple, Dict
from redis import asyncio as redis

from fastapi import WebSocket
from core.utils.logger import HardwareMonitorLogger as Logger

logger = Logger(__name__).get_logger()

StreamMessageType = Tuple[bytes, Tuple[Tuple[bytes, Dict[bytes, bytes]]]]

class CustomRedisStreamBackend(BroadcastBackend):
    # noinspection PyMissingConstructor
    def __init__(self, url: str, default_ttl: int = 60):
        url = url.replace("redis-stream", "redis", 1)
        self.streams: dict[str, str] = {}
        self._ready = asyncio.Event()
        self._producer = redis.Redis.from_url(url)
        self._consumer = redis.Redis.from_url(url)
        self.default_ttl = default_ttl  # Значение TTL по умолчанию

    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        await self._producer.aclose()
        await self._consumer.aclose()

    async def subscribe(self, channel: str) -> None:
        try:
            info = await self._consumer.xinfo_stream(channel)
            last_id = info["last-generated-id"]
        except redis.ResponseError:
            last_id = "0"
        self.streams[channel] = last_id
        self._ready.set()

    async def unsubscribe(self, channel: str) -> None:
        self.streams.pop(channel, None)

    async def publish(self, channel: str, message: Any) -> None:
        # Check if UUID is provided
        uuid = None
        if isinstance(message, str):
            message = json.loads(message)

        uuid = message.get("UUID")
        if not uuid:
            raise ValueError("UUID must be provided")
        serialized_message = {}
        for k, v in message.items():
            if isinstance(v, dict):
                serialized_message[k] = json.dumps(v)
            elif isinstance(v, list):
                serialized_message[k] = json.dumps(v)  # Преобразование списка в строку
            else:
                serialized_message[k] = v

        # Обновляем данные, если они уже существуют, или создаем новые
        if await self._producer.exists(str(uuid)):
            # Обновляем данные в HASH
            await self._producer.hset(str(uuid), mapping=serialized_message)
            action = "updated"
        else:
            # Создаем новый UUID с данными
            await self._producer.hset(str(uuid), mapping=serialized_message)
            action = "created"

        # Записываем в Stream для истории изменений
        await self._producer.xadd(channel, {
            "uuid": str(uuid),
            "action": action,
            "data": json.dumps(message)})
        # Устанавливаем TTL для потока (в миллисекундах)
        await self._producer.pexpire(channel, self.default_ttl * 1000)

    async def wait_for_messages(self) -> list[StreamMessageType]:
        await self._ready.wait()
        messages = None
        while not messages:
            messages = await self._consumer.xread(self.streams, count=1, block=100)
        return messages

    async def next_published(self) -> Event:
        messages = await self.wait_for_messages()
        stream, events = messages[0]
        _msg_id, message = events[0]
        self.streams[stream.decode("utf-8")] = _msg_id.decode("utf-8")
        return Event(
            channel=stream.decode("utf-8"),
            message=message.get(b"message", b"").decode("utf-8"),
        )

    async def get_agent_data(self, uuid: str) -> dict:
        """Get agent data by UUID"""
        data = await self._producer.hgetall(uuid)
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in data.items()} if data else None



class BroadcastHandler:
    def __init__(self, redis_url: str):
        self.backend = CustomRedisStreamBackend(redis_url, default_ttl=3600)
        self.broadcast = Broadcast(backend=self.backend)
        self.running = False


    async def start(self):
        """Start broadcast service """
        await self.broadcast.connect()
        self.running = True
        logger.info("Broadcast service started")

    async def stop(self):
        """Stop broadcast service """
        await self.broadcast.disconnect()
        self.running = False
        logger.info("Broadcast service stopped")

    async def subscribe_to_topic(self, channel: str, websocket: WebSocket = None):
        """Get messages from a channel and send them to the websocket or return them

        :param channel: str
        :param websocket: WebSocket
        """
        async with self.broadcast.subscribe(channel=channel) as subscriber:
            async for event in subscriber:
                if websocket:
                    await websocket.send_text(event.message)
                else:
                    return event.message

    async def publish_to_topic(self, channel: str, message: Any = None, websocket: WebSocket = None):
        """Publish message to a channel from a Websocket or directly

        :param channel: str
        :param message: Any
        :param websocket: WebSocket
        """
        if websocket:
            async for ws_message in websocket.iter_text():
                await self.broadcast.publish(channel=channel, message=ws_message)
                await websocket.send_text(ws_message)
        elif message:
            await self.broadcast.publish(channel=channel, message=message)



service_broadcast = BroadcastHandler(redis_url="redis-stream://localhost:6379/0")