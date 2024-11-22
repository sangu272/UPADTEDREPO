import re
import requests
from pyrogram import filters
from BADMUSIC import app
from config import LOG_GROUP_ID


@app.on_message(filters.command(["pinterest"]))
async def download_pinterest_photo(client, message):
    # Check if the user provided a URL
    if len(message.command) < 2:
        await message.reply_text(
            "Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ Pɪɴᴛᴇʀᴇsᴛ ᴘʜᴏᴛᴏ URL ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ"
        )
        return

    # Extract the URL from the message
    url = message.text.split()[1]

    # Validate the URL format for Pinterest using regex
    if not re.match(
        re.compile(r"^(https?://)?(www\.)?(pinterest\.com)/.*$"), url
    ):
        return await message.reply_text(
            "Tʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ URL ɪs ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ Pɪɴᴛᴇʀᴇsᴛ URL😅😅"
        )
    
    # Notify user that the photo is being processed
    a = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")

    # API URL for Pinterest photo download
    api_url = f"https://pinterest-dl.hazex.workers.dev/?url={url}"

    try:
        # Send a GET request to the API
        response = requests.get(api_url)
        # Try to parse the JSON response
        result = response.json()

        # If the result has an error, notify the user
        if result["error"]:
            await a.edit("Fᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴘɪɴᴛᴇʀᴇsᴛ ᴘʜᴏᴛᴏ")
            return

        # If no error, extract the photo data
        data = result["result"]
        photo_url = data["url"]
        size = data["formattedSize"]
        type = data["extension"]

        # Format the caption with photo information
        caption = f"**Sɪᴢᴇ :** {size}\n**Tʏᴘᴇ :** {type}"

        # Remove processing message and send the photo
        await a.delete()
        await message.reply_photo(photo_url, caption=caption)

    except Exception as e:
        # If there's any error in the process, log it and notify the user
        error_message = f"Eʀʀᴏʀ :\n{e}"
        await a.delete()
        await message.reply_text("Fᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴘɪɴᴛᴇʀᴇsᴛ ᴘʜᴏᴛᴏ")
        
        # Log the error in the log group
        await app.send_message(LOG_GROUP_ID, error_message)
