from pieces_players_tokens import Player, Token, create_token_list
import pygame
from random import randrange
from board_geometry import walls_hitbox, vwall_list, hwall_list
import sys
import time
from game_information import GameInfo
# from graphics import main_win

pygame.init()
clock = pygame.time.Clock()

LEFT_SPACE = 300
# Size of the screen
dimx = 1000 + LEFT_SPACE
dimy = 1000
main_win = pygame.display.set_mode((dimx, dimy))
# This function creates the token list (the positions, images)
def create_tile_list():
    tile_list = []
    mr = Token(695, 93, "red", "moon")
    mb = Token(86, 635, "blue", "moon")
    my = Token(753, 817, "yellow", "moon")
    mg = Token(268, 93, "green", "moon")
    tile_list.append(mr)
    tile_list.append(mb)
    tile_list.append(my)
    tile_list.append(mg)

    sr = Token(271, 759, "red", "star")
    sb = Token(208, 394, "blue", "star")
    sy = Token(753, 398, "yellow", "star")
    sg = Token(694, 636, "green", "star")
    tile_list.append(sr)
    tile_list.append(sb)
    tile_list.append(sy)
    tile_list.append(sg)

    pr = Token(819, 698, "red", "planet")
    pb = Token(566, 268, "blue", "planet")
    py = Token(329, 333, "yellow", "planet")
    pg = Token(329, 572, "green", "planet")
    tile_list.append(pr)
    tile_list.append(pb)
    tile_list.append(py)
    tile_list.append(pg)

    tr = Token(86, 212, "red", "triangle")
    tb = Token(631, 760, "blue", "triangle")
    ty = Token(393, 882, "yellow", "triangle")
    tg = Token(870, 215, "green", "triangle")
    tile_list.append(tr)
    tile_list.append(tb)
    tile_list.append(ty)
    tile_list.append(tg)

    rb = Token(145, 517)
    tile_list.append(rb)

    return tile_list

# This function initializes the pieces and buttons


# This function creates a random list to show objectives every time a new one is needed
def create_random_list(n):
    aux = [i for i in range(n)]
    random_list = []
    for i in range(n):
        random_list.append(aux.pop(randrange(1000) % len(aux)))
    return random_list


# This is the main function
def main_function(game_info, win, player_list=None):
    if player_list is None:
        player_list = [Player("Player 1")]
    # HB = walls_hitbox(game_info.VW_list, game_info.HW_list)
    tile_list = create_tile_list()
    random_list = create_random_list(len(tile_list))
    # print(len(random_list))
    # print(random_list)
    for p in player_list:
        p.score = 0

    aux = Token(499 - 20, 508 - 20)
    objective_index = random_list[game_info.tokens]
    aux.copy(tile_list[objective_index])
    objective = aux

    objective.x = 499 - 20
    objective.y = 508 - 20
    # pieces_list, button_list = initialize_pieces_buttons(player_list)

    # INDEX = -1
    # POSITION_LIST = []
    # updatePositionList(pieces_list)
    # mainloop
    game_info.new_position_list()

    run = True
    start_time = 5000
    # '''
    while run:
        clock.tick(game_info.fps)
        coord_x, coord_y = pygame.mouse.get_pos()
        # An action may be done depending on the input from mouse and keyboard

        for event in pygame.event.get():
            # Close the game if Q is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    pygame.quit()
                    sys.exit()
                    # run = False
                # if event.key == ord('c'):
                #     game_menu.players2()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_info.buttons_lists.handle_clicks(coord_x, coord_y, game_info.movement)
                # run = False
        for pen_button in game_info.buttons_lists.penguin_button_list:
            if pen_button.pushed:
                keys = pygame.key.get_pressed()
                game_info.lists.update_hitbox(pen_button.penguin)
                pen_button.penguin.handle_movement(keys, game_info)
        if game_info.timer:
            game_info.first_movement_done = True
            if game_info.remaining_time == 0:
                start_time = int(time.time())
            game_info.timer = False

        if not game_info.first_movement_done:
            remaining_seconds = 0
            # game_info.remaining_time = 0
        else:
            # remaining_seconds = 15 - (int(time.time() -int(start_time)))
            # remaining_seconds = 60 - (int(time.time() - int(start_time)))
            remaining_seconds = game_info.hourglass - (int(time.time() - int(start_time)))
            if remaining_seconds <= 0:
                remaining_seconds = 0
                game_info.remaining_time = 0
                game_info.timer = False

        if game_info.real_movement:
            game_info.realmovement = False
            game_info.steps += 1
            # steps += 1
            # print("here01", steps)

        game_info.draw(win, coord_x, coord_y)
        # If the goal is reached, a new objective is generated
        try:
            if event.type == game_info.goal_reached:
                # SCORE += 1
                # HITBOX_SOUND.play()
                # print("goal reached")
                # steps = 0
                game_info.steps = 0
                game_info.new_position_list()
                game_info.lists.reset_bid()
                for p in player_list:
                    p.bid_status = False
                    p.bid = 0
                if game_info.score < 5:  # len(tile_list):
                    aux = Token(499-20, 508-20)
                    objective_index = random_list[game_info.score]
                    # print(objective_index)
                    # objective = tile_list[objective_index]
                    aux.copy(tile_list[objective_index])
                    objective = aux
                    objective.x = 499 - 20
                    objective.y = 508 - 20
                else:
                    game_over = True
                    # draw_winer()
                    # main()
        except:
            pass

    pygame.quit()
    # '''


player1 = Player("Player 1")
player2 = Player("Player 2")
play_list = [player1, player2]

hb_list = walls_hitbox(vwall_list, hwall_list)
t_list = create_token_list()
g_info = GameInfo(play_list, hb_list, t_list)
g_info.initialize_buttons()
g_info.new_random_list()
if __name__ == "__main__":
    # game_menu.game_start()
    main_function(g_info, main_win, play_list)
    # main(game_menu.players2())
    # main()
