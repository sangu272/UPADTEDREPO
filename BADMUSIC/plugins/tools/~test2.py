import os
import ffmpeg
from pyrogram import Client, filters
from pyrogram.types import Message
from BADMUSIC import app


# Path to store audio files
DOWNLOAD_DIR = "downloads/"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def bass_boost(input_file, output_file, boost_level=10):
    """Applies bass boost to an audio file using FFmpeg."""
    ffmpeg.input(input_file).output(
        output_file,
        af=f"bass=g={boost_level}",
        acodec="libmp3lame"
    ).run(overwrite_output=True)

@app.on_message(filters.command("bass") & filters.audio)
async def play_bass_boosted(_, message: Message):
    if not message.audio:
        await message.reply_text("Please reply to an audio file with the /play command!")
        return

    # Download the audio file
    file_path = await app.download_media(message.audio, DOWNLOAD_DIR)

    # Prepare the output file path
    output_file = os.path.join(DOWNLOAD_DIR, "bass_boosted.mp3")

    # Apply bass boost
    try:
        bass_boost(file_path, output_file, boost_level=10)
        await message.reply_audio(audio=output_file, caption="Here is your bass-boosted audio! 🔊")
    except Exception as e:
        await message.reply_text(f"Error processing audio: {str(e)}")
    finally:
        # Clean up files
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(output_file):
            os.remove(output_file)


