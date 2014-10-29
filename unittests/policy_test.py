from policy import Policy
import unittest
from collections import Counter

class testPolicy(unittest.TestCase):
    def setUp(self):
        self.pol = Policy(0.2, 0.2, 0.2, 0.2, 0.2)


    def test_get_direction(self):
        directions = []
        for i in xrange(100):
            directions.append(self.pol.get_direction())
        c = Counter(directions)
        print c.values()
        self.assertEqual(len(c.values()), 5)

if __name__ == '__main__':
    unittest.main()
