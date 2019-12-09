from gym.spaces import Discrete
from numpy import inf


class Inning(object):
    """
    Environment for refreeing the game between two agents.

    Args:
        wickets: Number of batsman per inning.
        target: If first inning set to (default) infinity, else set to target.

    """
    action_space = Discrete(7)
    observation_space = Discrete(7)

    def __init__(self, wickets=1, target=inf):
        self.wickets = wickets
        self.target = target
        self.reset()

    def reset(self):
        """
        Resets the innings by making runs to zero and outs to zero.
        """
        self.runs = 0
        self.outs = 0

    def end_of_inning(self):
        """
        Will return `True` if outs equals wickets or if target is met, otherwise will return
        `False`.

        Returns:
            bool: End of episode.
        """
        return self.outs == self.wickets or self.runs > self.target

    def __repr__(self):
        return '<{} instance>'.format(type(self).__name__)

    def step(self, bat, bowl):
        """ Step consumes one batsman agent's action and a bowler agent's action.
        It then either adds the batsman's runs to the env score or calls the batsman out.
        The actions spaces used are `gym.spaces.Discrete(7)`.

        Args:
            bat: In action space. Action of a batsman.
            bowl: In action space. Action of a bowler.

        Returns:
            tuple: Each item has the following. The first is the batsman's output.
                observation (object): Bowler's action.
                reward (float) : Reward is `1` if not out. `0` if out.
                done (bool): Whether the innings has ended or not.
                info (dict): `runs` will return current runs.

                For bowler:
                observation (object): Batsman's action.
                reward (float) : Reward is `1` if out. `0` if not out.
                done (bool): Whether the innings has ended or not.
                info (dict): `runs` will return current runs.

        Raises:
            ValueError: If the actions are out of bounds.
        """
        if not self.action_space.contains(bat):
            raise ValueError("Batsman action is invalid.")
        if not self.action_space.contains(bowl):
            raise ValueError("Bowler action is invalid.")

        bat_obs = bowl
        bowl_obs = bat

        if bat == bowl:
            self.outs += 1
            bat_reward = 0
            bowl_reward = 1
        else:
            bat_reward = 1
            bowl_reward = 0
            self.runs += bat
            if bat == 0:
                self.runs += bowl

        info_dict = {'runs': self.runs}
        bat_out = (bat_obs, bat_reward, self.end_of_inning(), info_dict)
        bowl_out = (bowl_obs, bowl_reward, self.end_of_inning(), info_dict)

        return bat_out, bowl_out
