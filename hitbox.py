import pygame
import sys     # let  python use your file system
import numpy as np
import os
import time
from random import randrange
import game_menu

pygame.font.init()
pygame.mixer.init()

# Space that exist in the right part of the board (with buttons and messages)
LEFT_SPACE = 300
# Color for the space
BLUE = (0, 155, 155)
pygame.init()
# Size of the screen
dimx = 1000 + LEFT_SPACE
dimy = 1000
win = pygame.display.set_mode((dimx, dimy))
GAME_OVER = False
# Variable that indicates if another piece is in movement. In that case, it should not be possible to select another one
MOVEMENT = False
# Total score. This variable is used to change the next objective
SCORE = 0
STEPS = 0
REAL_MOVEMENT = False
BUTTON_LENGTH = 50
HOURGLASS = 60

PLAYER_NOT_SELECTED = False
RICOCHET = False

HITBOX_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hitbox.mp3'))
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Event that indicates when the goal is reached
GOAL_REACHED = pygame.USEREVENT+1
MOVED_CELL = pygame.USEREVENT+2

TIMER = False
FIRST_MOVEMENT = False
POSITION_LIST = []

# FPS=60
FPS = 120
# FPS=10
VEL = 5
# With this variable we adjust the hitbox of walls, so they are perfectly align,
# and they are also aligh witn the hitbox to be added
# Small adjustments so the hitboxes are displayed where expected
EPSILON = 2
CALIBRATION_X = 7-EPSILON
CALIBRATION_Y = 7-EPSILON

# Lists of coordinates of the edges of the board
X_COORD_LIST = [11, 72, 133, 194, 255, 316, 377, 438, 499, 560, 621, 682, 743, 804, 865, 926, 987]
Y_COORD_LIST = [20, 81, 142, 203, 264, 325, 386, 447, 508, 569, 630, 691, 752, 813, 874, 935, 996]

# Name of the game
pygame.display.set_caption("First Game")

COORDS_FONT = pygame.font.SysFont('comicsans', 40)
TEXT_FONT = pygame.font.SysFont('comicsans', 20)
TEXT_FONT1 = pygame.font.SysFont('comicsans', 12)

BLACK_PIECE = pygame.image.load(os.path.join('Assets', 'heroblack.png'))

# Board image
bg = pygame.image.load(os.path.join('Assets', 'board.png'))

clock = pygame.time.Clock()

player_list = []
pieces_list = []
INDEX = -1

def cell(x, y):
    # return (int(y/(1000/16)), int(x/(1000/16)))
    return int((x-11)/61), int((y-20)/61)


def coord(i, j):
    l = 58
    return (j*l+20, i*l+20)
    # return (j*(1000/16),i*(1000/16))


HW = np.zeros((17, 17))

# List of vertical walls, starting from top/left corner
VW_list = [(133, 20), (560, 20), (316, 81), (682, 81),
         (72, 203), (926, 203),
         (621, 264), (316, 325),
         (255, 386), (743, 386), (194, 508),
         (316, 569), (133, 630), (682, 630),
         (804, 691), (316, 752),
         (682, 752),
         (804, 813), (377, 874), (255, 935), (621, 935)]

'''
HW_list=[(255,81),(682,81),(926,142),
         (865,203),(72,264),(316,325),(560,325),(14,386),(194,447),(743,447),
         (133,508),(316,630),(682,630),(72,691),(255,752),(621,752),(804,752),(926,752),
         (14,813),(377,874),(743,874)]
'''
HW_list = [(255, 81), (682, 81), (926, 142),
         (865, 203), (72, 264), (316, 325), (560, 325), (14, 386), (194, 447), (743, 447),
         (133, 508), (316, 630), (682, 630), (72, 691), (255, 752), (621, 752), (804, 752), (926, 752),
         (14, 813), (377, 874), (743, 874)]
# (133, 501), (316, 623), (682, 623), (72, 684), (255, 745), (621, 745), (804, 745), (926, 745),
#         (14, 806), (377, 867), (743, 867)]


