import os
import random
import pygame

from Ui import Ui
from objects.BaseObject import BaseObject
from objects.StaticRandomObstacle import StaticRandomObstacle
from objects.Player import Player
import config_loader as config


class Game:
    MENU_GAME_OVER = "game_over"

    def __init__(self):
        self.keep_running = True
        self.game_over = False
        self.speed = 1
        self.distance_traveled = 0

        self.all_objects: list[BaseObject] = []
        self.__current_frame_keys_down = {}

        # Initialize pygame
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()

        # Set the FPS
        self.clock = pygame.time.Clock()

        # Set the window title
        pygame.display.set_caption('PySki')

        # Translate the image data to a pygame surface
        self.original_surface = pygame.Surface((config.WIDTH, config.HEIGHT))

        # Make the drawn screen bigger from the start
        self.screen = pygame.display.set_mode((config.LAUNCH_WIDTH, config.LAUNCH_HEIGHT), pygame.RESIZABLE)

        self.player_object = Player(0, 0)

        self.iUi = Ui(self.original_surface)
        self.create_menu()

    def start_game(self):
        self.speed = 1
        self.set_player_centered()

        self.all_objects = [
            self.player_object,
            StaticRandomObstacle(0, 0),
            StaticRandomObstacle(10, 10),
            StaticRandomObstacle(20, 20),
            StaticRandomObstacle(100, 100),
        ]

    def set_player_centered(self):
        self.player_object.set_position(
            config.WIDTH / 2 - 8, 20
        )

    def create_menu(self):
        self.iUi.antialias = config.ANTI_ALIAS

        self.iUi.addMenu(Game.MENU_GAME_OVER, [
            {
                'rowName': 'title',
                'selectable': False,
                'font': config.FONT_NAME,
                'fontSize': 30,
                'color': (235, 64, 52),
                'text': 'Game Over'
            },
            {
                'rowName': 'restart',
                'selectable': True,
                'font': config.FONT_NAME,
                'fontSize': 20,
                'color': (0, 0, 255),
                'text': 'Restart',
                'action': self.menu_action_restart
            },
            {
                'rowName': 'exit',
                'selectable': True,
                'font': config.FONT_NAME,
                'fontSize': 20,
                'color': (0, 0, 255),
                'text': 'EXIT',
                'action': self.menu_action_exit
            },
        ])

    def process_menu_action(self, menu_item):
        pass

    def menu_action_restart(self):
        self.game_over = False
        self.start_game()

    def menu_action_exit(self):
        self.game_over = True
        self.keep_running = False

    def process_player_input(self):
        if self.game_over:
            return

        if self.__current_frame_keys_down[pygame.K_LEFT]:
            self.player_object.move_left(1)
        elif self.__current_frame_keys_down[pygame.K_RIGHT]:
            self.player_object.move_right(1)

        if self.__current_frame_keys_down[pygame.K_DOWN]:
            self.speed += 1
        elif self.__current_frame_keys_down[pygame.K_UP]:
            self.speed -= 1
            if self.speed < 1:
                self.speed = 1

    def spawn_objects(self):
        lowest_object_position = 0
        for obj in self.all_objects:
            if obj.y > lowest_object_position:
                lowest_object_position = obj.y

        if lowest_object_position >= config.HEIGHT - 16:
            return

        x = random.randint(0, config.WIDTH - 16)
        self.all_objects.append(StaticRandomObstacle(x, config.HEIGHT))

    def draw_distance(self):
        font = pygame.font.Font(config.FONT_NAME, 16)
        text = font.render("Distance: " + str(self.distance_traveled), config.ANTI_ALIAS, (100, 100, 100))
        self.original_surface.blit(text, (0, 0))

    def run(self):
        self.start_game()

        to_move_cache = 0

        # Main loop
        while self.keep_running:
            self.clock.tick(config.MAX_FPS)
            self.spawn_objects()

            to_move = 0
            if not self.game_over:
                to_move_delta = to_move_cache + (self.speed / self.clock.get_time())
                to_move_cache = to_move_delta % 1
                to_move = int(to_move_delta)
                self.distance_traveled += to_move

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_action_exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_over = True

                    if self.iUi.interaction(event.key):
                        # print("UI catched this key:", event.key)
                        pass
                    else:
                        # print("no UI catch, key pressed:", event.key)
                        if pygame.K_RETURN == event.key or pygame.K_SPACE == event.key or pygame.K_KP_ENTER == event.key:
                            selected_menu_item = self.iUi.getSelectedItem()
                            if selected_menu_item is not None and 'action' in selected_menu_item:
                                selected_menu_item['action']()
                                self.iUi.hideMenu()

            self.__current_frame_keys_down = pygame.key.get_pressed()
            self.process_player_input()

            self.original_surface.fill((255, 255, 255))

            for i in range(len(self.all_objects) - 1, -1, -1):
                obj = self.all_objects[i]
                if not self.game_over:
                    obj.move_up(to_move)

                if obj.can_be_removed():
                    self.all_objects.pop(i)
                    continue

                obj.draw(self.original_surface)

            for obj in self.all_objects:
                if obj.check_pixel_collision(self.player_object):
                    self.game_over = True
                    break

            if self.game_over:
                self.iUi.draw(Game.MENU_GAME_OVER)

            self.draw_distance()

            # Scale the surface to fit the window size
            scaled_surface = pygame.transform.scale(self.original_surface, self.screen.get_size())
            self.screen.blit(scaled_surface, (0, 0))

            pygame.display.flip()

        pygame.quit()
