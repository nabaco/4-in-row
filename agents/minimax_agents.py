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
    TODO - Implement!
    """
    def choose_action(self, env):
        pass


class AlphaBetaPruningAget(SearchAgentBase):
    """
    This agent implements the alpha-beta pruning algorithm, described in the book AIMA (3rd edition): Chapter 5.3.
    TODO - Implement!
    """
    def choose_action(self, env):
        pass
