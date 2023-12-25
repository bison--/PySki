import pygame
from objects.Tree import Tree
from objects.Rock import Rock
from objects.Player import Player
import config


class Game:
    def __init__(self):
        pass

    def run(self):
        # Initialize pygame
        pygame.init()

        # Set the FPS
        clock = pygame.time.Clock()

        # Create a window of the size of the image
        screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('PySki')

        # Translate the image data to a pygame surface
        original_surface = pygame.Surface((config.WIDTH, config.HEIGHT))

        # _tree = pygame.image.load(r'images\kenney_1-bit-pack-tiles\102_16.png')

        # make it bigger from the start
        screen = pygame.display.set_mode((config.LAUNCH_WIDTH, config.LAUNCH_HEIGHT), pygame.RESIZABLE)

        player_object = Player(config.WIDTH / 2 - 8, 20)

        all_objects = [
            player_object,
            Tree(0, 0),
            Tree(10, 10),
            Rock(20, 20),
            Tree(100, 100),
        ]

        speed = 1
        is_game_over = False

        # Main loop
        running = True
        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_DOWN]:
                speed += 1
            elif keys[pygame.K_UP]:
                speed -= 1
                if speed < 1:
                    speed = 1

            if keys[pygame.K_LEFT]:
                player_object.move_left(1)
            elif keys[pygame.K_RIGHT]:
                player_object.move_right(1)

            original_surface.fill((255, 255, 255))

            move_vertical_speed = clock.get_time()

            for i in range(len(all_objects) - 1, -1, -1):
                obj = all_objects[i]
                obj.move_up(speed / move_vertical_speed)

                if obj.can_be_removed():
                    all_objects.pop(i)
                    continue

                obj.draw(original_surface)

            # Scale the surface to fit the window size
            scaled_surface = pygame.transform.scale(original_surface, screen.get_size())
            screen.blit(scaled_surface, (0, 0))

            pygame.display.flip()

        pygame.quit()
