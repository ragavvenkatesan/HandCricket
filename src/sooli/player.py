from gym.spaces import Discrete


class PlayerModes:
    batting = 'batting'
    bowling = 'bowling'


class Player(object):
    """ Abstract player that plays samples from a unifrom random distribution."""

    def __init__(self):
        self.action_space = Discrete(7)
        self.mode = PlayerModes.batting

    def reset(self, mode=PlayerModes.batting):
        """
        Use reset to set the player's mode.
        Args:
            mode: Some mode to which to reset.
        """
        self.mode = mode

    def __call__(self, obs, reward, done, info):
        """ Player will consume everything that the previous step provided."""
        return self.action_space.sample()

    def __repr__(self):
        return '{} instance'.format(type(self).__name__)
