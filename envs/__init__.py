from .env_base import Environment
from .env_4inrow import Env4InRow

__all__ = ['Environment', 'create_env']

ENVS = {
    'base': Environment,
    '4-in-row': Env4InRow
}


def create_env(env_type, p1, p2, *args, **kwargs):
    """
    Creates an environment.
    Args:
        env_type (str): the type of the environment. currently supported: '4-in-row'
        p1, p2 (Agent): the agents.
        *args, **kwargs : additional parameters for creation of the environment.
    Returns:
        env (Environment) : the environment object.
    """
    return ENVS[env_type](p1, p2, *args, **kwargs)
