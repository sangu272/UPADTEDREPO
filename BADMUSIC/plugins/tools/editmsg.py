from pyrogram import Client, filters
import asyncio

@app.on_message(filters.edited)
async def delete_edited_message(client, message):
    # Wait for a specified time (e.g., 10 seconds)
    await asyncio.sleep(10)
    await message.delete()