# Function to create the list of rectangles that define the hitbox for the walls
def walls_hitbox(VW_list, HW_list):
    # List of hitbox
    HB = []
    for vw in VW_list:
        hb = pygame.Rect(vw[0]-CALIBRATION_X, vw[1]+CALIBRATION_Y, 14-2*EPSILON, 40)
        HB.append(hb)
    for hw in HW_list:
        hb = pygame.Rect(hw[0]+CALIBRATION_X, hw[1]-CALIBRATION_Y, 40, 14-2*EPSILON)
        HB.append(hb)
    # Center block
    hb = pygame.Rect(438-CALIBRATION_X, 447-CALIBRATION_Y, 122+2*CALIBRATION_X, 122+2*CALIBRATION_Y)
    HB.append(hb)
    # Board boundaries

    lw = pygame.Rect(5-CALIBRATION_X, 0-CALIBRATION_Y, 0+2*CALIBRATION_X, 1000+2*CALIBRATION_Y)
    HB.append(lw)
    uw = pygame.Rect(0-CALIBRATION_X, 10-CALIBRATION_Y, 1000+2*CALIBRATION_X, 0+2*CALIBRATION_Y)
    HB.append(uw)
    rw = pygame.Rect(1000 - 10 - CALIBRATION_X, 0 - CALIBRATION_Y, 0 + 2 * CALIBRATION_X, 1000 + 2 * CALIBRATION_Y)
    HB.append(rw)
    dw = pygame.Rect(0 - CALIBRATION_X, 1000 - 10 - CALIBRATION_Y, 1000 + 2 * CALIBRATION_X, 0 + 2 * CALIBRATION_Y)
    HB.append(dw)
    return HB


# Class of the pieces of the game. They have their current position in screen, current cell in board,
# image, size, color, hitbox
class Penguin(object):
    # def __init__(self, x, y, width, height):
    # Constructor for the class. It only needs to know the initial position and color
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 49
        self.height = 48
        self.vel = VEL
        self.state = "standing"
        self.cell_x, self.cell_y = cell(self.x, self.y)
        self.old_cell_x = self.cell_x
        self.old_cell_y = self.cell_y
        self.hitbox_list = []
        self.hitbox_inactive = True
        self.image = pygame.image.load(os.path.join('Assets', "hero"+color+".png"))
        # self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.hitbox = (self.x + 49, self.y + 48, 49, 48)
        self.rect = pygame.Rect(self.x, self.y, 49, 89)



    def update_cell(self):
        self.old_cell_x = self.cell_x
        self.old_cell_y = self.cell_y
        self.cell_x, self.cell_y = cell(self.x, self.y)

    # This function updates the current hitbox and cell of the piece
    def handle_hitbox(self):
        '''
        self.old_cell_x = self.cell_x
        self.old_cell_y = self.cell_y
        self.cell_x, self.cell_y = cell(self.x, self.y)
        '''
        # self.update_cell()

        hitbox_left_x = X_COORD_LIST[self.cell_x] - CALIBRATION_X
        hitbox_left_y = Y_COORD_LIST[self.cell_y] + CALIBRATION_Y
        hitbox_left = pygame.Rect(hitbox_left_x, hitbox_left_y, 14 - 2 * EPSILON, 40)
        hitbox_up_x = X_COORD_LIST[self.cell_x] + CALIBRATION_X
        hitbox_up_y = Y_COORD_LIST[self.cell_y] - CALIBRATION_Y
        hitbox_up = pygame.Rect(hitbox_up_x, hitbox_up_y, 40, 14 - 2 * EPSILON)
        hitbox_right_x = X_COORD_LIST[self.cell_x+1] - CALIBRATION_X
        hitbox_right_y = Y_COORD_LIST[self.cell_y] + CALIBRATION_Y
        hitbox_right = pygame.Rect(hitbox_right_x, hitbox_right_y, 14 - 2 * EPSILON, 40)
        hitbox_down_x = X_COORD_LIST[self.cell_x] + CALIBRATION_X
        hitbox_down_y = Y_COORD_LIST[self.cell_y+1] - CALIBRATION_Y
        hitbox_down = pygame.Rect(hitbox_down_x, hitbox_down_y, 40, 14 - 2 * EPSILON)
        # self.hitbox_up = pygame.Rect()
        self.hitbox_list = []
        self.hitbox_list.append(hitbox_left)
        self.hitbox_list.append(hitbox_up)
        self.hitbox_list.append(hitbox_right)
        self.hitbox_list.append(hitbox_down)

    # Draws the piece
    def draw(self, win):
        # win.blit(BLACK_PIECE, (self.x, self.y))
        win.blit(self.image, (self.x, self.y))

        # self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.hitbox = (self.x, self.y, 49, 48)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


