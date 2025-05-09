import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from parallel_handler import get_parallel_responses

load_dotenv()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the user's message
    user_message = update.message.text
    
    # Get responses from both models
    claude_response, openai_response = await get_parallel_responses(user_message)
    
    # Send responses with model identifiers
    await update.message.reply_text(f"OpenAI:\n{openai_response}")
    await update.message.reply_text(f"Claude:\n{claude_response}")

token = os.getenv("PARALLEL_AGENT_TELEGRAM_BOT_TOKEN")
app = ApplicationBuilder().token(token).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
