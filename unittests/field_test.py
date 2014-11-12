import unittest

from models.field import Field
from models.prey import Prey
from models.predator import Predator


class testField(unittest.TestCase):
    def setUp(self):
        self.environment = Field(11, 11)

    def setup_standard_env(self):
        prey = Prey((5, 5))
        predator = Predator((1, 1))
        self.environment.add_player(prey)
        self.environment.add_player(predator)
        return prey,predator

    def test_get_new_coordinates(self):
        location = (5, 4)
        delta = (8, 8)
        (new_x, new_y) = self.environment.get_new_coordinates(location, delta)

        self.assertEqual(new_x, 2)
        self.assertEqual(new_y, 1)

    def test_add_player(self):
        prey,predator =  self.setup_standard_env()
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

    def test_reward(self):
        self.assertEqual(self.environment.get_reward(((1,1),(2,2))), 0)
        self.assertEqual(self.environment.get_reward(((1,1),(1,1))), 10)

    def test_get_all_states(self):
        self.assertEqual(len(self.environment.get_all_states()), (self.environment.height * self.environment.width)^2
                         -(self.environment.height * self.environment.width))

    def test_get_state(self):
        prey,predator =  self.setup_standard_env()
        self.assertEqual(self.environment.get_state(),(60,12))

    def test_get_players_except(self):
        prey,predator =  self.setup_standard_env()
        self.assertEqual(self.environment.get_players_except(predator),[prey])

    def test_relative_position(self):
	self.assertEqual(self.environment.get_relative_position((0,0), (10,10)), (-1,-1))
	self.assertEqual(self.environment.get_relative_position((9,9), (1,2)), (3,4))
	self.assertEqual(self.environment.get_relative_position((5,5), (4,6)), (-1,1))

	

if __name__ == '__main__':
    unittest.main()
