from telethon import TelegramClient, events
from config.env import get_env

API_ID = get_env("APP_ID")
API_HASH = get_env("API_HASH")

SOURCE_CHANNELS = get_env("SOURCE_CHANNELS", "").split(",")
DEST_CHANNEL = get_env("DEST_CHANNEL")

client = TelegramClient("forwarder_session", API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    await client.forward_messages(DEST_CHANNEL, event.message)
    print(f"Forwarded from {event.chat.username}: {event.message.id}")

print("Listening to all channels...")
client.start()
client.run_until_disconnected()