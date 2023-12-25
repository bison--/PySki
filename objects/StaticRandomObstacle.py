import pygame
import random
from objects.BaseObject import BaseObject


class StaticRandomObstacle(BaseObject):
    def __init__(self, x, y):
        sprites = [
            r'images\pine_trees.png',  # tree
            r'images\rocks.png',  # rock
        ]

        random_sprites = random.choices(
            sprites,
            weights=(50, 10),
            k=1
        )

        random_sprite = random_sprites[0]

        super().__init__(x, y, random_sprite)

