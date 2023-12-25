import pygame
from objects.BaseObject import BaseObject


class Player(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y, r'images\26_16.png')
        # TODO: load more frames

    def move_up(self, y):
        pass

    def move_left(self, x):
        self.x -= x

    def move_right(self, x):
        self.x += x
