import unittest
from field import Field
from prey import Prey
from predator import Predator


class testField(unittest.TestCase):
    def setUp(self):
        self.environment = Field(11, 11)

    def test_get_new_coordinates(self):
        location = (5,4)
        delta = (8,8)
        (new_x, new_y) = self.environment.get_new_coordinates(location,delta)

        self.assertEqual(new_x, 2)
        self.assertEqual(new_y, 1)

    def test_add_player(self):
        prey = Prey((5,5))
        predator = Predator((1,1))
        self.environment.add_player(prey)
        self.environment.add_player(predator)

        self.assertEqual(prey.field, self.environment)
        self.assertEqual(len(self.environment.players), 2)


if __name__ == '__main__':
    unittest.main()