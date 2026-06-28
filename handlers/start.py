from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🐺 <b>Welcome to Wolf Bot!</b>\n\n"
        "A social deduction game where one player is secretly the Wolf.\n\n"
        "<b>Commands</b>\n"
        "/create - Create a new game\n"
        "/join - Join a game\n"
        "/leave - Leave the lobby\n"
        "/startgame - Start the game (Host only)\n"
        "/help - Show this message"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📖 <b>Wolf Bot Help</b>\n\n"
        "1. Create a game using /create.\n"
        "2. Other players join using /join.\n"
        "3. The host starts the game with /startgame.\n"
        "4. Everyone votes every 3 minutes.\n"
        "5. The Wolf secretly chooses one player to kill.\n"
        "6. Eliminate the Wolf to win!"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )


start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help_command)