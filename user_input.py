

width, height = 140, 32
input_rect = pygame.Rect((screen1_x-width)//2, (screen1_y-height)//2, width, height)

# color_active stores color(lightskyblue3) which
# gets active when input box is clicked by user
color_active = pygame.Color('lightskyblue3')

# color_passive store color(chartreuse4) which is
# color of input box.
color_passive = pygame.Color('chartreuse4')
color = color_passive

active = False





# We verify if a button was pushed. If it is a piece, the other pieces should deactivate and the pushed
# piece should become active. This is the piece that we will move.
def handle_clicks(x,y, button_list):
    for button in button_list:
        if button.x < x and x < button.x + button.width and button.y < y and y < button.y + button.height:
            if button.function == "Piece" and MOVEMENT == False:
                for but in button_list:
                    if but.function == "Piece":
                        but.pushed = False
                        but.image = but.image_nonactive
                button.pushed = True
                button.image = button.image_active
            else:
                button.activate()
        elif button.function == "Piece" and MOVEMENT == False:
            if button.piece.x < x and x < button.piece.x + button.piece.width and button.piece.y < y and y < button.piece.y + button.piece.height:
                for but in button_list:
                    if but.function == "Piece":
                        but.pushed = False
                        but.image = but.image_nonactive
                button.pushed = True
                button.image = button.image_active




def userInput():
    global active
    user_text = ''
    getting_text = True
    while getting_text:

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

        # it will set background color of screen
        screen.fill((255, 255, 255))

        if active:
            color = color_active
        else:
            color = color_passive

        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(screen, color, input_rect)

        text_surface = base_font.render(user_text, True, (255, 255, 255))

        # render at position stated in arguments
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width() + 10)

        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()

        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)
    return user_text

def inputBox(request="", explanation=""):
    global active
    user_text = ''
    getting_text = True
    while getting_text:
        screen.blit(blank, (0, 0))
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

        # it will set background color of screen
        # screen1.fill((255, 255, 255))
        # steps_info = base_font.render(request, True, (235, 235, 0))
        request_text = base_font.render(request, True, (0, 0, 0))
        screen1.blit(request_text, ((screen1_x-request_text.get_width())//2, (screen1_y-request_text.get_height())//2-height))
        explanation_text = base_font.render(explanation, True, (0, 0, 0))
        screen1.blit(explanation_text, ((screen1_x-explanation_text.get_width())//2, (screen1_y-explanation_text.get_height())//2+height))
        # screen1.blit(request_text, (width//2, height//2))
        # WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
        # input_rect = pygame.Rect((screen1_x - width) // 2, (screen1_y - height) // 2, width, height)
        if active:
            color = color_active
        else:
            color = color_passive

        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(screen1, color, input_rect)

        text_surface = base_font.render(user_text, True, (255, 255, 255))

        # render at position stated in arguments
        screen1.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

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



def adjustTime():
    req1 = "Please enter the time in seconds (between 5 and 300): "
    req2 = "Please enter a valid time in seconds (between 5 and 300): "
    waiting_valid_number = True
    while waiting_valid_number:
        number = inputBox(req1)
        try:
            s = int(number)
            if s > 4 and s < 301:
                waiting_valid_number = False

        except:
            req1 = req2
    return s

def players2():
    # print("Enter number of players: ")
    req1 = "Enter number of players: "
    req2 = "Please enter a valid number of players: "
    waiting_valid_number = True
    while waiting_valid_number:
        number = inputBox(req1)
        try:
            n = int(number)
            if n > 0:
                waiting_valid_number = False
            # else:
            #    print()
        except:
            req1 = req2
            # print("Please enter a valid number of players: ")
    # return n
    # print("Do you want to name the players? Y or N")
    waiting_valid_input = True
    answer = ""
    req1 = "Do you want to name the players? Y or N"
    req2 = "Do you want to name the players? Please answer Y or N"
    reqname1 = "Name the player number "
    reqname2 = "Place write a valid name for player number "
    while waiting_valid_input:

        answer = inputBox(req1)
        if answer != "Y" and answer != "y" and answer != "N" and answer != "n":
            req1 = req2
        else:
            waiting_valid_input = False
    names_list = []
    if answer == "N" or answer == "n":
        for i in range(n):
            names_list.append(hitbox.Player("Player " + str(i+1)))
        return names_list
    else:
        for i in range(n):
            waiting_valid_name = True
            # print("Name the player number ", i+1)
            while waiting_valid_name:
                name = inputBox(reqname1 + str(i+1))
                if name == "":
                    reqname1 = reqname2
                else:
                    waiting_valid_name = False
            names_list.append(hitbox.Player(name))

    return names_list


def screen_players(coord_x, coord_y):
    screen.fill(BLUE)
    waiting = True
    while waiting:
        steps_info = base_font.render("What is the number of players?", True, (235, 235, 0))
        screen.blit(steps_info, (200, 170))
        coord_x, coord_y = pygame.mouse.get_pos()


        pygame.display.update()
    user_text = userInput()
    print(user_text)




    pygame.display.update()

