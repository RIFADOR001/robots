import pygame
import os
from main import main_function
from game_menu import adjustTime, bid
# from game_info import GameInfo
# from piecesPlayersTokens import Penguin, Player


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
        self.piece = penguin
        # Depending on the color of the piece, the image is selected
        self.image_nonactive = pygame.image.load(os.path.join("Assets", f"hero{self.color}.png"))
        self.image = self.image_nonactive
        self.image_active = pygame.image.load(os.path.join("Assets", f"{self.color}_active.png"))


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

    def activate(self, game):
        game.active_player = self.player
        game.timer = True
        game.player_not_selected = False
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
                for p in game_info.pieces_list:
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
            main_function(game_info)
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



