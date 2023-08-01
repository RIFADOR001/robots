import pygame
import os
from game_info import GameInfo




dimx = 262*2
dimy = 262*2
win2 = pygame.display.set_mode((dimx, dimy))




pygame.font.init()

# Space that exist in the right part of the board (with buttons and messages)
LEFT_SPACE = 300
# Color for the space
BLUE = (0, 155, 155)

# Size of the screen
dimx = 1000 + LEFT_SPACE
dimy = 1000
win = pygame.display.set_mode((dimx, dimy))
SHOW_HITBOX = True


# FPS=60
FPS = 120
# FPS=10


# Name of the game
pygame.display.set_caption("First Game")


COORDS_FONT = pygame.font.SysFont('comicsans', 40)
TEXT_FONT = pygame.font.SysFont('comicsans', 20)
TEXT_FONT1 = pygame.font.SysFont('comicsans', 12)


# Board image
bg = pygame.image.load(os.path.join('Assets', 'board.png'))

# This function draws the board, pieces, score and everything displayed in screen
# def drawGameWindow(HB, tile_list, pieces_list, button_list, coord_x, coord_y, objective, remaining_seconds, steps, player_list):
def drawGameWindow(game_info, coord_x, coord_y):
    win.fill(BLUE)
    win.blit(bg, (0, 0))
    if SHOW_HITBOX:
        for hb in game_info.lists.hitbox_list:
            pygame.draw.rect(win, (255, 0, 0), hb)
    for t in game_info.token_list:
        t.draw(win)
    for piece in pieces_list:
        piece.draw(win)
    objective.draw(win)
    # steps = 0
    steps_info = TEXT_FONT.render(f"Number of steps: {game_info.steps}", True, (255, 255, 0))
    # win.blit(steps_info, (1000, 220))
    aux = 10
    for button in button_list:
        # if button.function == "Piece":
        #    button_info = TEXT_FONT.render("Pushed " + button.color + " button? " + str(button.pushed), True, (255, 255, 0))

            # win.blit(button_info, (1000, 200 + aux*20))
            # aux += 1
        button.draw(win)

    # '''
    score_info = TEXT_FONT.render(f"Tokens obtained: {SCORE}", True, (255, 255, 0))
    win.blit(score_info, (1000, 200 + aux * 20))
    steps_info = TEXT_FONT.render(f"GLOBAL Steps: {STEPS}", True, (255, 255, 0))
    win.blit(steps_info, (1000, 200 + (aux + 1) * 20))
    time_info = TEXT_FONT.render(f"Time: {remaining_seconds}", True, (255, 255, 0))
    win.blit(time_info, (1000, 200 + (aux + 2) * 20))
    timer_info = TEXT_FONT.render(f"Time: {TIMER}", True, (255, 255, 0))
    win.blit(timer_info, (1000, 200 + (aux + 3) * 20))
    steps01_info = TEXT_FONT.render(f"Steps: {steps}", True, (255, 255, 0))
    win.blit(steps01_info, (1000, 200 + (aux + 4) * 20))
    steps01_info = TEXT_FONT.render(f"Active player: {ACTIVE_PLAYER.name}", True, (255, 255, 0))
    win.blit(steps01_info, (1000, 200 + (aux + 5) * 20))
    waiting_info = TEXT_FONT.render(f"Waiting time: {HOURGLASS}", True, (255, 255, 0))
    win.blit(waiting_info, (1000, 200 + (aux + 6) * 20))
    INDEX_info = TEXT_FONT.render(f"INDEX: {INDEX}", True, (255, 255, 0))
    win.blit(INDEX_info, (1000, 200 + (aux + 7) * 20))
    # '''
    pieces_text = TEXT_FONT.render("Select your penguin", True, (255, 255, 0))
    coords_text = COORDS_FONT.render(f"Coords:  {coord_x}, {coord_y}", True, (255, 0, 255))


    '''
    for p in player_list:
        but = Button(1000, 200 + aux*20 +50, 50, 20, "Player")
        but.player = p.name
        but.draw(win)
        aux += 1
    #'''
    # win.blit(coords_text, (10, 10))
    win.blit(pieces_text, (1000, 20))
    if PLAYER_NOT_SELECTED:
        unselected_text = TEXT_FONT.render("Select a player before moving", True, (255, 255, 0))
        win.blit(unselected_text, (1000, 200 ))


    pygame.display.update()


# This function indicates the winner
def draw_winer(text="GAME OVER"):
    draw_text = WINNER_FONT.render(text, True, (255, 255, 0))
    win.blit(draw_text, (1000//2-draw_text.get_width()//2, 1000//2-draw_text.get_height()//2))
    pygame.display.update()
    # The delay is computed as 1000* seconds
    pygame.time.delay(10000)


# The function needs the name of the 4 quadrants to be used, then the board is created using them
def buildBoard(Q1='Iceboardquarter001.png', Q2='Iceboardquarter001.png', Q3='Iceboardquarter001.png', Q4='Iceboardquarter001.png'):

    # 262x262
    # bg1 = pygame.image.load(os.path.join('Assets', 'Iceboardquarter001.png'))
    # bg2 = pygame.transform.rotate(bg1,270)
    # bg3 = pygame.transform.rotate(bg2,270)
    # bg4 = pygame.transform.rotate(bg3,270)
    bg1 = pygame.image.load(os.path.join('Assets', Q1))
    bg2 = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', Q2)), 270)
    bg3 = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', Q3)), 180)
    bg4 = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', Q4)), 90)
    bg_list = [bg1, bg2, bg3, bg4]
    return bg_list
    # win.blit(bg1, (0, 0))
    # win.blit(bg2, (262, 0))
    # win.blit(bg3, (262, 262))
    # win.blit(bg4, (0, 262))


if __name__=="__main__":
    waiting = True
    while waiting:
        bg_list = buildBoard()
        win2.blit(bg_list[0], (0, 0))
        win2.blit(bg_list[1], (262, 0))
        win2.blit(bg_list[2], (262, 262))
        win2.blit(bg_list[3], (0, 262))
        for event in pygame.event.get():
            # Close the game if Q is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()






