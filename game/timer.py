import asyncio

from game.state import game
from game.manager import end_round


ROUND_TIME = 180  # 3 minutes


async def start_timer(context):
    while game.started:

        await context.bot.send_message(
            chat_id=game.group_id,
            text=(
                f"⏳ Round {game.day}\n\n"
                "You have 3 minutes to vote.\n"
                "The Wolf is choosing a victim..."
            )
        )

        await send_wolf_menu(context)

        await asyncio.sleep(ROUND_TIME)

        if not game.started:
            break

        await end_round(context)