from BADMUSIC import app
from pyrogram import Client, filters

@app.on_message(filters.command("create_group"))
def create_group(client, message):
    group_name = "My New Group"  # You can customize the group name
    try:
        # Create a new group
        new_group = client.create_group(group_name, [message.from_user.id])
        message.reply_text(f"Group '{new_group.title}' created successfully!")
    except Exception as e:
        message.reply_text(f"Failed to create group: {str(e)}")
