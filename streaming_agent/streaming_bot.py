import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from streaming_handler import get_streaming_response

load_dotenv()

async def update_message(message_obj, new_text: str):
    """Update the message text while preserving any markdown"""
    try:
        await message_obj.edit_text(
            new_text,
            parse_mode='Markdown'
        )
    except Exception as e:
        # If markdown parsing fails, try without markdown
        try:
            await message_obj.edit_text(new_text)
        except Exception as e:
            print(f"Error updating message: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the user's message
    user_message = update.message.text
    
    # Send initial response
    response_message = await update.message.reply_text("Thinking...")
    
    # Create callback for streaming updates
    async def stream_callback(accumulated_text: str):
        await update_message(response_message, accumulated_text)
    
    # Get streaming response
    final_response = await get_streaming_response(user_message, stream_callback)

# Set up and run the bot
token = os.getenv("STREAMING_AGENT_TELEGRAM_BOT_TOKEN")
if not token:
    raise ValueError("STREAMING_AGENT_TELEGRAM_BOT_TOKEN not found in environment variables")

app = ApplicationBuilder().token(token).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling() 