import pygame
import sys     # let  python use your file system
import numpy as np
import os

pygame.font.init()
pygame.mixer.init()

LEFT_SPACE = 300
pygame.init()
dimx = 1000 + LEFT_SPACE
dimy = 1000
win = pygame.display.set_mode((dimx, dimy))

HITBOX_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hitbox.mp3'))


# FPS=60
FPS = 120
# FPS=10
VEL = 5
# With this variable we adjust the hitbox of walls, so they are perfectly align,
# and they are also aligh witn the hitbox to be added
EPSILON = 2
CALIBRATION_X = 7-EPSILON
CALIBRATION_Y = 7-EPSILON

X_COORD_LIST = [11, 72, 133, 194, 255, 316, 377, 438, 499, 560, 621, 682, 743, 804, 865, 926, 987]
Y_COORD_LIST = [20, 81, 142, 203, 264, 325, 386, 447, 508, 569, 630, 691, 752, 813, 874, 935, 996]

pygame.display.set_caption("First Game")
COORDS_FONT = pygame.font.SysFont('comicsans', 40)
TEXT_FONT = pygame.font.SysFont('comicsans', 20)

BLACK_PIECE = pygame.image.load(os.path.join('Assets', 'heroblack.png'))
bg = pygame.image.load(os.path.join('Assets', 'board.png'))

clock = pygame.time.Clock()


def cell(x, y):
    # return (int(y/(1000/16)), int(x/(1000/16)))
    return int((x-11)/61), int((y-20)/61)


def coord(i, j):
    l = 58
    return (j*l+20, i*l+20)
    # return (j*(1000/16),i*(1000/16))


HW = np.zeros((17, 17))
# Board matrix [right,up, left, down] limits for every position
bm = [[[(x, y), (x, y), (x, y), (x, y)]for y in range(16)] for x in range(16)]

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


def walls():
    # First we fill the boundary
    for i in range(17):
        HW[0][i] = 1
        HW[16][i] = 1
    # Center zone
    HW[7][7] = 1
    HW[7][8] = 1
    HW[9][7] = 1
    HW[9][8] = 1
    # Walls in the board
    HW[1][4] = 1
    HW[1][11] = 1
    HW[2][15] = 1
    HW[3][14] = 1
    HW[4][1] = 1
    HW[5][5] = 1
    HW[5][9] = 1
    HW[6][0] = 1
    HW[7][3] = 1
    HW[7][12] = 1
    HW[8][2] = 1
    HW[10][5] = 1
    HW[10][11] = 1
    HW[11][1] = 1
    HW[12][4] = 1
    HW[12][10] = 1
    HW[12][13] = 1
    HW[12][15] = 1
    HW[13][0] = 1
    HW[14][6] = 1
    HW[14][12] = 1


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


# dir is the direction of movement (right, up, left, down) from position i,j (dir is (1,0), (0,1), (-1,0) or (0,-1))
def limit(i, j, dir):
    if(dir == "up"):
        for k in range(16):
            if(HW[i-(k)][j] == 1):
                return (i-k, j)
    if (dir == "down"):
        for k in range(16):
            if (HW[i + (k + 1)][j] == 1):
                return (i + k, j)


# We need to know horizontal walls, vertical walls and robot's positions
def movementMatrix():
    for i in range(16):
        for j in range(16):
            bm[i][j][1] = limit(i, j, "up")
            # print(i,j,bm[i][j][1])
            bm[i][j][3] = limit(i, j, "down")
            # print(bm[i][j][3])


class Penguin(object):
    # def __init__(self, x, y, width, height):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
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


    def handle_hitbox(self):

        self.old_cell_x = self.cell_x
        self.old_cell_y = self.cell_y
        self.cell_x, self.cell_y = cell(self.x, self.y)

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


    def draw(self, win):
        # win.blit(BLACK_PIECE, (self.x, self.y))
        win.blit(self.image, (self.x, self.y))

        # self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.hitbox = (self.x, self.y, 49, 48)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


