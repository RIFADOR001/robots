import os
from board_geometry import cell, CALIBRATION_X, CALIBRATION_Y, X_COORD_LIST, Y_COORD_LIST, EPSILON, NEW_X_COORD_LIST
from game_config import*
from graphics import input_box

VEL = 5


# Class of the pieces of the game. They have their current position in screen, current cell in board,
# image, size, color, hitbox
class Penguin(object):
    # def __init__(self, x, y, width, height):
    # Constructor for the class. It only needs to know the initial position and color
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 24 #49
        self.height = 24 #48
        self.vel = VEL
        self.state = "standing"
        self.cell_x, self.cell_y = cell(self.x, self.y)
        self.old_cell_x = self.cell_x
        self.old_cell_y = self.cell_y
        self.hitbox_list = []
        self.hitbox_inactive = True
        image = pygame.image.load(os.path.join('Assets', "hero"+color+".png"))
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.hitbox = (self.x + self.width, self.y + self.height, self.width, self.height)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.button = None

    def update_cell(self):
        self.old_cell_x = self.cell_x
        self.old_cell_y = self.cell_y
        self.cell_x, self.cell_y = cell(self.x, self.y)

    # This function updates the current hitbox and cell of the piece
    def handle_hitbox(self):
        # NEW_X_COORD_LIST
        hitbox_left_x = NEW_X_COORD_LIST[self.cell_x]  # - 5
        hitbox_left_y = NEW_X_COORD_LIST[self.cell_y] + 5
        hitbox_left = pygame.Rect(hitbox_left_x, hitbox_left_y, 4, 10)
        hitbox_up_x = NEW_X_COORD_LIST[self.cell_x] + 5
        hitbox_up_y = NEW_X_COORD_LIST[self.cell_y]  # - 5
        hitbox_up = pygame.Rect(hitbox_up_x, hitbox_up_y, 10, 4)
        hitbox_right_x = NEW_X_COORD_LIST[self.cell_x+1]  # - 5
        hitbox_right_y = NEW_X_COORD_LIST[self.cell_y] + 5
        hitbox_right = pygame.Rect(hitbox_right_x, hitbox_right_y, 4, 10)
        hitbox_down_x = NEW_X_COORD_LIST[self.cell_x] + 5
        hitbox_down_y = NEW_X_COORD_LIST[self.cell_y+1]  # - 5
        hitbox_down = pygame.Rect(hitbox_down_x, hitbox_down_y, 10, 4)
        # self.hitbox_up = pygame.Rect()
        self.hitbox_list = []
        self.hitbox_list.append(hitbox_left)
        self.hitbox_list.append(hitbox_up)
        self.hitbox_list.append(hitbox_right)
        self.hitbox_list.append(hitbox_down)

    # Draws the piece
    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)

    # This function changes the state if the piece would hit a wall in the indicated direction
    # The state is either moving or standing
    def hit_wall(self, hitbox_list):
        epsilon = 10
        if self.state == "left":
            aux = pygame.Rect(self.x - self.vel, self.y, self.width, self.height)
            for hb in hitbox_list:
                if aux.colliderect(hb):
                    self.state = "standing"
                    self.handle_hitbox()
                    break
        if self.state == "right":
            aux = pygame.Rect(self.x + self.vel, self.y, self.width, self.height)
            for hb in hitbox_list:
                if aux.colliderect(hb):
                    self.state = "standing"
                    self.handle_hitbox()
                    break
        if self.state == "up":
            aux = pygame.Rect(self.x, self.y - self.vel, self.width, self.height)
            for hb in hitbox_list:
                if aux.colliderect(hb):
                    self.state = "standing"
                    self.handle_hitbox()
                    break
        if self.state == "down":
            aux = pygame.Rect(self.x, self.y + self.vel, self.width, self.height)
            for hb in hitbox_list:
                if aux.colliderect(hb):
                    self.state = "standing"
                    self.handle_hitbox()
                    break

    # Handles the movement of the pieces, and verifies the conditions
    def handle_movement(self, keys, game_info):
        step = False
        # if ACTIVE_PLAYER != AUX_PLAYER:
        if True:
            if keys[pygame.K_LEFT] and self.state == "standing":
                self.state = "left"
                game_info.movement = True
                step = True
            elif keys[pygame.K_RIGHT] and self.state == "standing":
                self.state = "right"
                game_info.movement = True
                step = True
            elif keys[pygame.K_DOWN] and self.state == "standing":
                self.state = "down"
                game_info.movement = True
                step = True
            elif keys[pygame.K_UP] and self.state == "standing":
                self.state = "up"
                game_info.movement = True
                step = True

            self.hit_wall(game_info.lists.hitbox_list)
            if self.state == "left" and self.x > self.vel:
                self.x -= self.vel
                self.handle_hitbox()
                # if step:
                #    STEPS += 1
            elif self.state == "right" and self.x < dimx - self.width - self.vel - LEFT_SPACE:
                self.x += self.vel
                self.handle_hitbox()
                # if step:
                #    STEPS += 1
            elif self.state == "down" and self.y < dimy - self.height - self.vel:
                self.y += self.vel
                self.handle_hitbox()
                # if step:
                #    STEPS += 1
            elif self.state == "up" and self.y > self.vel:
                self.y -= self.vel
                self.handle_hitbox()
                # if step:
                #    STEPS += 1
            else:
                if game_info.objective.cell_x == self.cell_x and game_info.objective.cell_y == self.cell_y:
                    if game_info.steps != 0 and game_info.objective.color == self.color or game_info.objective.color == "rainbow":
                        pygame.event.post(pygame.event.Event(game_info.goal_reached))
                        if game_info.active_player is not None:  # here (Erase if, this is only for quick testing)
                            game_info.active_player.score += 1
                        game_info.active_player = None
                        game_info.tokens += 1
                        game_info.objective.cell_x = 20
                        game_info.steps = 0
                        game_info.update_objective()
                self.state = "standing"
                self.update_cell()
                self.handle_hitbox()
                if self.cell_x != self.old_cell_x or self.cell_y != self.old_cell_y:
                    # print("here")
                    game_info.update_position_list()
                    pygame.event.post(pygame.event.Event(game_info.moved_cell))
                    game_info.real_movement = True
                self.state = "standing"
                game_info.movement = False
        else:
            game_info.player_not_selected = True