# Class of the objectives in the game. They know their color, position, image
class Tile(object):

    def __init__(self, x, y, color="rainbow", shape=""):
        self.x = x
        self.y = y
        self.cell_x, self.cell_y = cell(x, y)
        self.color = color
        self.active = False
        if color == "rainbow":
            self.image = pygame.image.load(os.path.join('Assets', "rainbow-tile.png"))
        else:
            self.image = pygame.image.load(os.path.join('Assets', shape + "-" + color + "-tile.png"))

    # Draws itself
    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    # Creates a copy of itself (that will be displayed in the center as the objective
    def copy(self, tile):
        self.x = tile.x
        self.y = tile.y
        self.cell_x = tile.cell_x
        self.cell_y = tile.cell_y
        self.color = tile.color
        self.image = tile.image

# Class for the players. It knows their name, score
class Player(object):
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.bid_status = False
        self.bid = 0

AUX_PLAYER = Player("None")
ACTIVE_PLAYER = AUX_PLAYER

# Class of buttons. Buttons are used to select pieces to move, set timer, go back some steps, restart the game
class Button(object):
    # We specify the location, size and function of the button (character, timer, go back, etc)
    # The constructor needs to know the position, size, function of button and color (assuming it is linked to a piece)
    def __init__(self, x, y, width, height, function, color=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.function = function
        self.pushed = False
        # self.player = ""
        self.score = 0
        if function == "Piece":

            self.color = color
            self.piece = Penguin(0, 0, "blue")
            # Depending on the color of the piece, the image is selected
            if color == "red":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'herored.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                #self.piece = red
            if color == "yellow":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'heroyellow.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                #self.piece = yellow
            if color == "blue":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'heroblue.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                #self.piece = blue
            if color == "green":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'herogreen.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                #self.piece = green
            if color == "black":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'heroblack.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                #self.piece = black
        # If this is not a piece button, then we check its function
        elif self.function == "Restart position":
            self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Blank.png')), (100, 20))
        else:
            self.image = pygame.image.load(os.path.join('Assets', 'Blank.png'))

    def draw(self, win):
        # TEXT_FONT = pygame.font.SysFont('comicsans', 20)

        win.blit(self.image, (self.x, self.y))
        if self.function == "Piece":
            pass
        elif self.function == "Player":
            name_info = TEXT_FONT1.render(self.player.name, True, (0, 0, 0))
            if self.player.bid_status:
                score_info = TEXT_FONT1.render("Score: " + str(self.player.score) + "   Bid: " + str(self.player.bid), True, (0, 0, 0))
            else:
                score_info = TEXT_FONT1.render("Score: " + str(self.player.score), True, (0, 0, 0))
            win.blit(name_info, (self.x, self.y))
            win.blit(score_info, (self.x + BUTTON_LENGTH + 5, self.y))
        else:
            button_info = TEXT_FONT1.render(self.function, True, (0, 0, 0))
            win.blit(button_info, (self.x, self.y))


    # The activate function will depend on the pressed button
    def activate(self):
        global SCORE
        global TIMER
        global ACTIVE_PLAYER
        global PLAYER_NOT_SELECTED
        global HOURGLASS
        global INDEX
        global STEPS
        if self.function == "Restart":
            SCORE = 0
            main(player_list)
        if self.function == "Time":
            TIMER = True
        if self.function == "Start yes":
            self.pushed = True
        if self.function == "Start no":
            self.pushed = True
        if self.function == "Player":
            # print(self.player.name)
            ACTIVE_PLAYER = self.player
            TIMER = True
            PLAYER_NOT_SELECTED = False
            self.player.bid = game_menu.bid(self.player.bid_status, self.player.name, self.player.bid)
            self.player.bid_status = True
            # game_menu.inputBox("")
        if self.function == "Rules":
            path = os.path.join('Assets','rules.pdf')
            os.system("open " + path)
            #os.system("open Assets/rules.pdf")
        if self.function == "Settings":
            HOURGLASS = game_menu.adjustTime()
        if self.function == "Back":
            n = len(POSITION_LIST)
            if INDEX > 0:
                STEPS -= 2
                INDEX -= 1
                aux = 0
                for p in pieces_list:
                    p.x = POSITION_LIST[INDEX][aux][0]
                    p.y = POSITION_LIST[INDEX][aux][1]
                    aux +=1
            print("Back")
        if self.function == "Forward":
            print("Forward")
            n = len(POSITION_LIST)
            if INDEX < n-1:
                INDEX += 1
                aux = 0
                for p in pieces_list:
                    p.x = POSITION_LIST[INDEX][aux][0]
                    p.y = POSITION_LIST[INDEX][aux][1]
                    aux +=1

        if self.function == "Print list":
            print(POSITION_LIST)
        if self.function == "Restart position":
            INDEX = -1
            aux = 0
            for p in pieces_list:
                p.x = POSITION_LIST[0][aux][0]
                p.y = POSITION_LIST[0][aux][1]
                aux += 1


        # self.hitbox = (self.x, self.y, 49, 48)

# This function draws the board, pieces, score and everything displayed in screen
def drawGameWindow(HB, tile_list, pieces_list, button_list, coord_x, coord_y, objective, remaining_seconds, steps, player_list):
    win.fill(BLUE)
    win.blit(bg, (0, 0))
    for w in HB:
        pygame.draw.rect(win, (255, 0, 0), w)
    for t in tile_list:
        t.draw(win)
    for piece in pieces_list:
        piece.draw(win)
    objective.draw(win)
    # steps = 0
    steps_info = TEXT_FONT.render("Number of steps: " + str(steps), True, (255, 255, 0))
    # win.blit(steps_info, (1000, 220))
    aux = 10
    for button in button_list:
        # if button.function == "Piece":
        #    button_info = TEXT_FONT.render("Pushed " + button.color + " button? " + str(button.pushed), True, (255, 255, 0))

            # win.blit(button_info, (1000, 200 + aux*20))
            # aux += 1
        button.draw(win)

    # '''
    score_info = TEXT_FONT.render("Tokens obtained: " + str(SCORE), True, (255, 255, 0))
    win.blit(score_info, (1000, 200 + aux * 20))
    steps_info = TEXT_FONT.render("GLOBAL Steps: " + str(STEPS), True, (255, 255, 0))
    win.blit(steps_info, (1000, 200 + (aux + 1) * 20))
    time_info = TEXT_FONT.render("Time: " + str(remaining_seconds), True, (255, 255, 0))
    win.blit(time_info, (1000, 200 + (aux + 2) * 20))
    timer_info = TEXT_FONT.render("Time: " + str(TIMER), True, (255, 255, 0))
    win.blit(timer_info, (1000, 200 + (aux + 3) * 20))
    steps01_info = TEXT_FONT.render("Steps: " + str(steps), True, (255, 255, 0))
    win.blit(steps01_info, (1000, 200 + (aux + 4) * 20))
    steps01_info = TEXT_FONT.render("Active player: " + str(ACTIVE_PLAYER.name), True, (255, 255, 0))
    win.blit(steps01_info, (1000, 200 + (aux + 5) * 20))
    waiting_info = TEXT_FONT.render("Waiting time: " + str(HOURGLASS), True, (255, 255, 0))
    win.blit(waiting_info, (1000, 200 + (aux + 6) * 20))
    INDEX_info = TEXT_FONT.render("INDEX: " + str(INDEX), True, (255, 255, 0))
    win.blit(INDEX_info, (1000, 200 + (aux + 7) * 20))
    # '''
    pieces_text = TEXT_FONT.render("Select your piece", True, (255, 255, 0))
    coords_text = COORDS_FONT.render("Coords: " + str(coord_x) + "," + str(coord_y), True, (255, 0, 255))


    '''
    for p in player_list:
        but = Button(1000, 200 + aux*20 +50, 50, 20, "Player")
        but.player = p.name
        but.draw(win)
        aux += 1
    #'''
    win.blit(coords_text, (10, 10))
    win.blit(pieces_text, (1000, 20))
    if PLAYER_NOT_SELECTED:
        unselected_text = TEXT_FONT.render("Select a player before moving", True, (255, 255, 0))
        win.blit(unselected_text, (1000, 200 ))


    pygame.display.update()

# We verify if a button was pushed. If it is a piece, the other pieces should deactivate and the pushed
# piece should become active. This is the piece that we will move.
def handle_clicks(x,y, button_list):
    for button in button_list:
        if button.x < x and x < button.x + button.width and button.y < y and y < button.y + button.height:
            if button.function == "Piece" and MOVEMENT == False:
                for but in button_list:
                    if but.function == "Piece":
                        but.pushed = False
                        but.image = but.image_nonactive
                button.pushed = True
                button.image = button.image_active
            else:
                button.activate()
        elif button.function == "Piece" and MOVEMENT == False:
            if button.piece.x < x and x < button.piece.x + button.piece.width and button.piece.y < y and y < button.piece.y + button.piece.height:
                for but in button_list:
                    if but.function == "Piece":
                        but.pushed = False
                        but.image = but.image_nonactive
                button.pushed = True
                button.image = button.image_active

# This function indicates if the piece would hit a wall in the indicated direction
def hit_wall(HB, direction, piece):
    epsilon = 10
    if direction == "left":
        aux = pygame.Rect(piece.x-piece.vel, piece.y, 49-epsilon, 49-epsilon)
        for hb in HB:
            if aux.colliderect(hb):
                piece.state = "standing"
                piece.handle_hitbox()
                break
    if direction == "right":
        aux = pygame.Rect(piece.x+piece.vel, piece.y, 49-epsilon, 49-epsilon)
        for hb in HB:
            if aux.colliderect(hb):
                piece.state = "standing"
                piece.handle_hitbox()
                break
    if direction == "up":
        aux = pygame.Rect(piece.x, piece.y-piece.vel, 49-epsilon, 49-epsilon)
        for hb in HB:
            if aux.colliderect(hb):
                piece.state = "standing"
                piece.handle_hitbox()
                #for b in piece.hitbox_list:
                #    HB.append(b)
                # HITBOX_SOUND.play()
                break
    if direction == "down":
        aux = pygame.Rect(piece.x, piece.y+piece.vel, 49-epsilon, 49-epsilon)
        for hb in HB:
            if aux.colliderect(hb):
                piece.state = "standing"
                piece.handle_hitbox()
                break
    return HB


# Handles the movement of the pieces, and verifies the conditions
def handleMovement(keys, HB, piece, tile_list, objective, pieces_list):
    ind_r, ind_c = cell(piece.x, piece.y)
    global SCORE
    global MOVEMENT
    global STEPS
    global REAL_MOVEMENT
    global AUX_PLAYER
    global ACTIVE_PLAYER
    global PLAYER_NOT_SELECTED
    step = False
    # if ACTIVE_PLAYER != AUX_PLAYER:
    if True:
        if keys[pygame.K_LEFT] and piece.state == "standing":
            piece.state = "left"
            MOVEMENT = True
            step = True
        elif keys[pygame.K_RIGHT] and piece.state == "standing":
            piece.state = "right"
            MOVEMENT = True
            step = True
        elif keys[pygame.K_DOWN] and piece.state == "standing":
            piece.state = "down"
            MOVEMENT = True
            step = True
        elif keys[pygame.K_UP] and piece.state == "standing":
            piece.state = "up"
            MOVEMENT = True
            step = True

        HB = hit_wall(HB, piece.state, piece)
        if piece.state == "left" and piece.x > piece.vel:
            piece.x -= piece.vel
            piece.handle_hitbox()
            # if step:
            #    STEPS += 1
        elif piece.state == "right" and piece.x < dimx - piece.width - piece.vel - LEFT_SPACE:
            piece.x += piece.vel
            piece.handle_hitbox()
            # if step:
            #    STEPS += 1
        elif piece.state == "down" and piece.y < dimy - piece.height - piece.vel:
            piece.y += piece.vel
            piece.handle_hitbox()
            # if step:
            #    STEPS += 1
        elif piece.state == "up" and piece.y > piece.vel:
            piece.y -= piece.vel
            piece.handle_hitbox()
            # if step:
            #    STEPS += 1
        else:
            if objective.cell_x == piece.cell_x and objective.cell_y == piece.cell_y:
                if STEPS != 0 and objective.color == piece.color or objective.color == "rainbow":
                    pygame.event.post(pygame.event.Event(GOAL_REACHED))
                    ACTIVE_PLAYER.score += 1
                    ACTIVE_PLAYER = AUX_PLAYER
                    SCORE += 1
                    objective.cell_x = 20
                    STEPS = 0
            piece.state = "standing"
            piece.update_cell()
            piece.handle_hitbox()
            if piece.cell_x != piece.old_cell_x or piece.cell_y != piece.old_cell_y:
                # print("here")
                updatePositionList(pieces_list)
                pygame.event.post(pygame.event.Event(MOVED_CELL))
                REAL_MOVEMENT = True
            piece.standing = True
            MOVEMENT = False
    else:
        PLAYER_NOT_SELECTED = True


# HB is a list of hitboxes, mostly from walls. This function adds or eliminates hitboxes of the pieces,
# depending on the needs
def update_HB(HB, piece_list, piece):
    for p in piece_list:
        if p.hitbox_inactive:
            for hb in p.hitbox_list:
                HB.append(hb)
            p.hitbox_inactive = False
    for hb in piece.hitbox_list:
        HB.remove(hb)
    piece.hitbox_inactive = True
    return HB

# This function creates the token list (the positions, images)
def create_tile_list():
    tile_list = []
    mr = Tile(695, 93, "red", "moon")
    mb = Tile(86, 635, "blue", "moon")
    my = Tile(753, 817, "yellow", "moon")
    mg = Tile(268, 93, "green", "moon")
    tile_list.append(mr)
    tile_list.append(mb)
    tile_list.append(my)
    tile_list.append(mg)

    sr = Tile(271, 759, "red", "star")
    sb = Tile(208, 394, "blue", "star")
    sy = Tile(753, 398, "yellow", "star")
    sg = Tile(694, 636, "green", "star")
    tile_list.append(sr)
    tile_list.append(sb)
    tile_list.append(sy)
    tile_list.append(sg)

    pr = Tile(819, 698, "red", "planet")
    pb = Tile(566, 268, "blue", "planet")
    py = Tile(329, 333, "yellow", "planet")
    pg = Tile(329, 572, "green", "planet")
    tile_list.append(pr)
    tile_list.append(pb)
    tile_list.append(py)
    tile_list.append(pg)

    tr = Tile(86, 212, "red", "triangle")
    tb = Tile(631, 760, "blue", "triangle")
    ty = Tile(393, 882, "yellow", "triangle")
    tg = Tile(870, 215, "green", "triangle")
    tile_list.append(tr)
    tile_list.append(tb)
    tile_list.append(ty)
    tile_list.append(tg)

    rb = Tile(145, 517)
    tile_list.append(rb)

    return tile_list

# This function initializes the pieces and buttons
def initialize_pieces_buttons(player_list=[]):
    pieces_list = []
    # black = Penguin(200, 23, "black")
    # pieces_list.append(black)
    # '''
    yellow = Penguin(377 + CALIBRATION_X, 874 + CALIBRATION_Y, "yellow")
    pieces_list.append(yellow)
    green = Penguin(865 + CALIBRATION_X, 203 + CALIBRATION_Y, "green")
    pieces_list.append(green)
    red = Penguin(926 + CALIBRATION_X, 325 + CALIBRATION_Y, "red")
    pieces_list.append(red)
    blue = Penguin(560 + CALIBRATION_X, 264 + CALIBRATION_Y, "blue")
    pieces_list.append(blue)
    for p in pieces_list:
        p.handle_hitbox()
    # '''

    button_list = []
    button_yellow = Button(1000, 50, 50, 50, "Piece", "yellow")
    button_yellow.piece = yellow
    button_list.append(button_yellow)
    button_red = Button(1050, 50, 50, 50, "Piece", "red")
    button_red.piece = red
    button_list.append(button_red)
    button_blue = Button(1000, 100, 50, 50, "Piece", "blue")
    button_blue.piece = blue
    button_list.append(button_blue)
    button_green = Button(1050, 100, 50, 50, "Piece", "green")
    button_green.piece = green
    button_list.append(button_green)
    '''
    if BLACK:
        button_black = Button(1000, 150, 50, 50, "Piece", "black")
        button_black.piece = black
        button_list.append(button_black)
    '''
    button_restart = Button(1000, 240, 50, 20, "Restart")
    button_list.append(button_restart)
    button_timer = Button(1000, 200, 50, 20, "Time")
    button_list.append(button_timer)
    button_rules = Button(1000, 180, 50, 20, "Rules")
    button_list.append(button_rules)
    button_settings = Button(1000, 220, 50, 20, "Settings")
    button_list.append(button_settings)

    button_back = Button(1050, 200, 50, 20, "Back")
    button_list.append(button_back)
    button_forward = Button(1100, 200, 50, 20, "Forward")
    button_list.append(button_forward)
    button_print = Button(1100, 250, 50, 20, "Print list")
    button_list.append(button_print)
    button_restart_position = Button(1100, 350, 100, 20, "Restart position")
    button_list.append(button_restart_position)

    aux = 1
    for p in player_list:
        but = Button(1000, 200 + aux * 20 + 50, 50, 20, "Player")
        but.player = p

        # but.draw(win)
        aux += 1
        button_list.append(but)

    return pieces_list, button_list

# This function indicates the winner
def draw_winer(text="GAME OVER"):
    draw_text = WINNER_FONT.render(text, True, (255, 255, 0))
    win.blit(draw_text, (1000//2-draw_text.get_width()//2, 1000//2-draw_text.get_height()//2))
    pygame.display.update()
    # The delay is computed as 1000* seconds
    pygame.time.delay(10000)

# This function creates a random list to show objectives every time a new one is needed
def create_random_list(n):
    aux = [i for i in range(n)]
    random_list = []
    for i in range(n):
        random_list.append(aux.pop(randrange(1000) % len(aux)))
    return random_list

# This function asks for the number of players, and names if the want to use them
def players():
    print("Enter number of players: ")

    waiting_valid_number = True
    while waiting_valid_number:
        number = input()
        try:
            n = int(number)
            if n > 0:
                waiting_valid_number = False
            else:
                print("Please enter a valid number of players: ")
        except:
            print("Please enter a valid number of players: ")
    print("Do you want to name the players? Y or N")
    waiting_valid_input = True
    answer = ""
    while waiting_valid_input:
        answer = input()
        if answer != "Y" and answer != "y" and answer != "N" and answer != "n":
            print("Please answer Y or N")
        else:
            waiting_valid_input = False
    names_list = []
    if answer == "N" or answer == "n":
        for i in range(n):
            names_list.append(Player("Player " + str(i+1)))
        return names_list
    else:
        for i in range(n):
            print("Name the player number ", i+1)
            name = input()
            names_list.append(Player(name))

    return names_list


def updatePositionList(pieces_list):
    global INDEX
    aux_list = []
    for p in pieces_list:
        # print(p)
        aux_list.append((p.x, p.y))
        # print(p)
    POSITION_LIST.append(aux_list)
    INDEX += 1
    # print(POSITION_LIST)

# This is the main function
def main(player_list=[Player("Player 1")]):
    global SCORE
    global GOAL_REACHED
    global FIRST_MOVEMENT
    global TIMER
    global REAL_MOVEMENT
    global STEPS
    global POSITION_LIST
    global pieces_list
    global INDEX


    HB = walls_hitbox(VW_list, HW_list)
    tile_list = create_tile_list()
    random_list = create_random_list(len(tile_list))
    # print(len(random_list))
    # print(random_list)
    for p in player_list:
        p.score = 0


    aux = Tile(499 - 20, 508 - 20)
    objective_index = random_list[SCORE]
    aux.copy(tile_list[objective_index])
    objective = aux

    objective.x = 499 - 20
    objective.y = 508 - 20
    pieces_list, button_list = initialize_pieces_buttons(player_list)

    INDEX = -1
    POSITION_LIST = []
    updatePositionList(pieces_list)
    # mainloop

    FIRST_MOVEMENT = False
    remaining_seconds = 0
    steps = 0
    STEPS = 0

    run = True

    # '''
    while run:
        clock.tick(FPS)
        coord_x, coord_y = pygame.mouse.get_pos()
        # An action may be done depending on the input from mouse and keyboard

        for event in pygame.event.get():
            # Close the game if Q is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    pygame.quit()
                    sys.exit()
                    # run = False
                # if event.key == ord('c'):
                #     game_menu.players2()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_clicks(coord_x, coord_y, button_list)
                # run = False
        for button in button_list:
            if button.pushed == True:
                keys = pygame.key.get_pressed()
                HB = update_HB(HB, pieces_list, button.piece)
                handleMovement(keys, HB, button.piece, tile_list, objective, pieces_list)
        if TIMER:
            FIRST_MOVEMENT = True
            if remaining_seconds == 0:
                start_time = int(time.time())
            TIMER = False

        if FIRST_MOVEMENT == False:
            remaining_seconds = 0
        else:
            # remaining_seconds = 15 - (int(time.time() -int(start_time)))
            # remaining_seconds = 60 - (int(time.time() - int(start_time)))
            remaining_seconds = HOURGLASS - (int(time.time() - int(start_time)))
            if remaining_seconds <= 0:
                remaining_seconds = 0
                TIMER = False


        if REAL_MOVEMENT:
            REAL_MOVEMENT = False
            STEPS += 1
            steps += 1
            # print("here01", steps)


        drawGameWindow(HB, tile_list, pieces_list, button_list, coord_x, coord_y, objective, remaining_seconds, steps, player_list)
        # If the goal is reached, a new objective is generated
        try:
            if event.type == GOAL_REACHED:
                # SCORE += 1
                # HITBOX_SOUND.play()
                # print("goal reached")
                steps = 0
                STEPS = 0
                POSITION_LIST = []
                INDEX = -1
                updatePositionList(pieces_list)
                if SCORE < 5: # len(tile_list):
                    aux = Tile(499-20, 508-20)
                    objective_index = random_list[SCORE]
                    # print(objective_index)
                    # objective = tile_list[objective_index]
                    aux.copy(tile_list[objective_index])
                    objective = aux
                    objective.x = 499 - 20
                    objective.y = 508 - 20
                else:
                    GAME_OVER = True
                    draw_winer()
                    # main()
        except:
            pass


    pygame.quit()
    # '''

player1 = Player("Player 1")
player2 = Player("Player 2")
player_list = [player1, player2]


if __name__ == "__main__":
    # game_menu.game_start()
    main(player_list)
    # main(game_menu.players2())
    # main()