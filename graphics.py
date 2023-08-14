import pygame
import os
import sys

dimx = 262*2
dimy = 262*2

pygame.font.init()
screen = pygame.display.set_mode((dimx, dimy))
screen1_x, screen1_y = 650, 400
screen1 = pygame.display.set_mode((screen1_x, screen1_y))
width, height = 140, 32
base_font = pygame.font.Font(None, 32)

clock = pygame.time.Clock()

blank = pygame.image.load(os.path.join('Assets', "Blank(650-400).png"))
input_rect = pygame.Rect((screen1_x-width)//2, (screen1_y-height)//2, width, height)
pygame.font.init()

# Space that exist in the right part of the board (with buttons and messages)
LEFT_SPACE = 300
# Color for the space
BLUE = (0, 155, 155)

# Size of the screen
# dimx = 1000 + LEFT_SPACE
# dimy = 1000
dimx = 262*2 + LEFT_SPACE
dimy = 262*2
main_win = pygame.display.set_mode((dimx, dimy))
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

'''
# This function indicates the winner
def draw_winer(text="GAME OVER"):
    draw_text = WINNER_FONT.render(text, True, (255, 255, 0))
    win.blit(draw_text, (1000//2-draw_text.get_width()//2, 1000//2-draw_text.get_height()//2))
    pygame.display.update()
    # The delay is computed as 1000* seconds
    pygame.time.delay(10000)
'''


# The function needs the name of the 4 quadrants to be used, then the board is created using them
def build_board(q1='Iceboardquarter001.png', q2='Iceboardquarter001.png',
                q3='Iceboardquarter001.png', q4='Iceboardquarter001.png'):

    # 262x262
    # bg1 = pygame.image.load(os.path.join('Assets', 'Iceboardquarter001.png'))
    # bg2 = pygame.transform.rotate(bg1,270)
    # bg3 = pygame.transform.rotate(bg2,270)
    # bg4 = pygame.transform.rotate(bg3,270)
    # bg1 = pygame.image.load(os.path.join('Assets', q1))
    # bg2 = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', q2)), 270)
    # bg3 = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', q3)), 180)
    # bg4 = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', q4)), 90)
    bg1 = pygame.image.load(os.path.join('Assets/Board', q2))
    bg2 = pygame.transform.rotate(pygame.image.load(os.path.join('Assets/Board', q1)), 270)
    bg3 = pygame.transform.rotate(pygame.image.load(os.path.join('Assets/Board', q4)), 180)
    bg4 = pygame.transform.rotate(pygame.image.load(os.path.join('Assets/Board', q3)), 90)
    bg_list = [bg1, bg2, bg3, bg4]
    return bg_list
    # win.blit(bg1, (0, 0))
    # win.blit(bg2, (262, 0))
    # win.blit(bg3, (262, 262))
    # win.blit(bg4, (0, 262))


def input_box(win, win_x=650, win_y=400, request="", explanation=""):
    # color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = pygame.Color('lightskyblue3')

    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = pygame.Color('chartreuse4')
    # color = color_passive

    active = False
    user_text = ''
    getting_text = True
    while getting_text:
        win.blit(blank, (0, 0))
        for event in pygame.event.get():
            # if user types QUIT then the screen will close
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    # print("enter")
                    # hitbox.main()
                    getting_text = False
                # Unicode standard is used for string
                # formation
                else:
                    user_text += event.unicode

        request_text = base_font.render(request, True, (0, 0, 0))
        win.blit(request_text, ((win_x-request_text.get_width())//2, (win_y-request_text.get_height())//2-height))
        explanation_text = base_font.render(explanation, True, (0, 0, 0))
        win.blit(explanation_text, ((win_x-explanation_text.get_width())//2,
                                    (win_y-explanation_text.get_height())//2+height))
        # screen1.blit(request_text, (width//2, height//2))
        if active:
            color = color_active
        else:
            color = color_passive
        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(win, color, input_rect)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        # render at position stated in arguments
        win.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width() + 10)
        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()
        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)
    return user_text.strip()


def graphics_main(win):
    waiting = True
    while waiting:
        bg_list = build_board("Q1.png", "Q2.png", "Q3.png", "Q4.png")
        win.blit(bg_list[0], (0, 0))
        win.blit(bg_list[1], (262, 0))
        win.blit(bg_list[2], (262, 262))
        win.blit(bg_list[3], (0, 262))
        for event in pygame.event.get():
            # Close the game if Q is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    graphics_main(screen1)
