import os
from objects.BaseObject import BaseObject


class Player(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join('images', 'skier.png'))
        # TODO: load more frames

    def move_up(self, y):
        pass

    def move_left(self, x):
        self.move(-x, 0)

    def move_right(self, x):
        self.move(x, 0)
