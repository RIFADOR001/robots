import pygame


# Space that exist in the right part of the board (with buttons and messages)
LEFT_SPACE = 300
# Color for the space
BLUE = (0, 155, 155)

dimx = 1000 + LEFT_SPACE
dimy = 1000

BUTTON_LENGTH = 50

WINNER_FONT = pygame.font.SysFont('comicsans', 100)

SHOW_HITBOX = True

FPS=60
# FPS = 120
# FPS=10

EPSILON = 2
CALIBRATION_X = 7-EPSILON
CALIBRATION_Y = 7-EPSILON

# Lists of coordinates of the edges of the board
X_COORD_LIST = [11, 72, 133, 194, 255, 316, 377, 438, 499, 560, 621, 682, 743, 804, 865, 926, 987]
Y_COORD_LIST = [20, 81, 142, 203, 264, 325, 386, 447, 508, 569, 630, 691, 752, 813, 874, 935, 996]

pygame.display.set_caption("First Game")

COORDS_FONT = pygame.font.SysFont('comicsans', 40)
TEXT_FONT = pygame.font.SysFont('comicsans', 20)
TEXT_FONT1 = pygame.font.SysFont('comicsans', 12)