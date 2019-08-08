from .agent_base import Agent
# Note - from this point on, we refer to the book 'Artificial Intelligence: a Modern Approach' as AIMA.

import time
DEFAULT_SEARCH_DEPTH = 3  # Maximum depth of the search
TIMEOUT = 10.  # Maximum time for the agent to search through the state space


class PlayerTimeout(Exception):
    def __init__(self, player, message=""):
        super(PlayerTimeout, self).__init__(message)
        self.player = player


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
    if env.is_terminal_state():
        if env.player_status(player) > 0:
            return float("inf")
        if env.player_status(player) < 0:
            return -float("inf")
        return 0
    return 0


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

    def max_value(self, node, depth):
        # Check timeout
        if time.time() - self.start_time > self.timeout:
            raise PlayerTimeout(self)

        # Check terminal state or max search depth
        if node.is_terminal_state() or depth == 0:
            return self.score_fn(node, self)

        # Return MAX value of children nodes
        val = -float("inf")
        for move in node.available_moves(node.current_player):
            child = node.copy()
            child.apply_action(node.current_player, move)
            val = max(val, self.min_value(child, depth - 1))
        return val

    def min_value(self, node, depth):
        # Check timeout
        if time.time() - self.start_time > self.timeout:
            raise PlayerTimeout(self)

        # Check terminal state or max search depth
        if node.is_terminal_state() or depth == 0:
            return self.score_fn(node, self)

        # Return MIN value of children nodes
        val = float("inf")
        for move in node.available_moves(node.current_player):
            child = node.copy()
            child.apply_action(node.current_player, move)
            val = min(val, self.max_value(child, depth - 1))
        return val

    def minimax(self, env, move, depth):
        child = env.copy()
        child.apply_action(self, move)
        val = self.min_value(child, depth - 1)
        return val

    def choose_action(self, env):
        self.start_time = time.time()
        available_moves = list(env.available_moves(self))
        if available_moves:
            best_move = max(available_moves, key=lambda x: self.minimax(
                env, x, self.search_depth))
            return best_move
        return None


class AlphaBetaPruningAgent(SearchAgentBase):
    """
    This agent implements the alpha-beta pruning algorithm, described in the book AIMA (3rd edition): Chapter 5.3.
    TODO - Implement!
    """

    def choose_action(self, env):
        pass
