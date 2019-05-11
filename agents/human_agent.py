from .agent_base import Agent
import sys


class HumanAgent(Agent):
    """
    A user interface for playing the game -
    Renders the environment for the user to see and decide which action to take by letting
    the user choose the action.
    TODO - implement everything!
    """

    def __init__(self, name):
        super(HumanAgent, self).__init__(name)

    def choose_action(self, env):
        # create list of available moves
        available_moves = env.available_moves(self)

        # check if the list are not empty
        if available_moves:

            # action of the player
            while True:
                print("Please choose your action from the list below and press ENTER:")
                for act in available_moves:
                    print(act)
                move = input()

                # check input
                if move == 'q':
                    sys.exit(0)
                try:
                    assert int(move) in available_moves
                    return int(move)
                except:
                    print("Wrong input, try again or quit (q)")

        print("No moves available for player {}".format(self))
