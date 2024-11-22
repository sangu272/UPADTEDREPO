from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup
from BADMUSIC import app

def get_pinterest_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        meta = soup.find("meta", {"property": "og:video"})
        if meta:
            return meta.get("content")  # Video URL
        meta = soup.find("meta", {"property": "og:image"})
        if meta:
            return meta.get("content")  # Image URL
    return None

@app.on_message(filters.command("pinterest") & filters.private)
def pinterest_handler(client, message):
    if len(message.command) < 2:
        message.reply_text("Please provide a Pinterest link. Usage: `/pinterest <link>`")
        return

    pinterest_url = message.command[1]
    content_url = get_pinterest_content(pinterest_url)

    if content_url:
        message.reply_text("Downloading content...")
        client.send_document(
            message.chat.id,
            content_url,
            caption="Here is your Pinterest content!",
        )
    else:
        message.reply_text("Failed to retrieve content. Please ensure the link is correct.")
