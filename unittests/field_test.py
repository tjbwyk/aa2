import unittest

from field import Field
from prey import Prey
from predator import Predator


class testField(unittest.TestCase):
    def setUp(self):
        self.environment = Field(11, 11)

    def test_get_new_coordinates(self):
        location = (5, 4)
        delta = (8, 8)
        (new_x, new_y) = self.environment.get_new_coordinates(location, delta)

        self.assertEqual(new_x, 2)
        self.assertEqual(new_y, 1)

    def test_add_player(self):
        prey = Prey((5, 5))
        predator = Predator((1, 1))
        self.environment.add_player(prey)
        self.environment.add_player(predator)

        self.assertEqual(prey.field, self.environment)
        self.assertEqual(len(self.environment.players), 2)

    def test_get_players_of_class(self):
        prey = Prey((5, 5))
        predator = Predator((1, 1))
        predator2 = Predator((2, 2))
        self.environment.add_player(prey)
        self.environment.add_player(predator)
        self.environment.add_player(predator2)
        self.assertEqual(self.environment.get_players_of_class(Predator), [predator, predator2])
        self.assertEqual(self.environment.get_players_of_class(Prey), [prey])

    def test_print_field(self):
        prey = Prey((5, 5))
        predator = Predator((1, 1))
        predator2 = Predator((2, 2))
        self.environment.add_player(prey)
        self.environment.add_player(predator)
        self.environment.add_player(predator2)
        print self.environment.print_field()
        print self.environment


if __name__ == '__main__':
    unittest.main()