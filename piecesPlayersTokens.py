import pygame
import sys     # let  python use your file system
import numpy as np
import os
import time
from random import randrange
import game_menu


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







# To convert into a Penguin method

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




# To convert into a Penguin method


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


# Related to Penguin

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


# Convert into player method

def bid(bidding, name, steps=0):
    waiting_bid = True
    req1 = "What is your new bid " + name + "?"
    req2 = "Please write a valid bid " + name
    exp1 = "(You must introduce a number  of steps for your solution)"
    exp2 = "(The number of steps must be lower than your previous bid " + str(steps) + ")"
    if bidding:

        while waiting_bid:

            try:
                new_bid = int(inputBox(req1, exp1))
                if new_bid > steps:
                    req1 = req2
                    exp1 = exp2
                else:
                    waiting_bid = False
                    return new_bid
            except:
                req1 = req2


    else:
        while waiting_bid:
            try:
                new_bid = int(inputBox(req1, exp1))
                waiting_bid = False
            except:
                req1 = req2
        return new_bid


