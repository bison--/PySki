import os
import random
from objects.BaseObject import BaseObject


class StaticRandomObstacle(BaseObject):
    def __init__(self, x, y):
        sprites = [
            os.path.join('images', 'pine_tree.png'),
            os.path.join('images', 'pine_tree_snow.png'),
            os.path.join('images', 'pine_trees.png'),
            os.path.join('images', 'rocks.png'),
            os.path.join('images', 'wooden_hut_1.png'),
        ]

        random_sprites = random.choices(
            sprites,
            weights=(50, 25, 50, 10, 5),
            k=1
        )

        random_sprite = random_sprites[0]

        super().__init__(x, y, random_sprite)

