from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from game.manager import wolf_kill


async def wolf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await wolf_kill(update, context)


wolf_handler = CallbackQueryHandler(
    wolf,
    pattern=r"^kill_"
)