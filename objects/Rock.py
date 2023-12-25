import pygame
from objects.BaseObject import BaseObject


class Rock(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y, r'images\606_16.png')

