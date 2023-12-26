import os
from objects.BaseObject import BaseObject


class Tree(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join('images', 'pine_trees.png'))
        self.kills_player = True
