__author__ = 'fbuettner'
import unittest

from field import Field
from predator import Predator
from predatorpolicy import PredatorPolicy


class testField(unittest.TestCase):
    def setUp(self):
        self.environment = Field(11, 11)
        self.fatcat = Predator((0, 0))
        self.fatcat.policy = PredatorPolicy(self.fatcat, self.environment)

    def test_probability(self):
        probabilities = self.fatcat.policy.get_probability(state=((0, 0), (0, 1)), next_state=((0, 0), (0, 1)),
                                                           action=(0, 1))
        print probabilities