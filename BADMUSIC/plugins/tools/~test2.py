import os
from pyrogram import Client, filters
from pyrogram.types import Message
from BADMUSIC import app


# Folder to save downloaded songs
download_folder = "downloads"
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

@app.on_message(filters.command("down"))
async def download_song(client, message: Message):
    if message.reply_to_message and message.reply_to_message.document:
        # Check if the document is an MP3 file
        document = message.reply_to_message.document
        if document.mime_type == "audio/mpeg":
            # Get the file name and save path
            file_name = document.file_name
            file_path = os.path.join(download_folder, file_name)

            # Download the file
            await message.reply("Downloading your song... Please wait.")
            print(f"Downloading {file_name}...")

            # Download the file
            await message.reply_to_message.download(file_path)

            print(f"Downloaded {file_name} to {file_path}")
            await message.reply(f"Download complete! Song saved as {file_name}.")
        else:
            await message.reply("The file is not an MP3 song. Please reply to an MP3 file.")
    else:
        await message.reply("Please reply to an MP3 file to download it.")
