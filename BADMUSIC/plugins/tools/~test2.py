import re
import requests
from pyrogram import filters
from BADMUSIC import app
from config import LOG_GROUP_ID

# Command for Pinterest photo/video download
@app.on_message(filters.command(["pinterest", "pin"]))
async def download_pinterest_media(client, message):
    # Check if the user provided a URL
    if len(message.command) < 2:
        await message.reply_text(
            "Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ Pɪɴᴛᴇʀᴇsᴛ URL ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ"
        )
        return

    # Extract the URL from the message
    url = message.text.split()[1]

    # Validate the URL format for Pinterest using regex
    if not re.match(
        re.compile(r"^(https?://)?(www\.)?pinterest\.(com|co)/.*$"), url
    ):
        return await message.reply_text(
            "Tʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ URL ɪs ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ Pɪɴᴛᴇʀᴇsᴛ URL😅"
        )
    
    # Notify user that the media is being processed
    a = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")

    # API URL for Pinterest media download (This is a placeholder API)
    api_url = f"https://api.pinterest.com/v1/media?url={url}"  # Replace with a working API or scraping method

    try:
        # Send a GET request to the API or service
        response = requests.get(api_url, timeout=10)
        
        # Check if the request was successful (status code 200)
        if response.status_code != 200:
            await a.edit("Fᴀɪʟᴇᴅ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴛʜᴇ ᴀᴘɪ.")
            return

        # Try to parse the JSON response (assuming the API gives a JSON with media data)
        result = response.json()

        # If the result has an error, notify the user
        if result.get("error"):
            await a.edit("Fᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ Pɪɴᴛᴇʀᴇsᴛ ᴍᴇᴅɪᴀ")
            return

        # If no error, extract the media data (image or video URL)
        media_url = result["media_url"]  # Assuming "media_url" holds the media URL
        media_type = result["type"]  # Image or Video
        description = result.get("description", "No description available")

        # Handle sending the correct media type (Image or Video)
        if media_type == "image":
            # Send the image
            await a.delete()
            await message.reply_photo(media_url, caption=description)
        elif media_type == "video":
            # Send the video
            await a.delete()
            await message.reply_video(media_url, caption=description)
        else:
            await a.delete()
            await message.reply_text("Tʜᴇ ᴍᴇᴅɪᴀ ᴄᴏᴜʟᴅ ɴᴏᴛ ʙᴇ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ.")

    except requests.exceptions.Timeout:
        # Handle timeout errors
        error_message = "Tʜᴇ ᴀᴘɪ ᴛɪᴇᴅ ᴏᴜᴛ. Pʟᴇᴀsᴇ ᴛʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ."
        await a.delete()
        await message.reply_text(error_message)

    except requests.exceptions.RequestException as e:
        # Handle other request-related errors
        error_message = f"Request Error: {str(e)}"
        await a.delete()
        await message.reply_text("Fᴀɪʟᴇᴅ ᴛᴏ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴛʜᴇ ᴀᴘɪ.")

        # Log the error in the log group
        await app.send_message(LOG_GROUP_ID, error_message)

    except Exception as e:
        # Handle any other unexpected errors
        error_message = f"Unexpected Error: {str(e)}"
        await a.delete()
        await message.reply_text("Fᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ Pɪɴᴛᴇʀᴇsᴛ ᴍᴇᴅɪᴀ")

        # Log the error in the log group
        await app.send_message(LOG_GROUP_ID, error_message)
