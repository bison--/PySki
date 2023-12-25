import pygame
import random
from Ui import Ui
from objects.Tree import Tree
from objects.Rock import Rock
from objects.Player import Player
import config


class Game:
    MENU_GAME_OVER = "game_over"

    def __init__(self):
        self.speed = 1
        self.game_over = False
        self.all_objects = []
        self.__current_frame_keys_down = {}

        # Initialize pygame
        pygame.init()

        # Set the FPS
        self.clock = pygame.time.Clock()

        # Create a window of the size of the image
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('PySki')

        # Translate the image data to a pygame surface
        self.original_surface = pygame.Surface((config.WIDTH, config.HEIGHT))

        # make it bigger from the start
        self.screen = pygame.display.set_mode((config.LAUNCH_WIDTH, config.LAUNCH_HEIGHT), pygame.RESIZABLE)

        self.player_object = Player(config.WIDTH / 2 - 8, 20)
        self.all_objects.append(self.player_object)

        self.iUi = Ui(self.original_surface)
        self.iUi.addMenu(Game.MENU_GAME_OVER, [
            {
                "rowName": "title",
                "selectable": False,
                "font": "MS Comic Sans",
                "fontSize": 30,
                "color": (0, 0, 255),
                "text": "Game Over"
            },
            {
                "rowName": "restart",
                "selectable": True,
                "font": "MS Comic Sans",
                "fontSize": 30,
                "color": (0, 0, 255),
                "text": "Restart"},
        ])

    def process_player_input(self):
        if self.game_over:
            return

        if self.__current_frame_keys_down[pygame.K_LEFT]:
            self.player_object.move_left(1)
        elif self.__current_frame_keys_down[pygame.K_RIGHT]:
            self.player_object.move_right(1)

    def spawn_objects(self):
        lowest_object_position = 0
        for obj in self.all_objects:
            if obj.y > lowest_object_position:
                lowest_object_position = obj.y

        if lowest_object_position >= config.HEIGHT - 16:
            return

        self.all_objects.append(
            random.choice([Rock, Tree])(random.randint(0, config.WIDTH - 16), config.HEIGHT)
        )

    def run(self):
        self.all_objects += [
            Tree(0, 0),
            Tree(10, 10),
            Rock(20, 20),
            Tree(100, 100),
        ]

        # Main loop
        keep_running = True
        while keep_running:
            self.clock.tick(60)
            self.spawn_objects()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                elif event.type == pygame.KEYDOWN:
                    if self.iUi.interaction(event.key):
                        # print("UI catched this key:", event.key)
                        pass
                    else:
                        # print("no UI catch, key pressed:", event.key)
                        if pygame.K_RETURN == event.key:
                            selected_menu_item = self.iUi.getSelectedItem()
                            if selected_menu_item is not None and selected_menu_item['rowName'] == "restart":
                                self.game_over = False
                                self.speed = 1
                                self.all_objects = [self.player_object]

                            # print("selected item:", self.iUi.getSelectedItem())

            self.__current_frame_keys_down = pygame.key.get_pressed()

            if self.__current_frame_keys_down[pygame.K_DOWN]:
                self.speed += 1
            elif self.__current_frame_keys_down[pygame.K_UP]:
                self.speed -= 1
                if self.speed < 1:
                    self.speed = 1

            move_vertical_speed = self.clock.get_time()

            self.process_player_input()
            self.original_surface.fill((255, 255, 255))

            for i in range(len(self.all_objects) - 1, -1, -1):
                obj = self.all_objects[i]
                if not self.game_over:
                    obj.move_up(self.speed / move_vertical_speed)

                if obj.can_be_removed():
                    self.all_objects.pop(i)
                    continue

                obj.draw(self.original_surface)

            for obj in self.all_objects:
                if obj is self.player_object:
                    continue

                if obj.check_collision(self.player_object.get_rect()):
                    self.game_over = True

            if self.game_over:
                self.iUi.draw(Game.MENU_GAME_OVER)

            # Scale the surface to fit the window size
            scaled_surface = pygame.transform.scale(self.original_surface, self.screen.get_size())
            self.screen.blit(scaled_surface, (0, 0))

            pygame.display.flip()

        pygame.quit()
