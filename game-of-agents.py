from envs import *
from agents import *
from itertools import product


def inrow_heuristic(env, player, weight=0):
    """
    Score system:
        win = inf
        loss = -inf
        array of some symbols without space to extend = 0
        array with 1 symbol = +/-1 = +/-1^5
        array with 2 symbols = +/-32 = +/-2^5
        array with 3 symbols = +/-243 = +/-3^5
    This scores growth if the array have multiply space to extend to!!!
    """
    # Check terminal state
    if env.is_terminal_state():
        if env.player_status(player) > 0:
            return float("inf")
        if env.player_status(player) < 0:
            return -float("inf")
        return 0

    score = 0
    directions = {"hor": (0, 1),
                  "ver": (1, 0),
                  "diag": (1, -1),
                  "re-diag": (1, 1),
                  }

    # Run on every empty cell
    for i in range(env.boardH):
        for j in range(env.boardW):
            if env.board[i][j] == 0:

                # Run in every direction
                for direc in directions:

                    # Run in positive and negative diraction of direct
                    counter_p = counter(
                        i, j, env, directions[direc], 4, 1, player)
                    counter_n = counter(
                        i, j, env, directions[direc], 4, -1, player)

                    # calculate the score of both directions
                    if counter_p * counter_n > 0:
                        score += (counter_p + counter_n)**5
                    else:
                        score += (counter_p)**5 + (counter_n)**5

    # return score of the env by weight.
    # If weight > 0: the agent is passive!
    # If weight < 0: the agent is aggressive!
    # If weight = 0: the agent is neutral!
    if weight > 0:
        return score*weight if score > 0 else score
    elif weight < 0:
        return score*-weight if score < 0 else score
    else:
        return score


# Function to count len of symbols array that we have in some direction
def counter(i, j, env, direc, depth, np, player):
    counter = 0
    for k in range(1, depth):
        i_k = i + np * direc[0] * k
        j_k = j + np * direc[1] * k
        if 0 <= i_k < env.boardH and \
                0 <= j_k < env.boardW and \
                env.board[i_k][j_k] != 0:
            symbol = env.board[i_k][j_k]
            count = 1 if env.player2symbol[player] == symbol else -1
            if k == 1 or \
                    (counter * count > 0):  # Check if the counter and count both positive or negative
                counter += count
            else:
                break
        else:
            break
    return counter


# Initial parameters
WEIGHT = 1.5
depths = [1, 3, 5, 7]
timers = [1e-9, 1, 3, 10]
astratege = [WEIGHT, 1, 0, -WEIGHT]

def wraper(env, player):
    return inrow_heuristic(env, player, 1)

# Create list of players
players = [RandomAgent("random")]
for depth in depths:
    for time in timers:
            players.append(MinimaxAgent(
                f"minimax_depth{depth}_time{time}_weight{WEIGHT}", depth, wraper, time))


def tournament(players):
    result_table = []
    for pair in product(players, repeat=2):
        result = match(pair[0], pair[1])
        result_table.append({"players": pair, "result": result})
    return result_table


def match(player1, player2):
    board = create_env('4-in-row', player1, player2, (6, 7))
    try:
        while not board.is_terminal_state():
            board.apply_action(player1, player1.choose_action(board))
            board.apply_action(player2, player2.choose_action(board))
        return board.player_status(player1), board.player_status(player2)
    except TimeoutError:
        return "TimeoutError"

    return board.player_status(player1), board.player_status(player2)

result_table = tournament(players)
print("Result of the tournament:")
print("--------------------------------------------")
for match in result_table:
    print("palyer 1: {}".format(match["players"][0]))
    print("player 2: {}".format(match["players"][1]))
    if match["result"] == "TimeoutError":
        print("TimeoutError")
    elif match["result"][0] > 0:
        print("player 1 won!")
        print("player 2 loss...")
    elif match["result"][1] > 0:
        print("player 1 loss...")
        print("player 2 won!")
    else:
        print("draw")
    print("--------------------------------------------")
