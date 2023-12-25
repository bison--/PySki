from typing import Optional

import pygame


class BaseObject:
    global_image_cache = {}

    def __init__(self, x, y, image_filename):
        self.x = x
        self.y = y
        self.image_filename = image_filename

        self.image: pygame.Surface = self.load_image()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def load_image(self):
        if self.image_filename not in BaseObject.global_image_cache:
            BaseObject.global_image_cache[self.image_filename] = pygame.image.load(self.image_filename)

        return BaseObject.global_image_cache[self.image_filename]

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def check_collision(self, other: pygame.Rect):
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(
            pygame.Rect(other.x, other.y, other.width, other.height)
        )

    def move(self, x, y):
        self.x += x
        self.y += y

    def move_up(self, y):
        self.y -= y

    def can_be_removed(self):
        if self.y < -self.height:
            return True

        return False
