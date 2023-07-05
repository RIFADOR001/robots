import pygame
import sys     # let  python use your file system
import numpy as np


pygame.init()
dimx=1000
dimy=1000
win = pygame.display.set_mode((dimx, dimy))


#FPS=60
FPS=120
#FPS=10
VEL=5
#With this variable we adjust the hitbox of walls so they are perfectly align
#and they are also aligh witn the hitbox to be added
CALIBRATION_X=7
CALIBRATION_Y=7


pygame.display.set_caption("First Game")
COORDS_FONT=pygame.font.SysFont('comicsans',40)

walkRight = [pygame.image.load('hero4.png')]
walkLeft = [pygame.image.load('hero4.png')]
bg = pygame.image.load('board.png')
char = pygame.image.load('hero4.png')

clock = pygame.time.Clock()


def cell(x,y):
    return (int(y/(1000/16)),int(x/(1000/16)))

def coord(i,j):
    l=58
    return (j*l+20,i*l+20)
    #return (j*(1000/16),i*(1000/16))

HW=np.zeros((17,17))
#Board matrix [right,up, left, down] limits for every position
bm=[[[(x,y),(x,y),(x,y),(x,y)]for y in range(16)] for x in range(16)]

#List of vertical walls, starting from top/left corner
VW_list=[(133,20),(560,20),(316,80),(682,80),
         (72,203),(926,203),
         (621,264), (316,325),
         (255,386),(743,386),(194,508),
         (316,569),(133,630),(682,630),
         (804,691),(314,752),(682,752),
         (804,813),(377,874),(255,935),(621,935)]

'''
HW_list=[(255,81),(682,81),(926,142),
         (865,203),(72,264),(316,325),(560,325),(14,386),(194,447),(743,447),
         (133,508),(316,630),(682,630),(72,691),(255,752),(621,752),(804,752),(926,752),
         (14,813),(377,874),(743,874)]
'''
HW_list=[(255,81),(682,81),(926,142),
         (865,203),(72,264),(316,325),(560,325),(14,386),(194,447),(743,447),
         (133,501),(316,623),(682,623),(72,684),(255,745),(621,745),(804,745),(926,745),
         (14,806),(377,867),(743,867)]

def walls():
    #First we fill the boundary
    for i in range(17):
        HW[0][i]=1
        HW[16][i] = 1
    #Center zone
    HW[7][7]=1
    HW[7][8] =1
    HW[9][7] =1
    HW[9][8] =1
    #Walls in the board
    HW[1][4]=1
    HW[1][11] =1
    HW[2][15] =1
    HW[3][14] =1
    HW[4][1] =1
    HW[5][5] =1
    HW[5][9] =1
    HW[6][0] =1
    HW[7][3] =1
    HW[7][12] =1
    HW[8][2] =1
    HW[10][5] =1
    HW[10][11] =1
    HW[11][1] =1
    HW[12][4] =1
    HW[12][10] =1
    HW[12][13] =1
    HW[12][15] =1
    HW[13][0] =1
    HW[14][6] =1
    HW[14][12] =1

#Function to create the list of rectangles that define the hitbox for the walls
def walls_hitbox(VW_list, HW_list):
    #List of hitbox
    HB=[]
    for vw in VW_list:
        hb=pygame.Rect(vw[0]-CALIBRATION_X,vw[1]+CALIBRATION_Y,14,40)
        HB.append(hb)
    for hw in HW_list:
        hb=pygame.Rect(hw[0]+CALIBRATION_X,hw[1]-CALIBRATION_Y,40,14)
        HB.append(hb)
    #Center block
    hb=pygame.Rect(438-CALIBRATION_X,447-CALIBRATION_Y,122+2*CALIBRATION_X,122+2*CALIBRATION_Y)
    HB.append(hb)
    #Boundary
    #hb = pygame.Rect(12, 20, 975, 975)
    #HB.append(hb)
    return HB

