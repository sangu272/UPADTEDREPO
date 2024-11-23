from pyrogram import Client, filters
import os


# Directory to save photos
SAVE_DIR = "saved_photos"
os.makedirs(SAVE_DIR, exist_ok=True)

@Client.on_message(filters.self_destruction, group=6)
def save_timer_photos(client, message):
    """
    This function will save photo messages automatically.
    """
    try:
        # Get sender information
        chat_name = message.chat.title if message.chat.title else message.chat.username or "private_chat"
        
        # Save photo
        file_path = os.path.join(SAVE_DIR, f"{chat_name}_{message.photo.file_unique_id}.jpg")
        message.download(file_path)
        
        print(f"Photo saved: {file_path}")
    except Exception as e:
        print(f"Error saving photo: {e}")
