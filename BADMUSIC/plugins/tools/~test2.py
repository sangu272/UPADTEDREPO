from pyrogram import Client, filters
import os
from yt_dlp import YoutubeDL
from BADMUSIC import app

# Video download function with cookies support
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Video save location
        'cookiefile': 'cookies/cookies.txt',  # Path to cookies file
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
        return file_path

# Handle /download command
@app.on_message(filters.command("vidmate") & filters.text)
async def handle_download(client, message):
    # Extract URL from the command
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a video link after the command. Example: `/download <video_url>`")
        return
    
    url = message.command[1]
    await message.reply_text("🔄 Downloading your video, please wait...")
    try:
        # Download video
        file_path = download_video(url)
        # Send video to the user
        await message.reply_video(video=file_path, caption="🎥 Here's your video!")
        # Cleanup downloaded file
        os.remove(file_path)
    except Exception as e:
        await message.reply_text(f"❌ Failed to download video. Error: {str(e)}")
