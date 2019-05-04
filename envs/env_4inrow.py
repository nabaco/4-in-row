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
        for j in range(self.boardW):
            for i in reversed(range(self.boardH)):
                if not self.board[i][j]:
                    moves.append((i, j))
        return moves

    def is_terminal_state(self):
        for player in [self.player1, self.player2]:
            if self.available_moves(player) == [] \
                    or self.player_status(player):
                return True

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
