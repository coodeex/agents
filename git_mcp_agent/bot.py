import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from git_mcp_handler import get_git_mcp_response

load_dotenv()

# Global variable to store the repository path
repo_path = None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global repo_path
    
    if not repo_path:
        # If repo_path is not set, assume this is the first message setting it
        repo_path = update.message.text
        await update.message.reply_text(f"Git repository path set to: {repo_path}")
        return

    try:
        # Get response from the git MCP handler
        response = await get_git_mcp_response(update.message.text, repo_path)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Error processing request: {str(e)}")

token = os.getenv("GIT_MCP_TELEGRAM_BOT_TOKEN")
if not token:
    raise ValueError("Please set GIT_MCP_TELEGRAM_BOT_TOKEN in your .env file")

app = ApplicationBuilder().token(token).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot started. Send the git repository path as the first message.")
app.run_polling() 