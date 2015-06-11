class GameState:
    """
    The game state
    """
    def __init__(self, _game_sound=None, _game_gui=None):
        self.state = "welcome"
        self.gui = _game_gui
        self.players = []
        self.result = None

    def add_gui(self, _game_gui):
        """
        Provide an access to the game gui object
        """
        self.gui = _game_gui

    def reset(self):
        self.result = None
        self.players = []

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_result(self, val):
        self.result = val

    def get_result(self):
        return self.result
