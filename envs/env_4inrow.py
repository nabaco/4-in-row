from .env_base import Environment
IN_ROW = 4


class Env4InRow(Environment):
    """
    An environment representing a 4-in-row game.
    Args:
        player1, player2: the players
        board_size (tuple): the size of the board.
            boardH: height
            boardW: width
    """

    def __init__(self, player1, player2, board_size):
        super(Env4InRow, self).__init__(player1, player2)
        self.player1 = player1
        self.player2 = player2
        self.boardH = board_size[0]
        self.boardW = board_size[1]
        self.board = [[0] * self.boardW] * self.boardH

    def reset(self):
        self.board = [[0] * self.boardW] * self.boardH
        return self.board

    def apply_action(self, player, action):
        if action in self.available_moves(player):
            self.board[action[0]][action[1]] = player
            # next state, reward
            return self.board, 0
        return None

    def render(self):
        for i in self.board:
            print(i)

    def available_moves(self, player):
        moves = []
        for i in range(self.boardW):
            for j in reversed(range(self.boardH)):
                if self.board[j][i] == 0:
                    moves.append((j, i))
        return moves

    def is_terminal_state(self):
        for player in [self.player1, self.player2]:
            if self.available_moves(player) == [] \
                    or self.player_status(player) != 0:
                return True

    def player_status(self, player):
        pass
