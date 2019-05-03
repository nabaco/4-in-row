class EnvironmentBase:
    """
    Base class for all environments.
    Args:
        player1, player2: the player objects.
    """

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def reset(self):
        """
        Resets to the initial state of the environment and returns its observation.
        Returns:
            An observation of the initial state.
        """
        raise NotImplementedError

    def apply_action(self, player, action):
        """
        Apply action as a player.
        Args:
            player: the player
            action: the action
        Returns: tuple of (State, Reward)
            State - an observation of the next state.
            Reward for the action taken if the action is legal. # for now - return only 0.
            If the action is illegal - returns None.
        """
        raise NotImplementedError

    def render(self):
        """
        Prints the current state of the environment.
        """
        raise NotImplementedError

    def available_moves(self, player):
        """
        Returns an iterable of available moves for the player.
        """
        raise NotImplementedError

    def is_terminal_state(self):
        """
        Returns a true if the environment has reached its final state.
        """
        raise NotImplementedError

    def player_status(self, player):
        """
        Returns an number representing the status of the player for this environment:
        Negative number if the player has lost,
        Positive number if the player has won,
        otherwise returns 0.
        """
        raise NotImplementedError
