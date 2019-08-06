from .agent_base import Agent
# Note - from this point on, we refer to the book 'Artificial Intelligence: a Modern Approach' as AIMA.

DEFAULT_SEARCH_DEPTH = 3  # Maximum depth of the search
TIMEOUT = 10.  # Maximum time for the agent to search through the state space


def default_score_fn(env, player):
    """
    This is the default scoring function passed to the constructor of the agent.
    the scoring function should have this exact signature (except the name), as it
    gets the env and the player and outputs a score of the current state for the player.
    The scoring function is used as a heuristic for the agent to search for the best move.
    Args:
        env (Environment): the environment.
        player (Agent): the player.
    Returns:
        score (float): a score for the current state and player.
    Note:
        the score may be infinite! using infinite scores to represent winning/losing states may be beneficial!
    """
    return 0.


class SearchAgentBase(Agent):
    """
    Base class for searching agents, like minimax and alpha-beta pruning agents.
    """
    def __init__(self, name, search_depth=DEFAULT_SEARCH_DEPTH, score_fn=default_score_fn, timeout=TIMEOUT):
        super(SearchAgentBase, self).__init__(name)
        self.search_depth = search_depth
        self.score_fn = score_fn
        self.timeout = timeout

    def choose_action(self, env):
        raise NotImplementedError


class MinimaxAgent(SearchAgentBase):
    """
    This agent implements the minimax algorithm, described in the book AIMA (3rd edition): Chapter 5.2.
    """

    def minimax(self, node, search_depth, max_agent = False):
        
        # check terminal state or max search depth
        if node.is_terminal_state or search_depth == 0:
            return self.score_fn(node, self)

        # return MAX value of children nodes
        if max_agent:
            val = -float("inf")
            for move in node.available_moves:
                new_node = node.copy()
                new_node.applay_action(self, move)
                val = max(val, self.minimax(new_node, search_depth - 1, max_agent = False))

        # return MIN value of children nodes
        else:
            val = float("inf")
            node.switch_player()
            for move in node.available_moves:
                new_node = node.copy()
                new_node.applay_action(self, move)
                val = min(val, self.minimax(new_node, search_depth - 1, max_agent = True))

        return val


    def choose_action(self, env):

        # create list of available moves
        available_moves = list(env.available_moves(self))

        # check if we have available moves
        if available_moves:

            # search for a best move with the best value in the next node
            best_move = {"move":None, "val":-float("inf")}
            for move in available_moves:
                new_node = env.copy()
                new_node.applay_action(move)
                val = self.minimax(new_node, self.search_depth, max_agent=False)
                if val > best_move["val"]:
                    best_move["move"] = move
                    best_move["val"] = val

            # return the best move
            return best_move["move"]

        # if we don't have available moves return None
        return None
        


class AlphaBetaPruningAgent(SearchAgentBase):
    """
    This agent implements the alpha-beta pruning algorithm, described in the book AIMA (3rd edition): Chapter 5.3.
    TODO - Implement!
    """
    def choose_action(self, env):
        pass
