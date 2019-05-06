from .env_base import EnvironmentBase
IN_ROW = 4


class Env4InRow(EnvironmentBase):
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
        self.board = [[0 for i in range(self.boardW)] for j in range(self.boardH)]

    def reset(self):
        self.board = [[0 for i in range(self.boardW)] for j in range(self.boardH)]
        return self.board

    def apply_action(self, player, action):
        for a in self.available_moves(player):
            if action == a[1]:
                self.board[a[0]][a[1]] = player
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
                    print("\033[31m⬤\033[30m", end="")
                elif j == self.player2:
                    # Yellow
                    print("\033[93m⬤\033[30m", end="")
                else:
                    print("\033[30m⬤\033[30m", end="")
            print("⃒⃒\n", end="")
        # print("_" * (self.boardW * 2 + 1))

    def available_moves(self, player):
        moves = []
        if self.player_status(player) == 0 and not self.is_terminal_state():
            for j in range(self.boardW):
                for i in reversed(range(self.boardH)):
                    if not self.board[i][j]:
                        moves.append((i, j))
                        break
        return moves

    def is_terminal_state(self):
        status = True
        for i in range(self.boardW):
            if self.board[self.boardH-1][i] == 0:
                status = None
                break
        return status

    def player_status(self, player):
        # Iteration on each cell
        for i in reversed(range(self.boardH)):
            for j in range(self.boardW):

                # check if not zero and remember the cell symbol
                if self.board[i][j]:
                    symbol = self.board[i][j]

                    # check four in row: up
                    if (i-IN_ROW+1) >= 0 \
                            and all(self.board[i-k][j] == symbol for k in range(1, IN_ROW)):
                        if symbol == player:
                            return 1
                        else:
                            return -1

                    # check four in row: up-right
                    if (i-IN_ROW+1) >= 0 \
                            and (j+IN_ROW-1) < self.boardW \
                            and all(self.board[i-k][j+k] == symbol for k in range(1, IN_ROW)):
                        if symbol == player:
                            return 1
                        else:
                            return -1

                    # check four in row: right
                    if (j+IN_ROW-1) < self.boardW \
                            and all(self.board[i][j+k] == symbol for k in range(1, IN_ROW)):
                        if symbol == player:
                            return 1
                        else:
                            return -1

                    # check four in row: down-right
                    if (i+IN_ROW-1) < self.boardH \
                            and (j+IN_ROW-1) < self.boardW \
                            and all(self.board[i+k][j+k] == symbol for k in range(1, IN_ROW)):
                        if symbol == player:
                            return 1
                        else:
                            return -1
        return 0
