import logging
import pygame
import config_loader as conf


class BaseObject:
    global_image_cache = {}
    global_image_mask_cache = {}

    def __init__(self, x, y, image_filename):
        self.kills_player = False

        self.x = x
        self.y = y
        self.image_filename = image_filename

        self.image: pygame.Surface = self.load_image()
        self.collision_mask: pygame.mask.Mask = self.load_image_mask()

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def set_image(self, _image_filename):
        self.image_filename = _image_filename
        self.image: pygame.Surface = self.load_image()
        self.collision_mask: pygame.mask.Mask = self.load_image_mask()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def load_image(self):
        if self.image_filename not in BaseObject.global_image_cache:
            BaseObject.global_image_cache[self.image_filename] = pygame.image.load(self.image_filename)

        return BaseObject.global_image_cache[self.image_filename]

    def load_image_mask(self):
        if self.image_filename not in BaseObject.global_image_mask_cache:
            BaseObject.global_image_mask_cache[self.image_filename] = pygame.mask.from_surface(
                BaseObject.global_image_cache[self.image_filename]
            )

        return BaseObject.global_image_mask_cache[self.image_filename]

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def check_pixel_collision(self, other):
        if other == self:
            return False

        other_rect = other.get_rect()

        # simple rectangle collision check
        if not self.check_collision_rect(other_rect):
            return False

        # Calculate the offset
        offset = (int(self.x - other.x), int(self.y - other.y))

        # debug
        self_rect = self.get_rect()
        logging.debug(f"Self Position: ({self_rect})")
        logging.debug(f"Other Position: ({other_rect})")
        logging.debug(f"Offset: {offset}")

        # NOTE: overlap() returns NONE if there is no intersection
        #       overlap_mask() returns an object in any case with the intersecting pixels
        #       thanks ChatGPT for finding my mistake

        # Check for mask overlap with the calculated offset
        return other.collision_mask.overlap(
            self.collision_mask, offset
        )

    def check_collision(self, other):
        if other == self:
            return False

        return self.check_collision_rect(other.get_rect())

    def check_collision_rect(self, other: pygame.Rect):
        return self.get_rect().colliderect(other)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x += x
        self.y += y

    def move_up(self, y):
        self.y -= y

    def can_be_removed(self):
        if self.y < -self.height:
            return True

        return False
