



pygame.init()


# This function creates the token list (the positions, images)
def create_tile_list():
    tile_list = []
    mr = Tile(695, 93, "red", "moon")
    mb = Tile(86, 635, "blue", "moon")
    my = Tile(753, 817, "yellow", "moon")
    mg = Tile(268, 93, "green", "moon")
    tile_list.append(mr)
    tile_list.append(mb)
    tile_list.append(my)
    tile_list.append(mg)

    sr = Tile(271, 759, "red", "star")
    sb = Tile(208, 394, "blue", "star")
    sy = Tile(753, 398, "yellow", "star")
    sg = Tile(694, 636, "green", "star")
    tile_list.append(sr)
    tile_list.append(sb)
    tile_list.append(sy)
    tile_list.append(sg)

    pr = Tile(819, 698, "red", "planet")
    pb = Tile(566, 268, "blue", "planet")
    py = Tile(329, 333, "yellow", "planet")
    pg = Tile(329, 572, "green", "planet")
    tile_list.append(pr)
    tile_list.append(pb)
    tile_list.append(py)
    tile_list.append(pg)

    tr = Tile(86, 212, "red", "triangle")
    tb = Tile(631, 760, "blue", "triangle")
    ty = Tile(393, 882, "yellow", "triangle")
    tg = Tile(870, 215, "green", "triangle")
    tile_list.append(tr)
    tile_list.append(tb)
    tile_list.append(ty)
    tile_list.append(tg)

    rb = Tile(145, 517)
    tile_list.append(rb)

    return tile_list

# This function initializes the pieces and buttons
def initialize_pieces_buttons(player_list=[]):
    pieces_list = []
    # black = Penguin(200, 23, "black")
    # pieces_list.append(black)
    # '''
    yellow = Penguin(377 + CALIBRATION_X, 874 + CALIBRATION_Y, "yellow")
    pieces_list.append(yellow)
    green = Penguin(865 + CALIBRATION_X, 203 + CALIBRATION_Y, "green")
    pieces_list.append(green)
    red = Penguin(926 + CALIBRATION_X, 325 + CALIBRATION_Y, "red")
    pieces_list.append(red)
    blue = Penguin(560 + CALIBRATION_X, 264 + CALIBRATION_Y, "blue")
    pieces_list.append(blue)
    for p in pieces_list:
        p.handle_hitbox()
    # '''

    button_list = []
    button_yellow = Button(1000, 50, 50, 50, "Piece", "yellow")
    button_yellow.piece = yellow
    button_list.append(button_yellow)
    button_red = Button(1050, 50, 50, 50, "Piece", "red")
    button_red.piece = red
    button_list.append(button_red)
    button_blue = Button(1000, 100, 50, 50, "Piece", "blue")
    button_blue.piece = blue
    button_list.append(button_blue)
    button_green = Button(1050, 100, 50, 50, "Piece", "green")
    button_green.piece = green
    button_list.append(button_green)
    '''
    if BLACK:
        button_black = Button(1000, 150, 50, 50, "Piece", "black")
        button_black.piece = black
        button_list.append(button_black)
    '''
    button_restart = Button(1000, 240, 50, 20, "Restart")
    button_list.append(button_restart)
    button_timer = Button(1000, 200, 50, 20, "Time")
    button_list.append(button_timer)
    button_rules = Button(1000, 180, 50, 20, "Rules")
    button_list.append(button_rules)
    button_settings = Button(1000, 220, 50, 20, "Settings")
    button_list.append(button_settings)

    button_back = Button(1050, 200, 50, 20, "Back")
    button_list.append(button_back)
    button_forward = Button(1100, 200, 50, 20, "Forward")
    button_list.append(button_forward)
    button_print = Button(1100, 250, 50, 20, "Print list")
    button_list.append(button_print)
    button_restart_position = Button(1100, 350, 100, 20, "Restart position")
    button_list.append(button_restart_position)

    aux = 1
    for p in player_list:
        but = Button(1000, 200 + aux * 20 + 50, 50, 20, "Player")
        but.player = p

        # but.draw(win)
        aux += 1
        button_list.append(but)

    return pieces_list, button_list


