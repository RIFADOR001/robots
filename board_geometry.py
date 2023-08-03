import pygame


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


def cell(x, y):
    # return (int(y/(1000/16)), int(x/(1000/16)))
    return int((x-11)/61), int((y-20)/61)


def coord(i, j):
    length = 58
    return j*length+20, i*length+20
    # return (j*(1000/16),i*(1000/16))


# List of vertical walls, starting from top/left corner
vwall_list = [(133, 20), (560, 20), (316, 81), (682, 81),
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
hwall_list = [(255, 81), (682, 81), (926, 142),
              (865, 203), (72, 264), (316, 325), (560, 325), (14, 386), (194, 447), (743, 447),
              (133, 508), (316, 630), (682, 630), (72, 691), (255, 752), (621, 752), (804, 752), (926, 752),
              (14, 813), (377, 874), (743, 874)]
# (133, 501), (316, 623), (682, 623), (72, 684), (255, 745), (621, 745), (804, 745), (926, 745),
#         (14, 806), (377, 867), (743, 867)]


# Function to create the list of rectangles that define the hitbox for the walls
def walls_hitbox(vw_list, hw_list):
    # List of hitbox
    hitbox_list = []
    for vw in vw_list:
        hb = pygame.Rect(vw[0]-CALIBRATION_X, vw[1]+CALIBRATION_Y, 14-2*EPSILON, 40)
        hitbox_list.append(hb)
    for hw in hw_list:
        hb = pygame.Rect(hw[0]+CALIBRATION_X, hw[1]-CALIBRATION_Y, 40, 14-2*EPSILON)
        hitbox_list.append(hb)
    # Center block
    hb = pygame.Rect(438-CALIBRATION_X, 447-CALIBRATION_Y, 122+2*CALIBRATION_X, 122+2*CALIBRATION_Y)
    hitbox_list.append(hb)
    # Board boundaries

    lw = pygame.Rect(5-CALIBRATION_X, 0-CALIBRATION_Y, 0+2*CALIBRATION_X, 1000+2*CALIBRATION_Y)
    hitbox_list.append(lw)
    uw = pygame.Rect(0-CALIBRATION_X, 10-CALIBRATION_Y, 1000+2*CALIBRATION_X, 0+2*CALIBRATION_Y)
    hitbox_list.append(uw)
    rw = pygame.Rect(1000 - 10 - CALIBRATION_X, 0 - CALIBRATION_Y, 0 + 2 * CALIBRATION_X, 1000 + 2 * CALIBRATION_Y)
    hitbox_list.append(rw)
    dw = pygame.Rect(0 - CALIBRATION_X, 1000 - 10 - CALIBRATION_Y, 1000 + 2 * CALIBRATION_X, 0 + 2 * CALIBRATION_Y)
    hitbox_list.append(dw)
    return hitbox_list
