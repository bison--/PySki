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

    def __init__(self, screen):

        # the main screen, result from:
        # pygame.display.set_mode(...)
        self._screen = screen
        self.keymap = {
            pygame.K_UP: Ui.INTERACTION_UP,
            pygame.K_RIGHT: Ui.INTERACTION_RIGHT,
            pygame.K_DOWN: Ui.INTERACTION_DOWN,
            pygame.K_LEFT: Ui.INTERACTION_LEFT,
        }  # pygame.K_RETURN:5}
        self.selectedColor = (245, 101, 44)  # orange ;)
        self.nextAction = None
        self.antialias = True

        self.menus = {}

        self._selectedMenu = ''  # menu 'name'
        self._selectedMenuItem = None  # selected item row
        self._selectedMenuItemIndex = -1  # selected index

    def interaction(self, eventKey):
        canInteract = False

        if eventKey in self.keymap:
            canInteract = True
            self.nextAction = self.keymap[eventKey]
            if self.nextAction == 1:  # UP
                self.selectMenuItem(-1)
            elif self.nextAction == 3:  # DOWN
                self.selectMenuItem(1)
            elif self.nextAction == 5:  # SELECTED
                pass
        else:
            # reset the action if multiple times pressed keys before
            # actually did something
            self.nextAction = None

        return canInteract

    def getInteraction(self, eventKey):
        if eventKey in self.keymap:
            return self.keymap[eventKey]
        else:
            return None

    def addMenu(self, menuKey, menuRows):
        """ add a menu
        @menuKey: unique name of the menu
        @menuRows: [
                    {"rowName":"title", "selectable":False, "font":"MS Comic Sans", "fontSize":30, "color":(0,0,255), "text":"UserInterfaceGenerator"},
                    {"rowName":"start", "selectable":True, "font":"MS Comic Sans", "fontSize":30, "color":(0,0,255), "text":"Start Game"},
                    {"rowName":"q", "selectable":True, "font":"MS Comic Sans", "fontSize":30, "color":(123,55,255), "text":"QUIT"}
                    ]
        """
        self.menus[menuKey] = menuRows

    def addSimpleMenu(self, menuKey, menuRows, font="MS Comic Sans", size=30, color=(245, 101, 44)):
        """ add an SIMPLE menu
            @menuKey: unique name of the menu
            @menueRows: ["You Shall", "NOT PASS"]
        """
        menu = []
        rowCount = 0
        for row in menuRows:
            menu.append({"rowName": "simple_" + str(rowCount),
                         "selectable": False,
                         "font": font,
                         "fontSize": size,
                         "color": color,
                         "text": row}
                        )

        self.menus[menuKey] = menu

    def __getAvailableIndexes(self):
        indexList = []
        if self._selectedMenu in self.menus:
            for i in range(len(self.menus[self._selectedMenu])):
                if self.menus[self._selectedMenu][i]['selectable']:
                    indexList.append(i)
        return indexList

    def selectMenuItem(self, direction=0):
        """ select the menu item
            @direction: +1 (down) or -1 (up), 0 for the first selectable item in the current menu
        """
        # self._selectedIndex

        indexList = self.__getAvailableIndexes()
        if len(indexList) == 0:
            # print('NO SELECTABLE MENU ITEMS')
            return -1

        if self._selectedMenu in self.menus and direction == 0:
            self._selectedMenuItemIndex = indexList[0]
            self._selectedMenuItem = self.menus[self._selectedMenu][indexList[0]]
        else:
            currentIndex = 0
            if self._selectedMenuItemIndex in indexList:
                currentIndex = indexList.index(self._selectedMenuItemIndex)
            nextIndex = currentIndex + direction

            # allow top-down / down-top switching
            if nextIndex >= len(indexList):  # last element of list!
                self._selectedMenuItemIndex = indexList[0]
                self._selectedMenuItem = self.menus[self._selectedMenu][self._selectedMenuItemIndex]
            elif nextIndex < 0:
                self._selectedMenuItemIndex = indexList[-1]  # last element of list!
                self._selectedMenuItem = self.menus[self._selectedMenu][self._selectedMenuItemIndex]
            else:
                self._selectedMenuItemIndex = indexList[nextIndex]
                self._selectedMenuItem = self.menus[self._selectedMenu][self._selectedMenuItemIndex]

        return self._selectedMenuItem

    def getSelectedItem(self):
        if self._selectedMenu in self.menus and self._selectedMenuItemIndex >= 0:
            return self.menus[self._selectedMenu][self._selectedMenuItemIndex]

        # print("WARNING! NO SELECTED MENU ITEM FOUND!")
        return None

    def tryLoadFont(self, font_name, font_size):
        cacheName = font_name + str(font_size)

        if cacheName in Ui.font_cache:
            return Ui.font_cache[cacheName]

        try:
            Ui.font_cache[cacheName] = pygame.font.Font(font_name, font_size)
        except Exception as ex:
            print("WARNING! Font '" + font_name + "' not found, using default font.", ex)
            Ui.font_cache[cacheName] = pygame.font.SysFont(font_name, font_size)

        return Ui.font_cache[cacheName]

    def __getMenuRowRealFontSizes(self, menuRow):
        fnt = self.tryLoadFont(menuRow["font"], menuRow["fontSize"])
        return fnt.size(menuRow["text"])

    def __getPreviousMenuRowsRealFontHeight(self, menuRows, currentIndex):
        accumulated = 0
        for i in range(len(menuRows)):
            if currentIndex == i:
                break

            accumulated += self.__getMenuRowRealFontSizes(menuRows[i - 1])[1]

        return accumulated

    def __getPreviousMenuRowRealFontHeight(self, menuRows, currentIndex):
        if currentIndex == 0:
            return 0

        for i in range(len(menuRows)):
            if i == currentIndex:
                return self.__getMenuRowRealFontSizes(menuRows[i - 1])[1]

        return 0

    def hideMenu(self):
        self._selectedMenu = ''
        self._selectedMenuItem = None
        self._selectedMenuItemIndex = -1

    def draw(self, menuKey=''):
        if menuKey in self.menus:
            self._selectedMenu = menuKey
        elif menuKey == '':
            if self._selectedMenu == '' and 'main' in self.menus:
                self._selectedMenu = 'main'
        else:
            raise Exception("Error menu '" + menuKey + "' does not exist and there is no 'main' menu")

        menuToDraw = self.menus[self._selectedMenu]

        if self._selectedMenuItemIndex == -1:
            self.selectMenuItem(0)

        heightCenter = self._screen.get_height() / 2 - self.__getPreviousMenuRowsRealFontHeight(menuToDraw, len(menuToDraw)) / 2
        yPos = heightCenter

        if menuToDraw is not None:
            # print fnt.size(resultText)
            menuRowsCount = len(menuToDraw)
            for i in range(menuRowsCount):
                previous_row_font_height = self.__getPreviousMenuRowRealFontHeight(menuToDraw, i)
                xPos = (self._screen.get_width() / 2)
                yPos += previous_row_font_height

                fontSize = menuToDraw[i]["fontSize"]
                fnt = self.tryLoadFont(menuToDraw[i]["font"], fontSize)
                txt = menuToDraw[i]["text"]

                font_width, font_height = fnt.size(txt)

                color = menuToDraw[i]["color"]
                if i == self._selectedMenuItemIndex:
                    color = self.selectedColor

                self._screen.blit(fnt.render(txt, self.antialias, color), (xPos - (font_width / 2), yPos))
        else:
            raise Exception("Error menu '" + menuKey + "' does not exist")


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1024, 768), 0, 32)
    clock = pygame.time.Clock()

    BG_COLOR = (8, 13, 41)

    iUi = Ui(screen)
    iUi.addMenu("main", [
        {"rowName": "title", "selectable": False, "font": "MS Comic Sans", "fontSize": 30, "color": (0, 0, 255),
         "text": "UserInterfaceGenerator"},
        {"rowName": "start", "selectable": True, "font": "MS Comic Sans", "fontSize": 30, "color": (0, 0, 255),
         "text": "Start Game"},
        {"rowName": "info", "selectable": True, "font": "MS Comic Sans", "fontSize": 30, "color": (123, 55, 255),
         "text": "1NF0$"},
        {"rowName": "q", "selectable": True, "font": "MS Comic Sans", "fontSize": 30, "color": (123, 55, 255),
         "text": "QUIT"},
        {"rowName": "notes", "selectable": False, "font": "MS Comic Sans", "fontSize": 30, "color": (123, 55, 255),
         "text": "sometext"},
    ])

    while True:
        # Limit frame speed to 50 FPS
        time_passed = clock.tick(50)
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if iUi.interaction(event.key):
                    print("UI catched this key:", event.key)
                else:
                    print("no UI catch, key pressed:", event.key)
                    if pygame.K_RETURN == event.key:
                        print("selected item:", iUi.getSelectedItem())

                    if event.key == pygame.K_q:
                        sys.exit(0)

        iUi.draw("main")

        pygame.display.flip()
