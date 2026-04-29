import asyncio, os
from telethon import TelegramClient, types

# Your Credentials
api_id = 31205231
api_hash = '6e5f53cc8aa3bf98959d722094e6c9b6'
save_path = '/sdcard/Download/'

if not os.path.exists(save_path):
    os.makedirs(save_path)

client = TelegramClient('my_session', api_id, api_hash)

# Progress bar function
def progress_callback(current, total):
    percentage = (current / total) * 100
    current_mb = current / (1024 * 1024)
    total_mb = total / (1024 * 1024)
    print(f'\rStatus: {percentage:.1f}% | {current_mb:.1f}MB of {total_mb:.1f}MB', end='')

async def main():
    await client.start()
    print("\n--- Telegram Multi-Media Downloader ---")
    
    raw_input = input("Link/Username: ").strip().strip('/')
    limit_in = input("How many media files? (default 5): ").strip()
    skip_in = input("How many media files to skip? (default 0): ").strip()
    
    limit = int(limit_in) if limit_in.isdigit() else 5
    skip = int(skip_in) if skip_in.isdigit() else 0
    start_msg_id = 0

    try:
        if 't.me/' in raw_input:
            parts = raw_input.split('/')
            if 'c' in parts:
                target_id = int('-100' + parts[parts.index('c') + 1])
                target = await client.get_entity(target_id)
                if parts[-1].isdigit():
                    start_msg_id = int(parts[-1]) + 1
            else:
                target_username = parts[-1]
                if target_username.isdigit():
                    start_msg_id = int(target_username) + 1
                    target_username = parts[-2]
                target = await client.get_entity(target_username)
        else:
            target = await client.get_entity(raw_input)

        print(f"Connected to: {target.title if hasattr(target, 'title') else 'Chat'}")
        
        count = 0
        async for msg in client.iter_messages(target, limit=None, offset_id=start_msg_id, add_offset=skip):
            if count >= limit:
                break
            
            if msg.media:
                m_type = "Photo" if msg.photo else "Video" if msg.video else "File"
                print(f"\n[{count+1}/{limit}] Downloading {m_type} (ID: {msg.id})...")
                
                # Downloading with progress bar
                await msg.download_media(file=save_path, progress_callback=progress_callback)
                
                count += 1
                print(f"\nDone!")

        print(f"\nAll tasks finished! Check your Download folder.")

    except Exception as e:
        print(f"\nError: {e}")

with client:
    client.loop.run_until_complete(main())

