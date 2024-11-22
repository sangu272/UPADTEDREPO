import os
import youtube_dl
from pyrogram import Client, filters
from pyrogram.types import Message
from BADMUSIC import app


download_folder = "downloads"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# YouTube-DL options for downloading Instagram Reels
ydl_opts = {
    'format': 'best',  # Choose best quality
    'outtmpl': f'{download_folder}/%(id)s.%(ext)s',  # Save file as id.extension
    'quiet': False,  # Show progress info
}

@app.on_message(filters.command("reel") & filters.private)
async def download_reel(client, message: Message):
    if len(message.text.split()) < 2:
        await message.reply("Please provide the Instagram Reels link after the command, like this:\n`/download_reel <Instagram_Reel_URL>`")
        return

    reel_url = message.text.split()[1]

    try:
        # Download Instagram Reels using youtube-dl
        await message.reply("Downloading your Instagram Reel... Please wait.")

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(reel_url, download=True)
            filename = ydl.prepare_filename(info_dict)

        # Send the downloaded file to the user
        if os.path.exists(filename):
            await message.reply_document(filename)
            os.remove(filename)  # Delete the file after sending it to the user
        else:
            await message.reply("Failed to download the Reel. Please check the URL and try again.")

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
