from .env_base import Environment
IN_ROW = 4
RED = "\033[31m⬤\033[30m"
YELLOW = "\033[93m⬤\033[30m"
DEFAULT = "\033[30m⬤\033[30m"


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
        self.board = [[0 for i in range(self.boardW)]
                      for j in range(self.boardH)]

    def reset(self):
        self.board = [[0 for i in range(self.boardW)]
                      for j in range(self.boardH)]
        return self.board

    def apply_action(self, player, action):
        if action in self.available_moves(player):
            for i in reversed(range(self.boardH)):
                if not self.board[i][action]:
                    self.board[i][action] = player
                    break
            # next state, reward
            return self.board, 0

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
                print("⃒", end="")
                if j == self.player1:
                    # Red
                    print(RED, end="")
                elif j == self.player2:
                    # Yellow
                    print(YELLOW, end="")
                else:
                    # Default - empty
                    print(DEFAULT, end="")
            print("⃒⃒\n", end="")
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
                if self.board[i][j] == symbol:
                    count += 1
                    if count == IN_ROW:
                        if symbol == player:
                            return 1
                        elif symbol:
                            return -1
                else:
                    symbol = self.board[i][j]
                    count = 1
            count = 0

        # col
        for j in range(self.boardW):
            for i in range(self.boardH):
                if self.board[i][j] == symbol:
                    count += 1
                    if count == IN_ROW:
                        if symbol == player:
                            return 1
                        elif symbol:
                            return -1
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
                if self.board[i][j] == symbol:
                    count += 1
                    if count == IN_ROW:
                        if symbol == player:
                            return 1
                        elif symbol:
                            return -1
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
                if self.board[i][j] == symbol:
                    count += 1
                    if count == IN_ROW:
                        if symbol == player:
                            return 1
                        elif symbol:
                            return -1
                else:
                    symbol = self.board[i][j]
                    count = 1
                i += 1
                j += 1
            count = 0

        return 0
