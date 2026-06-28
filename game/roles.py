import random

from game.state import game


WOLF = "Wolf"
WANDERER = "Forest Wanderer"


def assign_roles():
    game.roles.clear()

    players = game.players[:]
    random.shuffle(players)

    wolf = random.choice(players)

    for player in players:
        if player == wolf:
            game.roles[player] = WOLF
        else:
            game.roles[player] = WANDERER

    game.alive = players[:]


def get_role(user_id):
    return game.roles.get(user_id)


def get_wolf():
    for user_id, role in game.roles.items():
        if role == WOLF:
            return user_id
    return None


def is_wolf(user_id):
    return game.roles.get(user_id) == WOLF


def is_alive(user_id):
    return user_id in game.alive


def eliminate_player(user_id):
    if user_id in game.alive:
        game.alive.remove(user_id)


def revive_player(user_id):
    if user_id not in game.alive:
        game.alive.append(user_id)


def alive_players():
    return game.alive[:]


def alive_count():
    return len(game.alive)


def clear_roles():
    game.roles.clear()
    game.alive.clear()