class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.host = None
        self.group_id = None

        self.started = False
        self.day = 1

        self.players = []
        self.player_names = {}

        self.roles = {}
        self.alive = []

        self.votes = {}
        self.wolf_target = None

        self.timer_task = None


game = GameState()