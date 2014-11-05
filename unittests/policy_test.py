import unittest
from collections import Counter

from models.policies.policy import Policy


class testPolicy(unittest.TestCase):
    def setUp(self):
        self.pol = Policy()

    def test_get_direction(self):
        directions = []
        for i in xrange(100):
            directions.append(self.pol.get_direction())
        c = Counter(directions)
        print c.keys()
        print c.values()
        self.assertEqual(len(c.values()), 5)

    def testPredatorPolicy(self):
        field = Field(3, 3)
        predator = Predator((1, 1))
        policy = PredatorPolicy()

        field.add_player(predator)
        field.print_field()

    def testPreyPolicy1(self):
        field = Field(3, 3)
        predator = Predator((1, 1))
        policy = PredatorPolicy()

        field.add_player(predator)
        field.print_field()


if __name__ == '__main__':
    unittest.main()
