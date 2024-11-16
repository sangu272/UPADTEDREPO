from BADMUSIC import app
from pyrogram import Client, filters
import asyncio
from pyrogram import *


@app.on_message(filters.text)
def handle_message(client, message):
    if message.edit_date:
        # This is an edited message
        print("Edited message:", message.text)