#dir is the direction of movement (right, up, left, down) from position i,j (dir is (1,0), (0,1), (-1,0) or (0,-1))
def limit(i, j, dir):
    if(dir=="up"):
        for k in range(16):
            if(HW[i-(k)][j]==1):
                return (i-k,j)
    if (dir == "down"):
        for k in range(16):
            if (HW[i+ (k + 1)][j ] == 1):
                return (i+ k, j )

#We need to know horizontal walls, vertical walls and robot's positions
def movementMatrix():
    for i in range(16):
        for j in range(16):
            bm[i][j][1]=limit(i,j,"up")
            #print(i,j,bm[i][j][1])
            bm[i][j][3]=limit(i,j,"down")
            #print(bm[i][j][3])




class player(object):
    #def __init__(self, x, y, width, height):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 49
        self.height = 48
        self.vel = VEL
        #self.vel = 20
        self.state="standing"
        self.isJump = False
        self.left = False
        self.right = False
        self.up=False
        self.down=False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        #self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.hitbox = (self.x + 49, self.y + 48, 49, 48)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.standing):
            win.blit(walkLeft[0], (self.x, self.y))
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        #self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.hitbox = (self.x , self.y , 49, 48)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)




class enemy(object):
    walkRight = [pygame.image.load('hero1.png')]
    walkLeft = [pygame.image.load('hero1.png')]

    #def __init__(self, x, y, width, height, end):
    def __init__(self, x, y, end):
        self.x = x
        self.y = y
        self.width = 49
        self.height = 48
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.hitbox = (self.x , self.y , 49, 48)

    def draw(self, win):

        #self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        l=49
        self.hitbox = (self.x , self.y , l, l)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)




def drawGameWindow(HB):
    win.blit(bg, (0, 0))
    man.draw(win)
    goblin.draw(win)

    coords_text = COORDS_FONT.render("Coords: " + str(coord_x) +","+str(coord_y), 1, (255, 0, 255))

    win.blit(coords_text, (10, 10))
    for w in HB:
        pygame.draw.rect(win,(255,0,0),w)

    pygame.display.update()


def handleMovement(keys):
    ind_r, ind_c = cell(man.x, man.y)

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.state = "left"
    elif keys[pygame.K_RIGHT] and man.x < dimx - man.width - man.vel:
        man.state = "right"
    # elif keys[pygame.K_DOWN] and man.y < dimy - man.height - man.vel:
    elif keys[pygame.K_DOWN] and limit(ind_r, ind_c, "down") != (ind_r, ind_c):
        man.state = "down"
    # elif keys[pygame.K_UP] and man.y > man.vel:
    elif keys[pygame.K_UP] and limit(ind_r, ind_c, "up") != (ind_r, ind_c):
        man.state = "up"

    if man.state == "left" and man.x > man.vel:
        man.x -= man.vel
    elif man.state == "right" and man.x < dimx - man.width - man.vel:
        man.x += man.vel
    # elif man.state == "down" and man.y < dimy - man.height - man.vel:
    elif man.state == "down" and man.y < coord(limit(ind_r, ind_c, "down")[0] + 1, limit(ind_r, ind_c, "down")[1])[
        1] - man.vel:
        man.y += man.vel
    # elif man.state == "up" and man.y > man.vel:
    # elif man.state == "up" and man.y>man.vel+man.height-coord(limit(ind_r, ind_c, "up")[0],limit(ind_r, ind_c, "up")[1])[1]:
    elif man.state == "up" and man.y > coord(limit(ind_r, ind_c, "up")[0], limit(ind_r, ind_c, "up")[1])[1] + man.vel:
        man.y -= man.vel
    else:
        man.state = "standing"
        man.standing = True
        man.walkCount = 0



walls()
movementMatrix()
HB=walls_hitbox(VW_list, HW_list)
#print(HW)
#for i in range(5):
#    print(bm[0][i])
# mainloop
man = player(200, 23)
goblin = enemy(100, 448, 450)
shootLoop = 0
run = True

#'''
while run:
    clock.tick(FPS)
    coord_x, coord_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        # Close the game if Q is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                run = False
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit()
            run = False





    keys = pygame.key.get_pressed()
    handleMovement(keys)
    drawGameWindow(HB)



pygame.quit()
#'''
