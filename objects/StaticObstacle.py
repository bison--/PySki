import os
from objects.BaseObject import BaseObject


class StaticObstacle(BaseObject):
    SPRITES = [
        os.path.join('images', 'pine_tree.png'),
        os.path.join('images', 'pine_tree_snow.png'),
        os.path.join('images', 'pine_trees.png'),
        os.path.join('images', 'rocks.png'),
        os.path.join('images', 'wooden_hut_1.png'),
        os.path.join('images', 'christmas_tree.png'),
    ]

    def __init__(self, x, y, selected_sprite: any):
        if type(selected_sprite) is int:
            super().__init__(x, y, StaticObstacle.SPRITES[selected_sprite])
        elif type(selected_sprite) is str:
            super().__init__(x, y, os.path.join('images', selected_sprite))
        else:
            raise Exception('Invalid sprite type')

        self.kills_player = True