# Class of the objectives in the game. They know their color, position, image
class Token(object):

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

    def bid(self, bidding_state, steps=0):
        waiting_bid = True
        req1 = f"What is your new bid {self.name}?"
        req2 = f"Please write a valid bid {self.name}"
        exp1 = "(You must introduce a number  of steps for your solution)"
        exp2 = f"(The number of steps must be lower than your previous bid {steps})"
        new_bid = None
        if bidding_state:
            while waiting_bid:
                try:
                    new_bid = int(input_box(req1, exp1))
                    if new_bid > steps:
                        req1 = req2
                        exp1 = exp2
                    else:
                        waiting_bid = False
                except ValueError:
                    req1 = req2
        else:
            while waiting_bid:
                try:
                    new_bid = int(input_box(req1, exp1))
                    waiting_bid = False
                except ValueError:
                    req1 = req2
            self.bid_status = True
        self.bid = new_bid


class ListsPenguinPlayersHitbox(object):
    def __init__(self, player_list, hitbox_list, positions=None):
        self.hitbox_list = hitbox_list
        self.penguins_list = create_penguin_list(positions)
        self.players_list = player_list

    def draw(self, win):
        for pen in self.penguins_list:
            pen.draw(win)

    def reset_bid(self):
        for p in self.players_list:
            p.bid = None
            p.bid_status = False

    # HB is a list of hitboxes, mostly from walls. This function adds or eliminates hitboxes of the pieces,
    # depending on the needs
    def update_hitbox(self, penguin):
        for p in self.penguins_list:
            if p.hitbox_inactive:
                for hb in p.hitbox_list:
                    self.hitbox_list.append(hb)
                p.hitbox_inactive = False
        for hb in penguin.hitbox_list:
            self.hitbox_list.remove(hb)
        penguin.hitbox_inactive = True


def create_penguin_list(positions=None):
    aux_penguin_list = []
    if positions is None:
        '''
        penguin1 = Penguin(560 + CALIBRATION_X, 264 + CALIBRATION_Y, "blue")
        aux_penguin_list.append(penguin1)
        penguin2 = Penguin(865 + CALIBRATION_X, 203 + CALIBRATION_Y, "green")
        aux_penguin_list.append(penguin2)
        penguin3 = Penguin(926 + CALIBRATION_X, 325 + CALIBRATION_Y, "red")
        aux_penguin_list.append(penguin3)
        penguin4 = Penguin(377 + CALIBRATION_X, 874 + CALIBRATION_Y, "yellow")
        aux_penguin_list.append(penguin4)
        '''
        # aux_penguin_list.append(Penguin(560 + CALIBRATION_X, 264 + CALIBRATION_Y, "blue"))
        aux_penguin_list.append(Penguin(6, 6, "blue"))
        aux_penguin_list.append(Penguin(6, 490, "green"))
        aux_penguin_list.append(Penguin(490, 6, "red"))
        aux_penguin_list.append(Penguin(490, 490, "yellow"))

    else:
        aux_penguin_list.append(Penguin(positions[0][0] + CALIBRATION_X, positions[0][1] + CALIBRATION_Y, "blue"))
        aux_penguin_list.append(Penguin(positions[1][0] + CALIBRATION_X, positions[1][1] + CALIBRATION_Y, "green"))
        aux_penguin_list.append(Penguin(positions[2][0] + CALIBRATION_X, positions[2][1] + CALIBRATION_Y, "red"))
        aux_penguin_list.append(Penguin(positions[3][0] + CALIBRATION_X, positions[3][1] + CALIBRATION_Y, "yellow"))
    for p in aux_penguin_list:
        p.handle_hitbox()
    return aux_penguin_list


