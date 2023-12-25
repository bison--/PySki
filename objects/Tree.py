import pygame
from objects.BaseObject import BaseObject


class Tree(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y, r'images\102_16.png')
