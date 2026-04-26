import asyncio, os
from telethon import TelegramClient

api_id = 31205231
api_hash = '6e5f53cc8aa3bf98959d722094e6c9b6'
save_path = '/sdcard/Download/'

client = TelegramClient('my_session', api_id, api_hash)

async def main():
    await client.start()
    raw_input = input("Link/Username: ").strip()
    limit = int(input("Check limit: ") or 5)

    try:
        # লিংক প্রসেসিং
        if 't.me/c/' in raw_input:
            # প্রাইভেট চ্যানেলের জন্য
            chat_id = int('-100' + raw_input.split('/')[-2])
            target = await client.get_entity(chat_id)
        elif 't.me/' in raw_input:
            # পাবলিক চ্যানেলের জন্য
            target = raw_input.split('/')[-2] if '/' in raw_input.strip('/')[-1] else raw_input.split('/')[-1]
            if '_' in target and target.split('_')[-1].isdigit(): # হ্যান্ডলিং মেসেজ লিংক
                 target = raw_input.split('/')[-2]
            target = await client.get_entity(target)
        else:
            target = await client.get_entity(raw_input)

        print(f"Connected to: {target.title}")
        async for msg in client.iter_messages(target, limit=limit):
            if msg.media:
                print(f"Downloading ID: {msg.id}...")
                await msg.download_media(file=save_path)
                print(f"Success!")
    except Exception as e:
        print(f"Error: {e}")

with client:
    client.loop.run_until_complete(main())

