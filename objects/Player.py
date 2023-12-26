import os
from objects.BaseObject import BaseObject


class Player(BaseObject):
    def __init__(self, x, y):
        self.image_left = os.path.join('images', 'skier_left.png')
        self.image_right = os.path.join('images', 'skier_right.png')
        self.image_down = os.path.join('images', 'skier.png')
        self.direction_move_counter = 0

        super().__init__(x, y, self.image_down)

    def move_up(self, y):
        self.direction_move_counter -= 1
        if self.direction_move_counter > 0:
            return

        self.set_image(self.image_down)

    def move_left(self, x):
        self.move(-x, 0)
        self.set_image(self.image_left)
        self.direction_move_counter = 2

    def move_right(self, x):
        self.move(x, 0)
        self.set_image(self.image_right)
        self.direction_move_counter = 2
