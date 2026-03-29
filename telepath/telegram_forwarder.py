import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("APP_ID"))
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")  # add this to .env
SOURCE_CHANNELS = os.getenv("SOURCE_CHANNELS", "").split(",")
DEST_CHANNEL = os.getenv("DEST_CHANNEL")

client = TelegramClient("forwarder_session", API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    await client.forward_messages(DEST_CHANNEL, event.message)
    print(f"Forwarded from {event.chat.username}: {event.message.id}")

print("Listening to all channels...")
client.start(phone=PHONE)
client.run_until_disconnected()