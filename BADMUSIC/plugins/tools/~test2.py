from pyrogram import Client, filters
import requests
import re
from BADMUSIC import app

# Helper function to extract Pinterest video URL
def get_pinterest_video(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        matches = re.search(r'"contentUrl":"(https://v\.pinimg\.com/videos/[^"]+)"', response.text)
        if matches:
            return matches.group(1)
    return None

# Command to download Pinterest video
@app.on_message(filters.command("pinterest") & filters.private)
def download_pinterest_video(client, message):
    if len(message.command) < 2:
        message.reply_text("Please provide a Pinterest video link.\nUsage: `/pinterest <link>`")
        return

    url = message.command[1]
    message.reply_text("Fetching video...")

    try:
        video_url = get_pinterest_video(url)
        if video_url:
            message.reply_text("Uploading video...")
            client.send_video(message.chat.id, video=video_url, caption="Here is your video!")
        else:
            message.reply_text("Failed to retrieve video. Please check the link and try again.")
    except Exception as e:
        message.reply_text(f"An error occurred: {e}")
