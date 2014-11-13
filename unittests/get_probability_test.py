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
        probabilities, next_states = self.fatcat.policy.get_next_states((0,0))
        print probabilities