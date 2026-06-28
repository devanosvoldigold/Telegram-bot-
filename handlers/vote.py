from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from game.manager import cast_vote


async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cast_vote(update, context)


vote_handler = CallbackQueryHandler(
    vote,
    pattern=r"^vote_"
)