# This function creates a random list to show objectives every time a new one is needed
def create_random_list(n):
    aux = [i for i in range(n)]
    random_list = []
    for i in range(n):
        random_list.append(aux.pop(randrange(1000) % len(aux)))
    return random_list



# This is the main function
def main(player_list=[Player("Player 1")]):
    global SCORE
    global GOAL_REACHED
    global FIRST_MOVEMENT
    global TIMER
    global REAL_MOVEMENT
    global STEPS
    global POSITION_LIST
    global pieces_list
    global INDEX


    HB = walls_hitbox(VW_list, HW_list)
    tile_list = create_tile_list()
    random_list = create_random_list(len(tile_list))
    # print(len(random_list))
    # print(random_list)
    for p in player_list:
        p.score = 0


    aux = Tile(499 - 20, 508 - 20)
    objective_index = random_list[SCORE]
    aux.copy(tile_list[objective_index])
    objective = aux

    objective.x = 499 - 20
    objective.y = 508 - 20
    pieces_list, button_list = initialize_pieces_buttons(player_list)

    INDEX = -1
    POSITION_LIST = []
    updatePositionList(pieces_list)
    # mainloop

    FIRST_MOVEMENT = False
    remaining_seconds = 0
    steps = 0
    STEPS = 0

    run = True

    # '''
    while run:
        clock.tick(FPS)
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
                handle_clicks(coord_x, coord_y, button_list)
                # run = False
        for button in button_list:
            if button.pushed == True:
                keys = pygame.key.get_pressed()
                HB = update_HB(HB, pieces_list, button.piece)
                handleMovement(keys, HB, button.piece, tile_list, objective, pieces_list)
        if TIMER:
            FIRST_MOVEMENT = True
            if remaining_seconds == 0:
                start_time = int(time.time())
            TIMER = False

        if FIRST_MOVEMENT == False:
            remaining_seconds = 0
        else:
            # remaining_seconds = 15 - (int(time.time() -int(start_time)))
            # remaining_seconds = 60 - (int(time.time() - int(start_time)))
            remaining_seconds = HOURGLASS - (int(time.time() - int(start_time)))
            if remaining_seconds <= 0:
                remaining_seconds = 0
                TIMER = False


        if REAL_MOVEMENT:
            REAL_MOVEMENT = False
            STEPS += 1
            steps += 1
            # print("here01", steps)


        drawGameWindow(HB, tile_list, pieces_list, button_list,
                       coord_x, coord_y, objective, remaining_seconds, steps, player_list)
        # If the goal is reached, a new objective is generated
        try:
            if event.type == GOAL_REACHED:
                # SCORE += 1
                # HITBOX_SOUND.play()
                # print("goal reached")
                steps = 0
                STEPS = 0
                POSITION_LIST = []
                INDEX = -1
                updatePositionList(pieces_list)

                for p in player_list:
                    p.bid_status = False
                    p.bid = 0
                if SCORE < 5: # len(tile_list):
                    aux = Tile(499-20, 508-20)
                    objective_index = random_list[SCORE]
                    # print(objective_index)
                    # objective = tile_list[objective_index]
                    aux.copy(tile_list[objective_index])
                    objective = aux
                    objective.x = 499 - 20
                    objective.y = 508 - 20
                else:
                    GAME_OVER = True
                    draw_winer()
                    # main()
        except:
            pass


    pygame.quit()
    # '''

player1 = Player("Player 1")
player2 = Player("Player 2")
player_list = [player1, player2]


if __name__ == "__main__":
    # game_menu.game_start()
    main(player_list)
    # main(game_menu.players2())
    # main()