# This function creates the token list (the positions, images)
def create_token_list():
    token_list = []
    # mr = Token(695, 93, "red", "moon")
    # mb = Token(86, 635, "blue", "moon")
    # my = Token(753, 817, "yellow", "moon")
    # mg = Token(268, 93, "green", "moon")
    mr = Token(4 + NEW_X_COORD_LIST[11], 4 + NEW_X_COORD_LIST[1], "red", "moon")
    mb = Token(4 + NEW_X_COORD_LIST[1], 4 + NEW_X_COORD_LIST[10], "blue", "moon")
    my = Token(4 + NEW_X_COORD_LIST[12], 4 + NEW_X_COORD_LIST[13], "yellow", "moon")
    mg = Token(4 + NEW_X_COORD_LIST[4], 4 + NEW_X_COORD_LIST[1], "green", "moon")
    token_list.append(mr)
    token_list.append(mb)
    token_list.append(my)
    token_list.append(mg)

    # sr = Token(271, 759, "red", "star")
    # sb = Token(208, 394, "blue", "star")
    # sy = Token(753, 398, "yellow", "star")
    # sg = Token(694, 636, "green", "star")
    sr = Token(4 + NEW_X_COORD_LIST[4], 4 + NEW_X_COORD_LIST[12], "red", "star")
    sb = Token(4 + NEW_X_COORD_LIST[3], 4 + NEW_X_COORD_LIST[6], "blue", "star")
    sy = Token(4 + NEW_X_COORD_LIST[12], 4 + NEW_X_COORD_LIST[6], "yellow", "star")
    sg = Token(4 + NEW_X_COORD_LIST[11], 4 + NEW_X_COORD_LIST[10], "green", "star")
    token_list.append(sr)
    token_list.append(sb)
    token_list.append(sy)
    token_list.append(sg)

    # pr = Token(819, 698, "red", "planet")
    # pb = Token(566, 268, "blue", "planet")
    # py = Token(329, 333, "yellow", "planet")
    # pg = Token(329, 572, "green", "planet")
    pr = Token(4 + NEW_X_COORD_LIST[13], 4 + NEW_X_COORD_LIST[11], "red", "planet")
    pb = Token(4 + NEW_X_COORD_LIST[9], 4 + NEW_X_COORD_LIST[4], "blue", "planet")
    py = Token(4 + NEW_X_COORD_LIST[5], 4 + NEW_X_COORD_LIST[5], "yellow", "planet")
    pg = Token(4 + NEW_X_COORD_LIST[5], 4 + NEW_X_COORD_LIST[9], "green", "planet")
    token_list.append(pr)
    token_list.append(pb)
    token_list.append(py)
    token_list.append(pg)

    # tr = Token(86, 212, "red", "triangle")
    # tb = Token(631, 760, "blue", "triangle")
    # ty = Token(393, 882, "yellow", "triangle")
    # tg = Token(870, 215, "green", "triangle")
    tr = Token(4 + NEW_X_COORD_LIST[1], 4 + NEW_X_COORD_LIST[3], "red", "triangle")
    tb = Token(4 + NEW_X_COORD_LIST[10], 4 + NEW_X_COORD_LIST[12], "blue", "triangle")
    ty = Token(4 + NEW_X_COORD_LIST[6], 4 + NEW_X_COORD_LIST[14], "yellow", "triangle")
    tg = Token(4 + NEW_X_COORD_LIST[14], 4 + NEW_X_COORD_LIST[3], "green", "triangle")
    token_list.append(tr)
    token_list.append(tb)
    token_list.append(ty)
    token_list.append(tg)

    # rb = Token(145, 517)
    rb = Token(4 + NEW_X_COORD_LIST[2], 4 + NEW_X_COORD_LIST[8])
    token_list.append(rb)

    return token_list
