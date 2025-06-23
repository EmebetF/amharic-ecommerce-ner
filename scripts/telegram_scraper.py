from telethon.sync import TelegramClient
import pandas as pd
import os

api_id = 28080028
api_hash = '09f4b66ec595578287e234cca9a5b54f'
phone = '+251923026799'  

# === Channels to scrape ===
channels = ['shageronlinestore'] 

# === Create Telegram client ===
client = TelegramClient('session_name', api_id, api_hash)

async def scrape_channel(channel):
    await client.start(phone)
    messages = []
    
    async for message in client.iter_messages(channel, limit=100):
        if message.message:  # skip empty or media-only messages
            messages.append({
                'channel': channel,
                'date': message.date,
                'sender_id': message.sender_id,
                'message': message.message,
                'views': message.views
            })

    return messages

async def main():
    all_data = []
    for channel in channels:
        print(f"Scraping: {channel}")
        data = await scrape_channel(channel)
        all_data.extend(data)

    # Save to CSV
    df = pd.DataFrame(all_data)
    os.makedirs("./data", exist_ok=True)
    df.to_csv("./data/raw_telegram_messages.csv", index=False)
    print("Saved to ./data/raw_telegram_messages.csv")

with client:
    client.loop.run_until_complete(main())
