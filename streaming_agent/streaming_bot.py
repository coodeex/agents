import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from streaming_handler import get_streaming_response, StreamingState

load_dotenv()

async def update_message(message_obj, new_text: str) -> bool:
    """
    Update the message text while preserving any markdown.
    Returns True if update was successful, False otherwise.
    """
    try:
        await message_obj.edit_text(
            new_text or "Thinking...",
            parse_mode='Markdown'
        )
        return True
    except Exception as e:
        if "Message is not modified" not in str(e):
            print(f"Error updating message: {e}")
        return False

async def periodic_message_updater(message_obj, state: StreamingState):
    """Periodically update the message with accumulated text"""
    last_text = ""
    
    while not state.is_complete:
        async with state.lock:
            current_text = state.text
        
        if current_text != last_text:
            success = await update_message(message_obj, current_text)
            if success:
                last_text = current_text
        
        await asyncio.sleep(1.0)  # Update every second
    
    # Final update to ensure we have the complete text
    async with state.lock:
        await update_message(message_obj, state.text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the user's message
    user_message = update.message.text
    
    # Send initial response
    response_message = await update.message.reply_text("Thinking...")
    
    # Create shared state
    state = StreamingState()
    
    # Start periodic updater task
    updater_task = asyncio.create_task(periodic_message_updater(response_message, state))
    
    # Get streaming response
    await get_streaming_response(user_message, state)
    
    # Wait for final update
    await updater_task

# Set up and run the bot
token = os.getenv("STREAMING_AGENT_TELEGRAM_BOT_TOKEN")
if not token:
    raise ValueError("STREAMING_AGENT_TELEGRAM_BOT_TOKEN not found in environment variables")

app = ApplicationBuilder().token(token).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling() 