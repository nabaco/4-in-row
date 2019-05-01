from .env_base import EnvironmentBase


class Env4InRow(EnvironmentBase):
    """
    An environment representing a 4-in-row game.
    Args:
        player1, player2: the players
        board_size (tuple): the size of the board.
            board_size[0]: height
            board_size[1]: width
    """

    def __init__(self, player1, player2, board_size):
        super(Env4InRow, self).__init__(player1, player2)
        self.board_size = board_size
        self.board = [[0] * board_size[0]] * board_size[1]

    def reset(self):
        self.board = [[0] * self.board_size[0]] * self.board_size[1]

    def apply_action(self, player, action):
        if action in self.available_moves(player):
            self.board[action[0]][action[1]] = player["symbol"]
            # next state, reward
            return self.board, 0
        print("Wrong action")

    def render(self):
        for i in self.board:
            print(i)

    def available_moves(self, player):
        pass

    def is_terminal_state(self):
        for player in [self.player1, self.player2]:
            if self.available_moves(player) is None \
                    or self.player_status(player) != 0:
                return True

    def player_status(self, player):
        pass
