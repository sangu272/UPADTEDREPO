import os
import asyncio
import time
import requests
from urllib.parse import urlparse
from pyrogram import Client, filters
from pyrogram.types import Message
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
from BADMUSIC import app

# Define a dictionary to track the last message timestamp for each user
user_last_message_time = {}
user_command_count = {}
# Define the threshold for command spamming (e.g., 2 commands within 5 seconds)
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5

# Path to the cookies file (ensure you have the cookies.txt file in the same directory or provide the full path)
COOKIES_FILE = 'cookies/cookies.txt'


def get_text(message: Message) -> str:
    """Extract Text From Commands"""
    if message.text is None or len(message.text.split()) <= 1:
        return None
    return message.text.split(None, 1)[1]


@app.on_message(filters.command("video"))
async def download_video(_, message: Message):
    user_id = message.from_user.id
    current_time = time.time()

    # Spam protection
    last_message_time = user_last_message_time.get(user_id, 0)
    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            await message.reply_text(f"**{message.from_user.mention} ᴘʟᴇᴀsᴇ ᴅᴏɴᴛ ᴅᴏ sᴘᴀᴍ, ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 sᴇᴄ**")
            return
    else:
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    # Get the video search query from the message
    query = get_text(message)
    if not query:
        await message.reply_text("Please provide a valid song name or URL to search.")
        return

    # Notify user about the search
    await message.reply_text("🔄 **Searching for video... Please wait.**")

    # Search for the video on YouTube
    search = SearchVideos(query, offset=1, mode="dict", max_results=1)
    search_result = search.result()
    if not search_result["search_result"]:
        await message.reply_text("😴 **No video found! Please make sure the query is correct.**")
        return

    # Extract video details
    video_info = search_result["search_result"][0]
    video_url = video_info["link"]
    video_title = video_info["title"]
    video_id = video_info["id"]
    video_channel = video_info["channel"]
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

    # Download video thumbnail
    thumbnail_path = f"{video_id}_thumbnail.jpg"
    await asyncio.to_thread(requests.get, thumbnail_url, allow_redirects=True)

    # Define the download options
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "cookiefile": COOKIES_FILE,  # Path to your cookies.txt file
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",  # Set a user agent
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": f"{video_id}.mp4",  # Save the file as video_id.mp4
        "logtostderr": False,
        "quiet": True,
    }

    # Download the video using yt_dlp
    try:
        with YoutubeDL(opts) as ydl:
            ydl_data = ydl.extract_info(video_url, download=True)
            video_file = f"{ydl_data['id']}.mp4"
    except Exception as e:
        await message.reply_text(f"**Failed to download video. Error:** `{str(e)}`")
        return

    # Send the downloaded video to the user
    caption = f"❄ **Title:** [{video_title}]({video_url})\n💫 **Channel:** {video_channel}\n✨ **Searched:** {query}\n🥀 **Requested by:** {message.from_user.mention}"

    await message.reply_video(
        video=open(video_file, "rb"),
        caption=caption,
        thumb=thumbnail_path,
        supports_streaming=True
    )

    # Clean up downloaded files (video and thumbnail)
    os.remove(video_file)
    os.remove(thumbnail_path)

__MODULE__ = "sᴏɴɢs"
__HELP__ = """ 

## sᴏɴɢs/ sᴏɴɢ ᴍᴘ3 ᴠɪᴅᴇᴏ ᴍᴘ4 ᴅᴏᴡɴʟᴀᴏᴅ.

/song ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴍᴘ3 ꜱᴏɴɢ ᴅᴏᴡɴʟᴏᴀᴅ.
/video ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏ ꜱᴏɴɢ.
/shorts ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ sʜᴏʀᴛs ᴠɪᴅᴇᴏ.
""" 
