import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from voice_agent_handler import voice_response
from pydub import AudioSegment
import io

load_dotenv()

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the voice message
    voice = await update.message.voice.get_file()
    
    # Download the voice file
    voice_file = await voice.download_as_bytearray()
    
    # Process the voice message and get response
    response_audio = await voice_response(voice_file)
    
    # Get duration of the response audio
    audio = AudioSegment.from_file(io.BytesIO(response_audio))
    duration = len(audio) / 1000.0  # Convert milliseconds to seconds
    
    print(f"Responding.. ")
    # Send the voice response back with duration
    await update.message.reply_voice(
        voice=response_audio,
        duration=int(duration)
    )

# Initialize bot
token = os.getenv("VOICE_AGENT_TELEGRAM_BOT_TOKEN")
app = ApplicationBuilder().token(token).build()

# Add voice message handler
app.add_handler(MessageHandler(filters.VOICE, handle_voice))

print("Voice agent bot started")
# Run the bot
app.run_polling()
