from telegram.ext import Application

from config import BOT_TOKEN

from handlers.start import start_handler, help_handler
from handlers.game import (
    create_handler,
    join_handler,
    leave_handler,
    startgame_handler,
)
from handlers.vote import vote_handler
from handlers.wolf import wolf_handler


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Start & Help
    app.add_handler(start_handler)
    app.add_handler(help_handler)

    # Game Commands
    app.add_handler(create_handler)
    app.add_handler(join_handler)
    app.add_handler(leave_handler)
    app.add_handler(startgame_handler)

    # Callback Queries
    app.add_handler(vote_handler)
    app.add_handler(wolf_handler)

    print(r"""
██╗    ██╗ ██████╗ ██╗     ███████╗
██║    ██║██╔═══██╗██║     ██╔════╝
██║ █╗ ██║██║   ██║██║     █████╗
██║███╗██║██║   ██║██║     ██╔══╝
╚███╔███╔╝╚██████╔╝███████╗██║
 ╚══╝╚══╝  ╚═════╝ ╚══════╝╚═╝

      🐺  W O L F   B O T  🐺

╭──────────────────────────────────╮
│  🟢 STATUS     : ONLINE          │
│  👑 CREATOR    : DevanosVoldigold│
╰──────────────────────────────────╯
""")

    app.run_polling()


if __name__ == "__main__":
    main()