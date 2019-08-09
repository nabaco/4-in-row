from envs import *
from agents import *
from time import time
from sys import exit
from game_of_agents import aggressive_heuristic, passive_heuristic, neutral_heuristic, zero_heuristic


heuristics = {'a': aggressive_heuristic,
              'p': passive_heuristic,
              'n': neutral_heuristic,
              'z': zero_heuristic,
              }


def user_input(message, input_type, options):
    """
    Function that take care about user input.
    Arguments:
        message (str): message to the user.
        input_type (str):
            'c' - choose item from the options tuple.
            'i' - choose int betwin two numbers in the options tuple.
            'f' - choose float betwin two numbers in the options tuple.
        options (tuple):
            tuple of the options to choose from if the input_type is 'c'
            and the range of numbers betwin witch the user can choose num
            if the input_type is 'i' or 'f'.
    Return:
        The user choose by the limits mention in the input_style and options/
    """

    while True:
        user_choose = input(message + " or quit (q): ")

        # Check if the user want to quit ('q')
        if user_choose == 'q':
            exit(0)

        # Check the validity of the input if so return the input
        if input_type == 'c' and\
                user_choose in options:
            return user_choose

        if input_type == 'i' or\
                input_type == 'f':
            try:
                if input_type == 'i':
                    assert options[0] <= int(user_choose) <= options[1]
                    return int(user_choose)
                if input_type == 'f':
                    assert options[0] <= float(user_choose) <= options[1]
                    return float(user_choose)

            except (ValueError, AssertionError):
                pass
        print("Ooops... Invalid input. Please try again or quit (q)")


def create_opponent():
    opp_type_message = "Please choose your opponent from the list below:\n"\
        "\t(r) Random agent\n"\
        "\t(m) Minimax agent\n"\
        "\t(a) Alpha Beta Pruning Agent\n"\
        "\t"

    # Choose opponent type
    opp_type = user_input(opp_type_message, 'c', ('r', 'm', 'a'))

    # Random
    if opp_type == 'r':
        return RandomAgent("Random")

    # Minimax
    if opp_type == 'm':
        # Choose depth
        opp_depth_message = "Please enter the max search depth of the agent"
        opp_depth = user_input(opp_depth_message, 'i', (1, float("inf")))

        # Choose timer
        opp_timer_message = "Please enter the max search time of the agent"
        opp_timer = user_input(opp_timer_message, 'f', (0, float("inf")))

        # Choose weight
        opp_strategy_message = "Please choose the agent strategy from the list below:\n"\
            "\t(a) Aggressive\n"\
            "\t(p) Passive\n"\
            "\t(n) Neutral\n"\
            "\t(z) Zero\n"\
            "\t"
        opp_strategy = user_input(
            opp_strategy_message, 'c', ('a', 'p', 'n', 'z'))

        # Return the minimax agent
        return MinimaxAgent("Minimax", opp_depth, heuristics[opp_strategy], opp_timer)

    if opp_type == 'a':
        print("Sorry, but Alpha Beta Pruning agent not implemented yet...")
        exit(0)


def create_players(user):
    opponent = create_opponent()
    first_player_message = "Please choose who will play the first move\n"\
        "\t(y) You\n"\
        "\t(c) Computer\n"\
        "\t"
    first_player = user_input(first_player_message, 'c', ('y', 'c'))
    return (user, opponent) if first_player == 'y' else (opponent, user)


def inrow_game(user):
    # Create players and the env
    player1, player2 = create_players(user)
    board = create_env("4-in-row", player1, player2, (6, 7))

    # Start the game
    start_time = time()
    try:
        while not board.is_terminal_state():
            print(
                f"{player1.name} turn.\tThe time from the start of the game is {time()-start_time} (sec)")
            board.render()
            board.apply_action(player1, player1.choose_action(board))
            if board.is_terminal_state():
                break
            print(
                f"{player2.name} turn.\tThe time from the start of the game is {time()-start_time} (sec)")
            board.render()
            board.apply_action(player2, player2.choose_action(board))

    # Except to the computer timeout
    except PlayerTimeout as to:
        result_render(board, start_time, 'to', user, to.player)
        return None

    # Print the result
    if board.player_status(player1) > 0:
        result_render(board, start_time, 'go', player1, player2)
    elif board.player_status(player1) < 0:
        result_render(board, start_time, 'go', player2, player1)
    else:
        result_render(board, start_time, 'd')


def result_render(board, start_time, result, winner=None, losser=None):
    print("Game over (tm)")
    board.render()
    if result == 'go':
        print(f"{winner.name} won!, {losser.name} loss...")
    elif result == 'to':
        print(f"The time of {losser.name} is out.")
        print(f"{winner.name} won!, {losser.name} loss...")
    elif result == 'd':
        print("draw")
    print(f"The total time of the game is {time() - start_time} (sec)")


if __name__ == "__main__":
    print("Welcome to the AI 4-in-row game!!!")
    user_name = input("Please enter your name or quit (q): ")
    if user_name == 'q':
        exit(0)
    user = HumanAgent(user_name)
    while True:
        inrow_game(user)
        user_input("Please start new game (n)", 'c', ('n'))
