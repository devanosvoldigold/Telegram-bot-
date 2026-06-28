import asyncio

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from game.manager import (
    create_game,
    join_game,
    leave_game,
    start_game,
)

from game.timer import start_timer
from game.state import game


async def create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await create_game(update, context)


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await join_game(update, context)


async def leave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await leave_game(update, context)


async def startgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_game(update, context)

    if game.started:
        if game.timer_task is None:
            game.timer_task = asyncio.create_task(
                start_timer(context)
            )


create_handler = CommandHandler("create", create)
join_handler = CommandHandler("join", join)
leave_handler = CommandHandler("leave", leave)
startgame_handler = CommandHandler("startgame", startgame)