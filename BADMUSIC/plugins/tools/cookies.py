import asyncio
import glob
import os
import random
from typing import Union

from pyrogram import filters

from BADMUSIC import app
from BADMUSIC.misc import SUDOERS


def get_random_cookie():
    folder_path = f"{os.getcwd()}/cookies"
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    return random.choice(txt_files)


async def check_cookies(video_url):
    cookie_file = get_random_cookie()
    opts = {
        "format": "bestaudio",
        "quiet": True,
        "cookiefile": cookie_file,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl.extract_info(video_url, download=False)
        return True
    except:
        return False


@app.on_message(
    filters.command(
        [
            "authstatus",
            "authtoken",
            "cookies",
            "cookie",
            "cookiesstatus",
            "cookiescheck",
        ]
    )
    & SUDOERS
)
async def list_formats(client, message):
    status_message = "sᴛᴀᴛᴜs⚣\n\n"
    status_message += "ᴄᴏᴏᴋɪᴇs⚣︎ ᴄʜᴇᴄᴋɪɴɢ ... "
    status_msg = await message.reply_text(status_message)

    cookie_status = await check_cookies("https://www.youtube.com/watch?v=LLF3GMfNEYU")
    status_message = "sᴛᴀᴛᴜs⚣\n\n"
    status_message += f"ᴄᴏᴏᴋɪᴇs⚣︎ {'✅ ᴀʟɪᴠᴇ' if cookie_status else '❌ ᴅᴇᴀᴅ'}"
    await status_msg.edit_text(status_message)

    use_token = await check_auth_token()
    status_message = "sᴛᴀᴛᴜs⚣︎\n\n"
    status_message += f"ᴄᴏᴏᴋɪᴇs⚣︎ {'✅ ᴀʟɪᴠᴇ' if cookie_status else '❌ ᴅᴇᴀᴅ'}\n"
    await status_msg.edit_text(status_message)
