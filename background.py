import pygame
import os
import sys

dimx = 262*2
dimy = 262*2
win = pygame.display.set_mode((dimx, dimy))



# 262x262
bg1 = pygame.image.load(os.path.join('Assets', 'Iceboardquarter001.png'))
bg2 = pygame.transform.rotate(bg1,270)
bg3 = pygame.transform.rotate(bg2,270)
bg4 = pygame.transform.rotate(bg3,270)
bg_list = [bg1, bg2, bg3, bg4]
win.blit(bg1, (0, 0))
win.blit(bg2, (262, 0))
win.blit(bg3, (262, 262))
win.blit(bg4, (0, 262))

waiting = True
while waiting:
    for event in pygame.event.get():
        # Close the game if Q is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()

    pygame.display.update()


