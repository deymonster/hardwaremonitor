from broadcaster import Broadcast
import asyncio

redis_url = "redis://localhost:6379/"



async def send_message_to_topic():
    broadcaster = Broadcast(redis_url)
    try:
        await broadcaster.connect()
        print("Connected to redis")

        await broadcaster.publish(channel="agent_updates", message="Hello from Agent!")
        print("Message published to channel")
    except Exception as e:
        print(f"Failed to connect or send messages: {e}")

    finally:
        await broadcaster.disconnect()

asyncio.run(send_message_to_topic())