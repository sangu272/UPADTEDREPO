from BADMUSIC import app
from pyrogram import Client, filters

@app.on_message(filters.command("re"))
async def toggle_reaction(client, message):
    global auto_react_enabled
    auto_react_enabled = not auto_react_enabled
    status = "enabled" if auto_react_enabled else "disabled"
    await message.reply(f"Auto reactions are now {status}.")
