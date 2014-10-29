__author__ = 'fbuettner'

class Field:
    """
    the playground
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_new_coordinates(self, current_x, current_y, delta_x, delta_y):
        new_x = current_x + delta_x
        if new_x <= 0:
            new_x += self.width
        elif new_x > self.width:
            new_x -= self.width

        new_y = current_y + delta_y
        if new_y <= 0:
            new_y += self.height
        elif new_y > self.height:
            new_y -= self.height

        return new_x, new_y

    def __str__(self):
        # print ASCII field here
        return "bla"