class Button(object):
    # We specify the location, size and function of the button (character, timer, go back, etc)
    def __init__(self, x, y, width, height, function, color=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.function = function
        self.color = color
        if function == "piece":
            self.pushed = False
            if color == "red":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'herored.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                self.piece = red
            if color == "yellow":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'heroyellow.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                self.piece = yellow
            if color == "blue":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'heroblue.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                self.piece = blue
            if color == "green":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'herogreen.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                self.piece = green
            if color == "black":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'heroblack.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                self.piece = black

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    # The activate function will depend on the pressed button
    def activate(self):
        pass

        # self.hitbox = (self.x, self.y, 49, 48)


def drawGameWindow(HB):
    win.fill((0, 155, 155))
    win.blit(bg, (0, 0))
    for piece in pieces_list:
        piece.draw(win)

    aux=0
    for button in button_list:
        button_info = TEXT_FONT.render("Pushed " + button.color + " button? " + str(button.pushed), True, (255, 255, 0))
        button.draw(win)
        win.blit(button_info, (1000, 200 + aux*20))
        aux+=1


    pieces_text = TEXT_FONT.render("Select your piece", True, (255, 255, 0))
    coords_text = COORDS_FONT.render("Coords: " + str(coord_x) + "," + str(coord_y), True, (255, 0, 255))

    win.blit(coords_text, (10, 10))
    win.blit(pieces_text, (1000, 20))
    for w in HB:
        pygame.draw.rect(win,(255,0,0),w)

    pygame.display.update()

# We verify if a button was pushed. If it is a piece, the other pieces should deactivate and the pushed
# piece should become active. This is the piece that we will move.
def handle_clicks(x,y):
    for button in button_list:
        if button.x < x and x < button.x + button.width and button.y < y and y < button.y + button.height:
            if button.function == "piece":
                for but in button_list:
                    if but.function == "piece":
                        but.pushed = False
                        but.image = but.image_nonactive
                button.pushed = True
                button.image = button.image_active
            else:
                button.activate()
        elif button.function == "piece":
            if button.piece.x < x and x < button.piece.x + button.piece.width and button.piece.y < y and y < button.piece.y + button.piece.height:
                for but in button_list:
                    if but.function == "piece":
                        but.pushed = False
                        but.image = but.image_nonactive
                button.pushed = True
                button.image = button.image_active


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
def handleMovement(keys, HB, piece):
    ind_r, ind_c = cell(piece.x, piece.y)

    if keys[pygame.K_LEFT] and piece.state == "standing":
        piece.state = "left"
    elif keys[pygame.K_RIGHT] and piece.state == "standing":
        piece.state = "right"
    elif keys[pygame.K_DOWN] and piece.state == "standing":
        piece.state = "down"
    elif keys[pygame.K_UP] and piece.state == "standing":
        piece.state = "up"

    HB = hit_wall(HB, piece.state, piece)
    if piece.state == "left" and piece.x > piece.vel:
        piece.x -= piece.vel
        # piece.image = pygame.image.load("heroblackleft.png")
    elif piece.state == "right" and piece.x < dimx - piece.width - piece.vel - LEFT_SPACE:
        piece.x += piece.vel
        # piece.image = pygame.image.load("heroblackright.png")
    # elif piece.state == "down" and piece.y < coord(limit(ind_r, ind_c, "down")[0] + 1, limit(ind_r, ind_c, "down")[1])[
      #  1] - piece.vel:
    elif piece.state == "down" and piece.y < dimy - piece.height - piece.vel:
        piece.y += piece.vel
        # piece.image = pygame.image.load("heroblackdown.png")
    # elif piece.state == "up" and piece.y > coord(limit(ind_r, ind_c, "up")[0], limit(ind_r, ind_c, "up")[1])[1] + piece.vel:
    elif piece.state == "up" and piece.y > piece.vel:
        piece.y -= piece.vel
        # piece.image = pygame.image.load("heroblackup.png")
    else:
        piece.state = "standing"
        piece.standing = True

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



walls()
movementMatrix()
HB = walls_hitbox(VW_list, HW_list)


# mainloop
pieces_list = []
black = Penguin(200, 23, "black")
pieces_list.append(black)
# '''
yellow=Penguin(377+CALIBRATION_X,874+CALIBRATION_Y, "yellow")
pieces_list.append(yellow)
green=Penguin(865+CALIBRATION_X,203+CALIBRATION_Y, "green")
pieces_list.append(green)
red=Penguin(926+CALIBRATION_X,325+CALIBRATION_Y, "red")
pieces_list.append(red)
blue=Penguin(560+CALIBRATION_X,264+CALIBRATION_Y, "blue")
pieces_list.append(blue)
for p in pieces_list:
    p.handle_hitbox()
# '''

button_list = []
button_yellow = Button(1000, 50, 50, 50, "piece", "yellow")
button_list.append(button_yellow)
button_red = Button(1050, 50, 50, 50, "piece", "red")
button_list.append(button_red)
button_blue = Button(1000, 100, 50, 50, "piece", "blue")
button_list.append(button_blue)
button_green = Button(1050, 100, 50, 50, "piece", "green")
button_list.append(button_green)
button_black = Button(1000, 150, 50, 50, "piece", "black")
button_list.append(button_black)
run = True

# '''
while run:
    clock.tick(FPS)
    coord_x, coord_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        # Close the game if Q is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                # run = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_clicks(coord_x, coord_y)
            # run = False
    for button in button_list:
        if button.pushed == True:
            keys = pygame.key.get_pressed()
            HB = update_HB(HB,pieces_list, button.piece)
            handleMovement(keys, HB, button.piece)
    drawGameWindow(HB)

pygame.quit()
# '''
