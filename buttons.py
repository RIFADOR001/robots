# Class of buttons. Buttons are used to select pieces to move, set timer, go back some steps, restart the game
class Button(object):
    # We specify the location, size and function of the button (character, timer, go back, etc)
    # The constructor needs to know the position, size, function of button and color (assuming it is linked to a piece)
    def __init__(self, x, y, width, height, function, color=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.function = function
        self.pushed = False
        # self.player = ""
        self.score = 0
        if function == "Piece":

            self.color = color
            self.piece = Penguin(0, 0, "blue")
            # Depending on the color of the piece, the image is selected
            if color == "red":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'herored.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                #self.piece = red
            if color == "yellow":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'heroyellow.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                #self.piece = yellow
            if color == "blue":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'heroblue.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                #self.piece = blue
            if color == "green":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'herogreen.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                #self.piece = green
            if color == "black":
                self.image_nonactive = pygame.image.load(os.path.join('Assets', 'heroblack.png'))
                self.image = self.image_nonactive
                self.image_active = pygame.image.load(os.path.join('Assets', color + '_active.png'))
                #self.piece = black
        # If this is not a piece button, then we check its function
        elif self.function == "Restart position":
            self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Blank.png')), (100, 20))
        else:
            self.image = pygame.image.load(os.path.join('Assets', 'Blank.png'))

    def draw(self, win):
        # TEXT_FONT = pygame.font.SysFont('comicsans', 20)

        win.blit(self.image, (self.x, self.y))
        if self.function == "Piece":
            pass
        elif self.function == "Player":
            name_info = TEXT_FONT1.render(self.player.name, True, (0, 0, 0))
            if self.player.bid_status:
                score_info = TEXT_FONT1.render(f"Score: {self.player.score}  Bid: {self.player.bid}", True, (0, 0, 0))
            else:
                score_info = TEXT_FONT1.render(f"Score: {self.player.score}", True, (0, 0, 0))
            win.blit(name_info, (self.x, self.y))
            win.blit(score_info, (self.x + BUTTON_LENGTH + 5, self.y))
        else:
            button_info = TEXT_FONT1.render(self.function, True, (0, 0, 0))
            win.blit(button_info, (self.x, self.y))


    # The activate function will depend on the pressed button
    def activate(self):
        global SCORE
        global TIMER
        global ACTIVE_PLAYER
        global PLAYER_NOT_SELECTED
        global HOURGLASS
        global INDEX
        global STEPS
        if self.function == "Restart":
            SCORE = 0
            main(player_list)
        if self.function == "Time":
            TIMER = True
        if self.function == "Start yes":
            self.pushed = True
        if self.function == "Start no":
            self.pushed = True
        if self.function == "Player":
            # print(self.player.name)
            ACTIVE_PLAYER = self.player
            TIMER = True
            PLAYER_NOT_SELECTED = False
            self.player.bid = game_menu.bid(self.player.bid_status, self.player.name, self.player.bid)
            self.player.bid_status = True
            # game_menu.inputBox("")
        if self.function == "Rules":
            path = os.path.join('Assets','rules.pdf')
            os.system("open " + path)
            #os.system("open Assets/rules.pdf")
        if self.function == "Settings":
            HOURGLASS = game_menu.adjustTime()
        if self.function == "Back":
            n = len(POSITION_LIST)
            if INDEX > 0:
                STEPS -= 2
                INDEX -= 1
                aux = 0
                for p in pieces_list:
                    p.x = POSITION_LIST[INDEX][aux][0]
                    p.y = POSITION_LIST[INDEX][aux][1]
                    aux +=1
            print("Back")
        if self.function == "Forward":
            print("Forward")
            n = len(POSITION_LIST)
            if INDEX < n-1:
                INDEX += 1
                aux = 0
                for p in pieces_list:
                    p.x = POSITION_LIST[INDEX][aux][0]
                    p.y = POSITION_LIST[INDEX][aux][1]
                    aux +=1

        if self.function == "Print list":
            print(POSITION_LIST)
        if self.function == "Restart position":
            INDEX = -1
            aux = 0
            for p in pieces_list:
                p.x = POSITION_LIST[0][aux][0]
                p.y = POSITION_LIST[0][aux][1]
                aux += 1
