from envs import *
from agents import *


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
    # If weight = 0: the agent is static!
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
