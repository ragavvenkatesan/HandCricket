from numpy import random, asarray, inf

from sooli import Inning
from sooli import Player
from sooli import PlayerModes


class Playground(object):
    """
    Playground will initialize two environments one for first inning and one for second inning.
    Playground will initialize two players in batting and bowling mode.
    Playground will play the game ball-by-ball.
    After two innings, playground will declare winner.

    Args:
        p1: Player class object for player 1.
        p2: Player class object for player 2.
        wickets: Number of wickets per innings. Defaults to `1`.

    Raises:
        TypeError: If `p1` and `p2` are not of type `sooli.Player`.
    """

    def __init__(self, p1, p2, wickets=1):
        self.wickets = wickets
        self.p1 = p1
        self.p2 = p2

        if not isinstance(self.p1, Player):
            raise TypeError('Player 1 is not of type Player.')
        if not isinstance(self.p2, Player):
            raise TypeError('Player 2 is not of type Player.')

        self.toss = random.randint(1, 3, 1)

    def _first_inning_roles(self):
        """
        Reset assigns start of match, player roles.
        """
        if self.toss == 1:
            self.p2.reset(mode=PlayerModes.bowling)
            self.p1.reset(mode=PlayerModes.batting)
        else:
            self.p1.reset(mode=PlayerModes.bowling)
            self.p2.reset(mode=PlayerModes.batting)

    def _second_inning_roles(self):
        """ consumes toss but assigns role opposite to reset."""
        if self.toss == 1:
            self.p1.reset(mode=PlayerModes.bowling)
            self.p2.reset(mode=PlayerModes.batting)
        else:
            self.p2.reset(mode=PlayerModes.bowling)
            self.p1.reset(mode=PlayerModes.batting)

    @staticmethod
    def _play_inning(batsman, bowler, wickets, target=inf):
        """
        Will run an innings.
        Args:
            batsman: Of type `sooli.Player` in mode `sooli.PlayerModes.batting`.
            bowler: Of type `sooli.Player` in mode `sooli.PlayerModes.bowling`.
            wickets: Number of wickets per innings.
            target: If first inning set to (default) infinity, else set to target.
        """
        inning = Inning(wickets=wickets, target=target)
        bat_tuple = (asarray(0.), asarray(0.), False, {'runs': 0})
        bowl_tuple = (asarray(0.), asarray(0.), False, {'runs': 0})
        done = False
        curr_runs = 0
        while not done:
            bat_actions = batsman(bat_tuple[0], bat_tuple[1], bat_tuple[2], bat_tuple[3])
            bowl_actions = bowler(bowl_tuple[0], bowl_tuple[1], bowl_tuple[2], bowl_tuple[3])
            bat_tuple, bowl_tuple = inning.step(bat_actions, bowl_actions)
            done = bowl_tuple[2]
            curr_runs = inning.runs
        return curr_runs

    def __call__(self):
        self._first_inning_roles()
        if self.toss == 1:
            batsman = self.p1
            bowler = self.p2
        else:
            batsman = self.p2
            bowler = self.p1
        target = Playground._play_inning(batsman, bowler, self.wickets)
        self._second_inning_roles()
        chase = Playground._play_inning(bowler, batsman, self.wickets, target=target)
        if target == chase:
            return 0, target, chase  # Tied game
        elif target > chase:
            return 1, target, chase  # Player 1 wins
        else:
            return 2, target, chase  # Player 2 wins
