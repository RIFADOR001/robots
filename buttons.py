import pygame
import os
# from main import main_function
from game_menu import adjustTime, bid


BUTTON_LENGTH = 50
TEXT_FONT1 = pygame.font.SysFont('comicsans', 12)


# Class of buttons. Buttons are used to select pieces to move, set timer, go back some steps, restart the game
class Button(object):
    # We specify the location, size and function of the button (character, timer, go back, etc.)
    # The constructor needs to know the position, size, function of button and color (assuming it is linked to a piece)
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(os.path.join('Assets', 'Blank.png'))


class PenguinButton(Button):
    def __init__(self, x, y, penguin):
        Button.__init__(self, x, y, 50, 50)
        self.pushed = False
        self.color = penguin.color
        self.penguin = penguin
        self.penguin.button = self
        # Depending on the color of the piece, the image is selected
        self.image_nonactive = pygame.image.load(os.path.join("Assets", f"hero{self.color}.png"))
        self.image = self.image_nonactive
        self.image_active = pygame.image.load(os.path.join("Assets", f"{self.color}_active.png"))

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def activate(self, penguin_button_list):
        for pb in penguin_button_list:
            pb.pushed = False
            pb.image = pb.image_nonactive
        self.image = self.image_active
        self.pushed = True


class PlayerButton(Button):
    def __init__(self, x, y, player):
        Button.__init__(self, x, y, BUTTON_LENGTH, 20)
        self.name = player.name
        self.player = player

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        name_info = TEXT_FONT1.render(self.player.name, True, (0, 0, 0))
        if self.player.bid_status:
            score_info = TEXT_FONT1.render(f"Score: {self.player.score}  Bid: {self.player.bid}", True, (0, 0, 0))
        else:
            score_info = TEXT_FONT1.render(f"Score: {self.player.score}", True, (0, 0, 0))
        win.blit(name_info, (self.x, self.y))
        win.blit(score_info, (self.x + BUTTON_LENGTH + 5, self.y))

    def activate(self, game_info):
        game_info.active_player = self.player
        game_info.timer = True
        game_info.player_not_selected = False
        self.player.bid = bid(self.player.bid_status, self.player.name, self.player.bid)
        self.player.bid_status = True


class MovementButton(Button):
    def __init__(self, x, y, function):
        if function == "Restart position":
            Button.__init__(self, x, y, 100, 20)
            self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Blank.png')), (100, 20))
        else:
            Button.__init__(self, x, y, 50, 20)
            # self.image = pygame.image.load(os.path.join('Assets', 'Blank.png'))
        self.function = function

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        button_info = TEXT_FONT1.render(self.function, True, (0, 0, 0))
        win.blit(button_info, (self.x, self.y))

    def activate(self, game_info):
        if self.function == "Back":
            if game_info.index > 0:
                game_info.steps -= 2
                game_info.index -= 1
                aux = 0
                for p in game_info.pieces_list:
                    p.x = game_info.position_list[game_info.INDEX][aux][0]
                    p.y = game_info.position_list[game_info.INDEX][aux][1]
                    aux += 1
            print("Back")
        if self.function == "Forward":
            print("Forward")
            n = len(game_info.position_list)
            if game_info.index < n - 1:
                game_info.index += 1
                aux = 0
                for p in game_info.pieces_list:
                    p.x = game_info.position_list[game_info.index][aux][0]
                    p.y = game_info.position_list[game_info.index][aux][1]
                    aux += 1

        if self.function == "Print list":
            print(game_info.position_list)
        if self.function == "Restart position":
            game_info.INDEX = 0
            aux = 0
            print(self.function)
            for p in game_info.lists.penguins_list:
                p.x = game_info.position_list[0][aux][0]
                p.y = game_info.position_list[0][aux][1]
                aux += 1


class FunctionalityButton(Button):
    def __init__(self, x, y, function):
        Button.__init__(self, x, y, 50, 20)
        self.function = function
        self.pushed = False

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

        button_info = TEXT_FONT1.render(self.function, True, (0, 0, 0))
        win.blit(button_info, (self.x, self.y))

        # The activate function will depend on the pressed button
    def activate(self, game_info=None):
        if self.function == "Restart":
            game_info.tokens = 0
            # main_function(game_info)
        if self.function == "Time":
            game_info.timer = True
            self.pushed = True
        if self.function == "Start yes":
            self.pushed = True
        if self.function == "Start no":
            self.pushed = True
        if self.function == "Rules":
            path = os.path.join('Assets', 'rules.pdf')
            os.system("open " + path)
            # os.system("open Assets/rules.pdf")
        if self.function == "Settings":
            game_info.hourglass = adjustTime()


class ButtonLists(object):
    def __init__(self, penguin_button_list, player_button_list, functionality_button_list):
        self.penguin_button_list = penguin_button_list
        self.player_button_list = player_button_list
        self.functionality_button_list = functionality_button_list

    def draw(self, win):
        for pen_b in self.penguin_button_list:
            pen_b.draw(win)
        for pla_b in self.player_button_list:
            pla_b.draw(win)
        for fun_b in self.functionality_button_list:
            fun_b.draw(win)

    # We verify if a button was pushed. If it is a piece, the other pieces should deactivate and the pushed
    # piece should become active. This is the piece that we will move.
    def handle_clicks(self, x, y, game_info):
        for pen_button in self.penguin_button_list:
            if not game_info.movement:
                if pen_button.x < x < pen_button.x + pen_button.width and pen_button.y < y < pen_button.y + pen_button.height:
                    pen_button.activate(self.penguin_button_list)
                elif pen_button.penguin.x < x < pen_button.penguin.x + pen_button.penguin.width and pen_button.penguin.y < y < pen_button.penguin.y + pen_button.penguin.height:
                    pen_button.activate(self.penguin_button_list)
        for fun_button in self.functionality_button_list:
            if fun_button.x < x < fun_button.x + fun_button.width and fun_button.y < y < fun_button.y + fun_button.height:
                fun_button.activate(game_info)
        for pla_button in self.player_button_list:
            if pla_button.x < x < pla_button.x + pla_button.width and pla_button.y < y < pla_button.y + pla_button.height:
                pla_button.activate(game_info)
