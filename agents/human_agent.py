from .agent_base import Agent
import sys


class HumanAgent(Agent):
    """
    A user interface for playing the game -
    Renders the environment for the user to see and decide which action to take by letting
    the user choose the action.
    """

    def __init__(self, name):
        super(HumanAgent, self).__init__(name)

    def choose_action(self, env):
        # create list of available moves
        available_moves = list(env.available_moves(self))

        # check if the list are not empty
        if available_moves:

            # action of the player
            while True:
                print("Please choose your action from the list below and press ENTER:")
                print(" # | col")
                print("---------")
                for act in enumerate(available_moves):
                    print(" {0} |  {1}".format(act[0]+1, act[1]))
                move = input()

                # check input
                if move == 'q':
                    sys.exit(0)
                try:
                    assert int(move) > 0
                    return available_moves[int(move)-1]
                except (ValueError, IndexError, AssertionError) as error:
                    if isinstance(error, ValueError):
                        print("The input must be an integer, try again or quit (q)")
                    elif isinstance(error, IndexError):
                        print("The input must be from a moves list, try again or quit (q)")
                    elif isinstance(error, AssertionError):
                        print("The input must be a positive number, try again or quit (q)")
                    

        print("No moves available for player {}".format(self))
        return None
