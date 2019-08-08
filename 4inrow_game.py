﻿from envs import *
from agents import *
from time import time
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
        message: message to the user.
        input_type:
            'c' - choose item from the options tuple.
            'i' - choose int betwin two numbers in the options tuple.
            'f' - choose float betwin two numbers in the options tuple.
        options:
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
            return None

        # Check the validity of the input
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


def opponent():
    opp_type_message = "Please choose your opponent from the list below:\n"\
        "\t(r) Random agent\n"\
        "\t(m) Minimax agent\n"\
        "\t(a) Alpha Beta Pruning Agent\n"\
        "\t"

    # Choose opponent type
    opp_type = user_input(opp_type_message, 'c', ('r', 'm', 'a'))
    if not opp_type:
        return None

    # Random
    if opp_type == 'r':
        return RandomAgent("random")

    # Minimax
    if opp_type == 'm':
        # Choose depth
        opp_depth_message = "Please enter the max search depth of the agent"
        opp_depth = user_input(opp_depth_message, 'i', (1, float("inf")))
        if not opp_depth:
            return None

        # Choose timer
        opp_timer_message = "Please enter the max search time of the agent"
        opp_timer = user_input(opp_timer_message, 'f', (0, float("inf")))
        if not opp_timer:
            return None

        # Choose weight
        opp_strategy_message = "Please choose the agent strategy from the list below:\n"\
            "\t(a) Aggressive\n"\
            "\t(p) Passive\n"\
            "\t(n) Neutral\n"\
            "\t(z) Zero\n"\
            "\t"
        opp_strategy = user_input(
            opp_strategy_message, 'c', ('a', 'p', 'n', 'z'))
        if not opp_strategy:
            return None

        # Return the minimax agent
        return MinimaxAgent("minimax", opp_depth, heuristics[opp_strategy], opp_timer)

    if opp_type == 'a':
        print("Sorry, but Alpha Beta Pruning agent not implemented yet...")
        return None


