import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('HELLO!!')

token = os.getenv("PARALLEL_AGENT_TELEGRAM_BOT_TOKEN")
app = ApplicationBuilder().token(token).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
