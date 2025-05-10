import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from voice_agent_handler import voice_response

load_dotenv()

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the voice message
    voice = await update.message.voice.get_file()
    
    # Download the voice file
    voice_file = await voice.download_as_bytearray()
    
    # Process the voice message and get response
    response_audio = await voice_response(voice_file)
    
    # Send the voice response back
    await update.message.reply_voice(
        voice=response_audio,
        caption="Here's my voice response!"
    )

# Initialize bot
token = os.getenv("VOICE_AGENT_TELEGRAM_BOT_TOKEN")
app = ApplicationBuilder().token(token).build()

# Add voice message handler
app.add_handler(MessageHandler(filters.VOICE, handle_voice))

# Run the bot
app.run_polling()
