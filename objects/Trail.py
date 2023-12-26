import os
from objects.BaseObject import BaseObject


class Trail(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join('images', 'trail.png'))
