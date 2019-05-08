class Agent:
    def __init__(self, name: str):
        self.name = name

    def choose_action(self, env):
        """
        Chooses and returns an action to take on the environment.
        Args:
            env (Environment): the environment on which to take an action
                based upon the observations.
        Returns:
            action: the action that was chosen by the agent.
        """
        raise NotImplementedError

    def __repr__(self):
        """
        Returns a pretty string representation of this object.
        DO NOT OVERRIDE THIS!
        """
        return "{0}({1}){2}".format(self.name, self.__class__.__name__,
                                    '\n' + self.extra_repr())

    # Methods for making player accessible as a key for a dictionary:
    def __hash__(self):
        return hash(object.__repr__(self))

    def __eq__(self, other):
        return type(other) == type(self) and id(self) == id(other)

    def extra_repr(self):
        """
        Returns extra string representation of the current object.
        Any derived class may override this.
        """
        return ''
