from envs import *
from agents import *
from itertools import product
from time import time


# Heuristic function for "4 in row" game
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

    if weight == 0:
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


# Helper function to count len of symbols array that we have in some direction
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


# Wrapper functions to define different heuristic strategics
def aggressive_heuristic(env, player):  # Aggressive strategy
    return inrow_heuristic(env, player, WEIGHT)


def passive_heuristic(env, player):  # Passive strategy
    return inrow_heuristic(env, player, -WEIGHT)


def neutral_heuristic(env, player):  # Neutral strategy
    return inrow_heuristic(env, player, 1)


def zero_heuristic(env, player):  # Zero strategy
    return inrow_heuristic(env, player, 0)


heuristics = {"aggressive": aggressive_heuristic,
              "passive": passive_heuristic,
              "neutral": neutral_heuristic,
              "zero": zero_heuristic}


# Function to play a game for each pair of players with different timers
def tournament(players, timers):

    # Remember the pair of agents that got timeout
    timeout_detector = None, None

    # Run over all combination of players and timers
    for player1, player2, timeout in product(players, players, timers):

        # Check if the player1 == player2 and if this pair of agents got timeout in previous match
        if player1 == player2 or timeout_detector == (player1, player2):
            continue

        # Play the game and return the result
        result = game(player1, player2, timeout)
        if result["total-time"] == "Player1 Timeout" or\
                result["total-time"] == "Player2 Timeout":
            timeout_detector = player1, player2

        yield {"players": (player1, player2),
               "timeout": timeout,
               "result": result["result"],
               "game-time": result["total-time"],
               "actions": result["actions"],
               }


# Play a single game
def game(player1, player2, timeout):
    # Define timeout and create board
    player1.timeout = timeout
    player2.timeout = timeout
    board = create_env('4-in-row', player1, player2, (6, 7))

    # Try to play the game
    actions = 0
    try:
        start_time = time()
        while not board.is_terminal_state():
            if board.apply_action(player1, player1.choose_action(board)):
                actions += 1
            if board.apply_action(player2, player2.choose_action(board)):
                actions += 1
        total_time = time() - start_time
        return {"result": (board.player_status(player1), board.player_status(player2)),
                "total-time": total_time,
                "actions": actions}

    # Except timeout
    except PlayerTimeout as ex:
        if ex.player == player1:
            return {"result": (-1, 1), "total-time": "Player1 Timeout", "actions": actions}
        return {"result": (1, -1), "total-time": "Player2 Timeout", "actions": actions}


# Print the result of the match
def render(num, match):
    print(f"Match number: # {num + 1}")
    print("Palyer 1: {}".format(match["players"][0].name))
    print("Player 2: {}".format(match["players"][1].name))
    print("Timeout: {} (sec)".format(match["timeout"]))
    print("Total time of the match: {} (sec)".format(match["game-time"]))
    print("Total actions of the players: {}".format(match["actions"]))
    if match["result"][0] > 0:
        print("Player 1 won!")
        print("Player 2 loss...")
    elif match["result"][1] > 0:
        print("Player 1 loss...")
        print("Player 2 won!")
    else:
        print("draw")
    print("--------------------------------------------")


# Initial parameters
WEIGHT = 1.5
depths = [1, 3, 5, 7]
timers = [3, 2, 1, 0.1]


# Create list of all players with different initial parameters
players = [RandomAgent("random")]
for depth, (heuristic_name, heuristic_func) in product(depths, heuristics.items()):
    players.append(MinimaxAgent(
        f"minimax agent, depth = {depth}, heuristic = {heuristic_name}", depth, heuristic_func, 0))
print("List of players was created Successfly")


print("Result of the tournament:")
print("--------------------------------------------")
for num, match in enumerate(tournament(players, timers)):
    render(num, match)
print("Done")
