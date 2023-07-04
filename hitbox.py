import pygame
import sys     # let  python use your file system
import numpy as np


pygame.init()
dimx=1000
dimy=1000
win = pygame.display.set_mode((dimx, dimy))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('hero4.png'), pygame.image.load('hero4.png'), pygame.image.load('hero4.png'),
             pygame.image.load('hero4.png'), pygame.image.load('hero4.png'), pygame.image.load('hero4.png'),
             pygame.image.load('hero4.png'), pygame.image.load('hero4.png'), pygame.image.load('hero4.png')]
walkLeft = [pygame.image.load('hero4.png'), pygame.image.load('hero4.png'), pygame.image.load('hero4.png'),
             pygame.image.load('hero4.png'), pygame.image.load('hero4.png'), pygame.image.load('hero4.png'),
             pygame.image.load('hero4.png'), pygame.image.load('hero4.png'), pygame.image.load('hero4.png')]
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
        self.vel = 5
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
            #win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
            #if self.left:
            #    win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
            #    self.walkCount += 1
            #elif self.right:
            #    win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
            #    self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        #self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.hitbox = (self.x , self.y , 49, 48)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


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
        self.vel = 3
        #self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.hitbox = (self.x , self.y , 49, 48)

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.walkRight[0], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[0], (self.x, self.y))
            self.walkCount += 1
        #self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        l=49
        self.hitbox = (self.x , self.y , l, l)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        print('hit')


def redrawGameWindow():
    win.blit(bg, (0, 0))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


walls()
movementMatrix()
#print(HW)
#for i in range(5):
#    print(bm[0][i])
# mainloop
man = player(200, 23)
goblin = enemy(100, 448, 450)
shootLoop = 0
bullets = []
run = True

#'''
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                run = False
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit()
            run = False

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[
            1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + \
                    goblin.hitbox[2]:
                goblin.hit()
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    ind_r, ind_c=cell(man.x,man.y)
    print(ind_r,ind_c)

    if keys[pygame.K_DOWN] and limit(ind_r, ind_c, "down") == (ind_r, ind_c):
        print("here")

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.state="left"
    elif keys[pygame.K_RIGHT] and man.x < dimx - man.width - man.vel:
        man.state = "right"
    #elif keys[pygame.K_DOWN] and man.y < dimy - man.height - man.vel:
    elif keys[pygame.K_DOWN] and limit(ind_r,ind_c,"down")!= (ind_r, ind_c):
        man.state = "down"
    #elif keys[pygame.K_UP] and man.y > man.vel:
    elif keys[pygame.K_UP] and limit(ind_r, ind_c, "up") != (ind_r, ind_c):
        man.state = "up"


    if man.state == "left" and man.x > man.vel:
        man.x -= man.vel
    elif man.state == "right" and man.x < dimx - man.width - man.vel:
        man.x += man.vel
    #elif man.state == "down" and man.y < dimy - man.height - man.vel:
    elif man.state == "down" and man.y<coord(limit(ind_r, ind_c, "down")[0]+1,limit(ind_r, ind_c, "down")[1])[1]-man.vel:
        man.y += man.vel
    #elif man.state == "up" and man.y > man.vel:
    #elif man.state == "up" and man.y>man.vel+man.height-coord(limit(ind_r, ind_c, "up")[0],limit(ind_r, ind_c, "up")[1])[1]:
    elif man.state == "up" and man.y > coord(limit(ind_r, ind_c, "up")[0], limit(ind_r, ind_c, "up")[1])[1]+man.vel :
        man.y -= man.vel
    else:
        man.state="standing"
        man.standing = True
        man.walkCount = 0
    redrawGameWindow()



pygame.quit()
#'''

'''
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                run = False
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit()
            run = False

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[
            1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + \
                    goblin.hitbox[2]:
                goblin.hit()
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()



    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.down = False
        man.up = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < dimx - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.down = False
        man.up = False
        man.standing = False
    elif keys[pygame.K_DOWN] and man.y < dimy - man.height - man.vel:
        man.y += man.vel
        man.right = False
        man.left = False
        man.down = True
        man.up = False
        man.standing = False
    elif keys[pygame.K_UP] and man.y > man.vel:
        man.y -= man.vel
        man.right = False
        man.left = False
        man.down = False
        man.up = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    redrawGameWindow()



pygame.quit()

#jun 21 11:41

    if keys[pygame.K_LEFT] and man.x > man.vel:
        #print("left")
        #man.left = True
        #man.right = False
        #man.down = False
        #man.up = False
        #man.standing = False
        man.state="left"
    elif keys[pygame.K_RIGHT] and man.x < dimx - man.width - man.vel:
        #print("right")
        #man.right = True
        #man.left = False
        #man.down = False
        #man.up = False
        #man.standing = False
        man.state = "right"
    elif keys[pygame.K_DOWN] and man.y < dimy - man.height - man.vel:
        #print("down")
        #man.right = False
        #man.left = False
        #man.down = True
        #man.up = False
        #man.standing = False
        man.state = "down"
    elif keys[pygame.K_UP] and man.y > man.vel:
        #print("up")
        #man.right = False
        #man.left = False
        #man.down = False
        #man.up = True
        #man.standing = False
        man.state = "up"
    #print(man.standing)


    #if keys[pygame.K_LEFT] and man.x > man.vel:
    #if man.left==True and man.x > man.vel:
    if man.state == "left" and man.x > man.vel:
        man.x -= man.vel
        #man.left = True
        #man.right = False
        #man.down = False
        #man.up = False
        #man.standing = False
    #elif man.right==True and man.x < dimx - man.width - man.vel:
    elif man.state == "right" and man.x < dimx - man.width - man.vel:
        man.x += man.vel
        #man.right = True
        #man.left = False
        #man.down = False
        #man.up = False
        #man.standing = False
    #elif man.down==True and man.y < dimy - man.height - man.vel:
    elif man.state == "down" and man.y < dimy - man.height - man.vel:
        man.y += man.vel
        #man.right = False
        #man.left = False
        #man.down = True
        #man.up = False
        #man.standing = False
    #elif man.up==True and man.y > man.vel:
    elif man.state == "up" and man.y > man.vel:
        man.y -= man.vel
        #man.right = False
        #man.left = False
        #man.down = False
        #man.up = True
        #man.standing = False
    else:
        man.state="standing"
        man.standing = True
        man.walkCount = 0
    redrawGameWindow()


'''