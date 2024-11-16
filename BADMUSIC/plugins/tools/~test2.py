from pyrogram import Client, filters
from collections import defaultdict
from BADMUSIC import app

@app.on_message(filters.command("download"))
async def download_media(client, message):
    if message.reply_to_message:
        # Download media from Telegram
        await app.download_media(message.reply_to_message)
        await message.reply("Media downloaded from Telegram!")
    else:
        # Handle other platform links
        link = message.text.split(" ", 1)[1]
        await download_from_other_platforms(link)

async def download_from_other_platforms(link):
    # Here you would implement the logic to download from Instagram, Facebook, YouTube, Pinterest
    # This could involve using requests or a specific library for each platform
    # Example: Use an API or library to fetch the video link and download it
    pass
