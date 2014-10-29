import unittest
from field import Field

class testField(unittest.TestCase):
    def setUp(self):
        self.environment = Field(11, 11)

    def test_get_new_coordinates(self):
        x = 5
        y = 4
        delta_x = 8
        delta_y = 8
        new_x, new_y = self.environment.get_new_coordinates(x, y, delta_x, delta_y)
        self.assertEqual(new_x, 2)
        self.assertEqual(new_y, 1)

if __name__ == '__main__':
    unittest.main()