from game.state import game
from game.roles import get_wolf

WOLF_WIN = "Wolf"
WANDERER_WIN = "Forest Wanderers"


def check_winner():
    wolf = get_wolf()

    # Wolf has been voted/killed
    if wolf not in game.alive:
        return WANDERER_WIN

    # Count alive wanderers
    wanderers_alive = 0

    for player in game.alive:
        if player != wolf:
            wanderers_alive += 1

    # Wolf wins if no wanderers remain
    if wanderers_alive == 0:
        return WOLF_WIN

    # No winner yet
    return None