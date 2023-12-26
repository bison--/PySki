import random
from objects.StaticObstacle import StaticObstacle


class StaticRandomObstacle(StaticObstacle):
    def __init__(self, x, y):
        random_sprite_index = random.choices(
            list(range(len(StaticObstacle.SPRITES))),
            weights=(50, 25, 50, 10, 5, 2),
            k=1
        )[0]

        super().__init__(x, y, random_sprite_index)
