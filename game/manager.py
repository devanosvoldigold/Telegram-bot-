from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from game.state import game
from game.roles import assign_roles, get_role
from game.winner import check_winner



async def create_game(update, context):
    if game.started:
        await update.message.reply_text(
            "❌ A game is already running."
        )
        return

    if game.host is not None:
        await update.message.reply_text(
            "❌ A lobby already exists."
        )
        return

    user = update.effective_user

    game.host = user.id
    game.group_id = update.effective_chat.id

    game.players.append(user.id)
    game.player_names[user.id] = user.first_name

    await update.message.reply_text(
        f"🐺 {user.first_name} created a Wolf game!\n\n"
        "Use /join to join.\n"
        "Minimum players: 5"
    )



async def join_game(update, context):
    if game.host is None:
        await update.message.reply_text(
            "❌ No lobby exists.\nUse /create first."
        )
        return

    if game.started:
        await update.message.reply_text(
            "❌ The game has already started."
        )
        return

    user = update.effective_user

    if user.id in game.players:
        await update.message.reply_text(
            "❌ You already joined."
        )
        return

    game.players.append(user.id)
    game.player_names[user.id] = user.first_name

    await update.message.reply_text(
        f"✅ {user.first_name} joined!\n"
        f"Players: {len(game.players)}"
    )



async def leave_game(update, context):
    if game.host is None:
        await update.message.reply_text(
            "❌ No active lobby."
        )
        return

    if game.started:
        await update.message.reply_text(
            "❌ You can't leave after the game starts."
        )
        return

    user = update.effective_user

    if user.id not in game.players:
        await update.message.reply_text(
            "❌ You aren't in the lobby."
        )
        return

    game.players.remove(user.id)
    game.player_names.pop(user.id, None)

    if user.id == game.host:
        game.reset()

        await update.message.reply_text(
            "❌ Host left.\nLobby closed."
        )
        return

    await update.message.reply_text(
        f"👋 {user.first_name} left.\n"
        f"Players: {len(game.players)}"
    )



async def start_game(update, context):
    if game.started:
        await update.message.reply_text(
            "❌ Game already started."
        )
        return

    if update.effective_user.id != game.host:
        await update.message.reply_text(
            "❌ Only the host can start."
        )
        return

    if len(game.players) < 5:
        await update.message.reply_text(
            "❌ At least 5 players are required."
        )
        return

    game.started = True

    assign_roles()

    for player in game.players:
        role = get_role(player)

        try:
            await context.bot.send_message(
                chat_id=player,
                text=f"🎭 Your role is:\n\n{role}"
            )
        except:
            pass

    keyboard = []

    for player in game.players:
        keyboard.append([
            InlineKeyboardButton(
                game.player_names[player],
                callback_data=f"vote_{player}"
            )
        ])

    await context.bot.send_message(
        chat_id=game.group_id,
        text=(
            "🐺 The game has begun!\n\n"
            "Vote for who you think is the Wolf.\n"
            "The Wolf has received a private message."
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    

async def send_wolf_menu(context):
    from game.roles import get_wolf

    wolf = get_wolf()

    keyboard = []

    for player in game.alive:
        if player == wolf:
            continue

        keyboard.append([
            InlineKeyboardButton(
                game.player_names[player],
                callback_data=f"kill_{player}"
            )
        ])

    try:
        await context.bot.send_message(
            chat_id=wolf,
            text="🐺 Choose a player to kill.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except:
        pass



async def cast_vote(update, context):
    query = update.callback_query
    await query.answer()

    voter = query.from_user.id

    if voter not in game.alive:
        await query.answer(
            "You are dead.",
            show_alert=True
        )
        return

    target = int(query.data.split("_")[1])

    if target not in game.alive:
        await query.answer(
            "That player is already dead.",
            show_alert=True
        )
        return

    game.votes[voter] = target

    await query.answer(
        "✅ Vote submitted!"
    )



async def wolf_kill(update, context):
    from game.roles import get_wolf

    query = update.callback_query
    await query.answer()

    wolf = get_wolf()

    if query.from_user.id != wolf:
        await query.answer(
            "Only the Wolf can do this.",
            show_alert=True
        )
        return

    target = int(query.data.split("_")[1])

    if target not in game.alive:
        await query.answer(
            "Player already dead.",
            show_alert=True
        )
        return

    game.wolf_target = target

    await query.edit_message_text(
        f"🐺 You chose to kill {game.player_names[target]}."
    )



def get_voted_player():
    if not game.votes:
        return None

    results = {}

    for target in game.votes.values():
        results[target] = results.get(target, 0) + 1

    highest = max(results.values())

    winners = [
        player
        for player, votes in results.items()
        if votes == highest
    ]

    if len(winners) != 1:
        return None

    return winners[0]

from game.roles import (
    eliminate_player,
    get_wolf
)



async def end_round(context):
    voted_player = get_voted_player()
    wolf = get_wolf()

    message = "🌙 Round Over!\n\n"

    # Player voted out
    if voted_player is not None:
        eliminate_player(voted_player)

        message += (
            f"🗳 Voted Out: "
            f"{game.player_names[voted_player]}\n"
        )
    else:
        message += "🗳 Nobody was voted out.\n"


    if (
        game.wolf_target is not None
        and game.wolf_target in game.alive
    ):
        eliminate_player(game.wolf_target)

        message += (
            f"🐺 Killed: "
            f"{game.player_names[game.wolf_target]}\n"
        )
    else:
        message += "🐺 Nobody was killed.\n"

    await context.bot.send_message(
        chat_id=game.group_id,
        text=message
    )

    winner = check_winner()

    if winner:
        await context.bot.send_message(
            chat_id=game.group_id,
            text=f"🏆 {winner} wins!"
        )

        reset_game()
        return

    game.day += 1
    game.votes.clear()
    game.wolf_target = None

    keyboard = []

    for player in game.alive:
        keyboard.append([
            InlineKeyboardButton(
                game.player_names[player],
                callback_data=f"vote_{player}"
            )
        ])

    await context.bot.send_message(
        chat_id=game.group_id,
        text=(
            f"☀️ Day {game.day}\n\n"
            "Vote for who you think is the Wolf."
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await send_wolf_menu(context)



def reset_game():
    if game.timer_task:
        game.timer_task.cancel()
        game.timer_task = None

    game.reset()