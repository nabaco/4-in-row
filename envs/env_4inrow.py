import platform

from .env_base import Environment
from copy import deepcopy

IN_ROW = 4
if platform.system() == 'Windows':
    RED = "O"
    YELLOW = "X"
    DEFAULT = "⬤"
    DELIMITER = "|"
else:
    RED = "\033[31m⬤\033[30m"
    YELLOW = "\033[93m⬤\033[30m"
    DEFAULT = "\033[30m⬤\033[30m"
    DELIMITER = "⃒"


class Env4InRow(Environment):
    """
    An environment representing a 4-in-row game.
    Args:
        player1, player2: the players
        board_size (tuple): the size of the board.
            boardH: height
            boardW: width
    """
    SYMBOL_COLORS = {
        0: DEFAULT,
        'x': RED,
        'o': YELLOW
    }

    def __init__(self, player1, player2, board_size):
        super(Env4InRow, self).__init__(player1, player2)
        self.player1 = player1
        self.player2 = player2
        self.symbol2player = {
            0: None,
            'x': self.player1,
            'o': self.player2
        }
        self.player2symbol = {
            self.player1: 'x',
            self.player2: 'o'
        }
        self.boardH = board_size[0]
        self.boardW = board_size[1]
        self.board = [[0 for i in range(self.boardW)]
                      for j in range(self.boardH)]
        self.current_player = player1

    def reset(self):
        self.board = [[0 for i in range(self.boardW)]
                      for j in range(self.boardH)]
        self.current_player = self.player1
        return self.board

    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 \
            else self.player1

    def get_symbol(self, player):
        return self.player2symbol[player]

    def apply_action(self, player, action):
        if action == 'pass':
            self.switch_player()
            return self.board, 0
        if self.current_player != player:
            # Not players turn - his move is illegal.
            return None
        symbol = self.get_symbol(player)
        if action in self.available_moves(player):
            for i in reversed(range(self.boardH)):
                if not self.board[i][action]:
                    self.board[i][action] = symbol
                    self.switch_player()
                    break
            # next state, reward
            return self.board, 0
        # Illegal move.
        return None

    def render(self):
        print(" ", end="")
        for r in range(self.boardW):
            print("{:1d} ".format(r), end="")
        print()
        count = 0
        for i in self.board:
            # print("_" * (self.boardW * 2 + 1))
            print(str(count), end="")
            count += 1
            for j in i:
                print("%s%s" % (DELIMITER, Env4InRow.SYMBOL_COLORS[j]), end="")
            print("%s\n" % DELIMITER, end="")
        # print("_" * (self.boardW * 2 + 1))

    def available_moves(self, player):
        moves = []
        if not self.player_status(player) and not self.is_terminal_state():
            moves = [j for j in range(self.boardW) if not self.board[0][j]]
        return moves

    def is_terminal_state(self):
        status = False
        if all(cell for cell in self.board[0])\
                or self.player_status(self.player1)\
                or self.player_status(self.player2):
            status = True
        return status

    def player_status(self, player):

        # initialize var
        symbol = 0
        count = 0

        # row
        for i in range(self.boardH):
            for j in range(self.boardW):
                if self.board[i][j] == symbol and symbol:  # we only increment whenever the cell isn't empty
                    count += 1
                    if count == IN_ROW:
                        return 1 if self.symbol2player[symbol] == player else -1
                else:
                    symbol = self.board[i][j]
                    count = 1
            count = 0

        # col
        for j in range(self.boardW):
            for i in range(self.boardH):
                if self.board[i][j] == symbol and symbol:  # we only increment whenever the cell isn't empty
                    count += 1
                    if count == IN_ROW:
                        return 1 if self.symbol2player[symbol] == player else -1
                else:
                    symbol = self.board[i][j]
                    count = 1
            count = 0

        # left-down diagonal
        for k in range(IN_ROW - 1, self.boardW + self.boardH - IN_ROW):
            if k < self.boardW:
                i = 0
                j = k
            else:
                i = k - self.boardW + 1
                j = self.boardW - 1
            while i < self.boardH and j >= 0:
                if self.board[i][j] == symbol and symbol:  # we only increment whenever the cell isn't empty
                    count += 1
                    if count == IN_ROW:
                        return 1 if self.symbol2player[symbol] == player else -1
                else:
                    symbol = self.board[i][j]
                    count = 1
                i += 1
                j -= 1
            count = 0

        # right-down diagonal
        for k in range(-self.boardH + IN_ROW, self.boardW - IN_ROW + 1):
            if k < 0:
                i = -k
                j = 0
            else:
                i = 0
                j = k
            while i < self.boardH and j < self.boardW:
                if self.board[i][j] == symbol and symbol:  # we only increment whenever the cell isn't empty
                    count += 1
                    if count == IN_ROW:
                        return 1 if self.symbol2player[symbol] == player else -1
                else:
                    symbol = self.board[i][j]
                    count = 1
                i += 1
                j += 1
            count = 0

        return 0

    def get_observation(self):
        return self.board

    def copy(self):
        result = Env4InRow(self.player1, self.player2, (self.boardH, self.boardW))
        result.current_player = self.current_player
        result.board = deepcopy(self.board)
        return result
