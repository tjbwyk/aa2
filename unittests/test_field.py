from unittest import TestCase
from collections import Counter
from models.player import Player
from models.field import Field

__author__ = 'fbuettner'


class TestField(TestCase):
    def test_transition(self):
        """
        test if the transitions are computed correctly based on tripping probabilities.
        """
        n_runs = 1000
        p = Player(location=(0, 0), tripping_prob=0.5)
        f = Field(11, 11)
        f.add_player(p)
        new_states = [f.transition(p, action=(-1, 0)) for i in range(n_runs)]
        c = Counter(new_states)
        self.assertAlmostEqual(c[c.keys()[0]], n_runs*p.tripping_prob, delta=0.05*n_runs)