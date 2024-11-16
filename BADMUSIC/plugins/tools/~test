from BADMUSIC import app
from pyrogram import Client, filters

# Flag to enable/disable auto reactions
auto_react_enabled = True

# Emoji to react with
react_emoji = "❤️"

# Command to toggle auto reactions
@app.on_message(filters.command("react_off"))
async def turn_off_react(client, message):
    global auto_react_enabled
    auto_react_enabled = False
    await message.reply("Auto reactions turned off.")

@app.on_message(filters.command("react_on"))
async def turn_on_react(client, message):
    global auto_react_enabled
    auto_react_enabled = True
    await message.reply("Auto reactions turned on.")

# Auto react to incoming messages
@app.on_message(filters.text)
async def auto_react(client, message):
    if auto_react_enabled:
        await message.react(react_emoji)

# Run the bot
