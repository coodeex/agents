import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from git_mcp_handler import get_git_mcp_response

load_dotenv()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Get response from the git MCP handler
        response = await get_git_mcp_response(update.message.text)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Error processing request: {str(e)}")

token = os.getenv("GIT_MCP_TELEGRAM_BOT_TOKEN")
if not token:
    raise ValueError("Please set GIT_MCP_TELEGRAM_BOT_TOKEN in your .env file")

app = ApplicationBuilder().token(token).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot started. Ready to answer questions about the GitHub repository.")
app.run_polling() 