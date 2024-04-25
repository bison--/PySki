import sys
import pygame

# original: https://github.com/pythonfoo/pySnake/blob/master/ui.py


class Ui:
    INTERACTION_UP = 1
    INTERACTION_RIGHT = 2
    INTERACTION_DOWN = 3
    INTERACTION_LEFT = 4
    INTERACTION_SELECT = 5

    font_cache = {}

    def __init__(self, _screen):

        # the main screen, result from:
        # pygame.display.set_mode(...)
        self._screen = _screen
        self.keymap = {
            pygame.K_UP: Ui.INTERACTION_UP,
            pygame.K_RIGHT: Ui.INTERACTION_RIGHT,
            pygame.K_DOWN: Ui.INTERACTION_DOWN,
            pygame.K_LEFT: Ui.INTERACTION_LEFT,
        }  # pygame.K_RETURN:5}
        self.selected_color = (245, 101, 44)  # orange ;)
        self.next_action = None
        self.antialias = True

        self.menus = {}

        self._selected_menu = ''  # menu 'name'
        self._selected_menu_item = None  # selected item row
        self._selected_menu_item_index = -1  # selected index

    def interaction(self, event_key):
        can_interact = False

        if event_key in self.keymap:
            can_interact = True
            self.next_action = self.keymap[event_key]
            if self.next_action == 1:  # UP
                self.select_menu_item(-1)
            elif self.next_action == 3:  # DOWN
                self.select_menu_item(1)
            elif self.next_action == 5:  # SELECTED
                pass
        else:
            # reset the action if multiple times pressed keys before
            # actually did something
            self.next_action = None

        return can_interact

    def get_interaction(self, event_key):
        if event_key in self.keymap:
            return self.keymap[event_key]
        else:
            return None

    def add_menu(self, menu_key, menu_rows):
        """ add a menu
        @menu_key: unique name of the menu
        @menu_rows: [
            {"rowName": "title", "selectable": False, "font": "MS Comic Sans", "fontSize":30, "color": (0,0,255), "text": "UserInterfaceGenerator"},
            {"rowName": "start", "selectable": True, "font": "MS Comic Sans", "fontSize":30, "color": (0,0,255), "text": "Start Game"},
            {"rowName": "q", "selectable": True, "font": "MS Comic Sans", "fontSize":30, "color": (123,55,255), "text": "QUIT"}
        ]
        """
        self.menus[menu_key] = menu_rows

    def add_simple_menu(self, menu_key, menu_rows, font="MS Comic Sans", size=30, color=(245, 101, 44)):
        """ add an SIMPLE menu
            @menu_key: unique name of the menu
            @menu_rows: ["You Shall", "NOT PASS"]
        """
        menu = []
        row_count = 0
        for row in menu_rows:
            menu.append({
                "rowName": "simple_" + str(row_count),
                "selectable": False,
                "font": font,
                "fontSize": size,
                "color": color,
                "text": row
            })
            row_count += 1

        self.menus[menu_key] = menu

    def __get_available_indexes(self):
        index_list = []
        if self._selected_menu in self.menus:
            for i in range(len(self.menus[self._selected_menu])):
                if self.menus[self._selected_menu][i]['selectable']:
                    index_list.append(i)

        return index_list

    def select_menu_item(self, direction=0):
        """ select the menu item
            @direction: +1 (down) or -1 (up), 0 for the first selectable item in the current menu
        """

        index_list = self.__get_available_indexes()
        if len(index_list) == 0:
            # NO SELECTABLE MENU ITEMS
            return -1

        if self._selected_menu in self.menus and direction == 0:
            self._selected_menu_item_index = index_list[0]
            self._selected_menu_item = self.menus[self._selected_menu][index_list[0]]
        else:
            current_index = 0
            if self._selected_menu_item_index in index_list:
                current_index = index_list.index(self._selected_menu_item_index)
            next_index = current_index + direction

            # allow top-down / down-top switching
            if next_index >= len(index_list):  # last element of list!
                self._selected_menu_item_index = index_list[0]
                self._selected_menu_item = self.menus[self._selected_menu][self._selected_menu_item_index]
            elif next_index < 0:
                self._selected_menu_item_index = index_list[-1]  # last element of list!
                self._selected_menu_item = self.menus[self._selected_menu][self._selected_menu_item_index]
            else:
                self._selected_menu_item_index = index_list[next_index]
                self._selected_menu_item = self.menus[self._selected_menu][self._selected_menu_item_index]

        return self._selected_menu_item

    def get_selected_item(self):
        if self._selected_menu in self.menus and self._selected_menu_item_index >= 0:
            return self.menus[self._selected_menu][self._selected_menu_item_index]

        # NO SELECTED MENU ITEM FOUND!
        return None

    @staticmethod
    def try_load_font(_font_name, _font_size):
        cache_name = _font_name + str(_font_size)

        if cache_name in Ui.font_cache:
            return Ui.font_cache[cache_name]

        try:
            Ui.font_cache[cache_name] = pygame.font.Font(_font_name, _font_size)
        except Exception as ex:
            print("WARNING! Font '" + _font_name + "' not found, using default font.", ex)
            Ui.font_cache[cache_name] = pygame.font.SysFont(_font_name, _font_size)

        return Ui.font_cache[cache_name]

    def __get_menu_row_real_font_sizes(self, menu_row):
        fnt = self.try_load_font(menu_row["font"], menu_row["fontSize"])
        return fnt.size(menu_row["text"])

    def __get_previous_menu_rows_real_font_height(self, menu_rows, current_index):
        accumulated = 0
        for i in range(len(menu_rows)):
            if current_index == i:
                break

            accumulated += self.__get_menu_row_real_font_sizes(menu_rows[i - 1])[1]

        return accumulated

    def __get_previous_menu_row_real_font_height(self, menu_rows, current_index):
        if current_index == 0:
            return 0

        for i in range(len(menu_rows)):
            if i == current_index:
                return self.__get_menu_row_real_font_sizes(menu_rows[i - 1])[1]

        return 0

    def hide_menu(self):
        self._selected_menu = ''
        self._selected_menu_item = None
        self._selected_menu_item_index = -1

    def draw(self, menu_key=''):
        if menu_key in self.menus:
            self._selected_menu = menu_key
        elif menu_key == '':
            if self._selected_menu == '' and 'main' in self.menus:
                self._selected_menu = 'main'
        else:
            raise Ui.MenuKeyError(menu_key, "and there is no 'main' menu")

        menu_to_draw = self.menus[self._selected_menu]

        if self._selected_menu_item_index == -1:
            self.select_menu_item(0)

        height_center = self._screen.get_height() / 2 - self.__get_previous_menu_rows_real_font_height(menu_to_draw, len(menu_to_draw)) / 2
        y_pos = height_center

        if menu_to_draw is not None:
            menu_rows_count = len(menu_to_draw)
            for i in range(menu_rows_count):
                previous_row_font_height = self.__get_previous_menu_row_real_font_height(menu_to_draw, i)
                x_pos = (self._screen.get_width() / 2)
                y_pos += previous_row_font_height

                font_size = menu_to_draw[i]["fontSize"]
                font = self.try_load_font(menu_to_draw[i]["font"], font_size)
                txt = menu_to_draw[i]["text"]

                font_width, _ = font.size(txt)

                color = menu_to_draw[i]["color"]
                if i == self._selected_menu_item_index:
                    color = self.selected_color

                self._screen.blit(font.render(txt, self.antialias, color), (x_pos - (font_width / 2), y_pos))
        else:
            raise Ui.MenuKeyError(menu_key)

    class MenuKeyError(Exception):
        def __init__(self, menu_key, additional_message=""):
            self.menu_key = menu_key
            # Call the base class constructor with the parameters it needs
            super().__init__("Error menu '{}' does not exist {}".format(menu_key, additional_message))


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1024, 768), 0, 32)
    clock = pygame.time.Clock()

    BG_COLOR = (8, 13, 41)

    iUi = Ui(screen)
    font_name = "MS Comic Sans"

    iUi.add_menu("main", [
        {"rowName": "title", "selectable": False, "font": font_name, "fontSize": 30, "color": (0, 0, 255),
         "text": "UserInterfaceGenerator"},
        {"rowName": "start", "selectable": True, "font": font_name, "fontSize": 30, "color": (0, 0, 255),
         "text": "Start Game"},
        {"rowName": "info", "selectable": True, "font": font_name, "fontSize": 30, "color": (123, 55, 255),
         "text": "1NF0$"},
        {"rowName": "q", "selectable": True, "font": font_name, "fontSize": 30, "color": (123, 55, 255),
         "text": "QUIT"},
        {"rowName": "notes", "selectable": False, "font": font_name, "fontSize": 30, "color": (123, 55, 255),
         "text": "sometext"},
    ])

    while True:
        # Limit frame speed to 60 FPS
        time_passed = clock.tick(60)
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if iUi.interaction(event.key):
                    print("UI caught this key:", event.key)
                else:
                    print("no UI catch, key pressed:", event.key)
                    if pygame.K_RETURN == event.key:
                        print("selected item:", iUi.get_selected_item())

                    if event.key == pygame.K_q:
                        sys.exit(0)

        iUi.draw("main")

        pygame.display.flip()
