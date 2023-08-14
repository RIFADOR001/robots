from pieces_players_tokens import ListsPenguinPlayersHitbox, Player, Token
from graphics import BLUE, bg, SHOW_HITBOX, build_board
from game_config import*
from buttons import PenguinButton, PlayerButton, FunctionalityButton, MovementButton, ButtonLists
from random import randrange


class GameInfo(object):
    def __init__(self, players_list, hitbox_list, token_list, initial_positions=None):
        self.buttons_lists = None
        self.position_list = None  # [[(p.x, p.y) for p in players_list]]
        self.index = 0
        self.tokens = 0
        self.movement = False
        self.goal_reached = False
        self.timer = False
        self.hourglass = False
        self.moved_cell = False
        self.real_movement = False
        self.first_movement_done = False
        self.max_time = 30
        self.steps = 0
        self.player_not_selected = True
        self.active_player = self.aux_player = Player("None")

        self.random_list = None
        self.objective = None
        self.remaining_time = 0
        self.lists = ListsPenguinPlayersHitbox(players_list, hitbox_list, initial_positions)
        self.token_list = token_list
        self.walls = None
        self.fps = 60

    def new_position_list(self):
        self.position_list = [[(p.x, p.y) for p in self.lists.penguins_list]]
        self.index = 0

    def update_position_list(self):
        self.position_list.append([(p.x, p.y) for p in self.lists.penguins_list])
        self.index += 1

    def update_active_player(self, player):
        self.active_player = player

    def update_objective(self):
        aux_token = Token(499 - 20, 508 - 20)
        aux_token.copy(self.token_list[self.random_list[self.tokens]])
        objective = aux_token

        objective.x = 230 + 12
        objective.y = 230 + 12
        self.objective = objective

    def initialize_buttons(self):
        # black = Penguin(200, 23, "black")
        # pieces_list.append(black)
        # '''
        # right = 1000
        right = 262 * 2
        aux_penguin_button_list = []

        # button_blue = PenguinButton(1000, 50, self.lists.penguins_list[0])
        button_blue = PenguinButton(right, 50, self.lists.penguins_list[0])
        aux_penguin_button_list.append(button_blue)
        # button_green = PenguinButton(1050, 50, self.lists.penguins_list[1])
        button_green = PenguinButton(right + 50, 50, self.lists.penguins_list[1])
        aux_penguin_button_list.append(button_green)
        # button_red = PenguinButton(1000, 100, self.lists.penguins_list[2])
        button_red = PenguinButton(right, 100, self.lists.penguins_list[2])
        aux_penguin_button_list.append(button_red)
        # button_yellow = PenguinButton(1050, 100, self.lists.penguins_list[3])
        button_yellow = PenguinButton(right + 50, 100, self.lists.penguins_list[3])
        aux_penguin_button_list.append(button_yellow)
        '''
        if BLACK:
            button_black = PenguinButton(1000, 150, black_penguin)
            aux_penguin_button_list.append(button_black)
        '''

        aux_functionality_button_list = []

        button_restart = FunctionalityButton(right, 240, "Restart")
        aux_functionality_button_list.append(button_restart)
        button_timer = FunctionalityButton(right, 200, "Time")
        aux_functionality_button_list.append(button_timer)
        button_rules = FunctionalityButton(right, 180, "Rules")
        aux_functionality_button_list.append(button_rules)
        button_settings = FunctionalityButton(right, 220, "Settings")
        aux_functionality_button_list.append(button_settings)

        button_back = MovementButton(right + 50, 200, "Back")
        aux_functionality_button_list.append(button_back)
        button_forward = MovementButton(right + 100, 200, "Forward")
        aux_functionality_button_list.append(button_forward)
        button_print = MovementButton(right + 100, 250, "Print list")
        aux_functionality_button_list.append(button_print)
        button_restart_position = MovementButton(right + 100, 350, "Restart position")
        aux_functionality_button_list.append(button_restart_position)

        aux_player_button_list = []
        aux = 1
        for pla in self.lists.players_list:
            pla_button = PlayerButton(right, 200 + aux * 20 + 50, pla)
            aux += 1
            aux_player_button_list.append(pla_button)

        self.buttons_lists = ButtonLists(aux_penguin_button_list, aux_player_button_list, aux_functionality_button_list)

    def print_text(self, win, mouse_x, mouse_y):
        aux = 10
        # right = 1000
        right = 262 * 2
        score_info = TEXT_FONT.render(f"Tokens obtained: {self.tokens}", True, (255, 255, 0))
        win.blit(score_info, (right, 200 + aux * 20))
        steps_info = TEXT_FONT.render(f"GLOBAL Steps: {self.steps}", True, (255, 255, 0))
        win.blit(steps_info, (right, 200 + (aux + 1) * 20))
        time_info = TEXT_FONT.render(f"Time: {self.remaining_time}", True, (255, 255, 0))
        win.blit(time_info, (right, 200 + (aux + 2) * 20))
        timer_info = TEXT_FONT.render(f"Time: {self.timer}", True, (255, 255, 0))
        win.blit(timer_info, (right, 200 + (aux + 3) * 20))
        # steps01_info = TEXT_FONT.render(f"Steps: {steps}", True, (255, 255, 0))
        # win.blit(steps01_info, (1000, 200 + (aux + 4) * 20))
        if self.active_player is not None:
            steps01_info = TEXT_FONT.render(f"Active player: {self.active_player.name}", True, (255, 255, 0))
        else:
            steps01_info = TEXT_FONT.render(f"Active player: None", True, (255, 255, 0))
        win.blit(steps01_info, (right, 200 + (aux + 5) * 20))
        waiting_info = TEXT_FONT.render(f"Waiting time: {self.hourglass}", True, (255, 255, 0))
        win.blit(waiting_info, (right, 200 + (aux + 6) * 20))
        index_info = TEXT_FONT.render(f"INDEX: {self.index}", True, (255, 255, 0))
        win.blit(index_info, (right, 200 + (aux + 7) * 20))
        # '''
        pieces_text = TEXT_FONT.render("Select your penguin", True, (255, 255, 0))
        coords_text = COORDS_FONT.render(f"Coords:  {int(mouse_x)}, {int(mouse_y)}", True, (255, 0, 255))
        win.blit(coords_text, (10, 10))
        win.blit(pieces_text, (right, 20))

    def draw(self, win, mouse_x, mouse_y):
        epsilon = 0
        win.fill(BLUE)
        # win.blit(bg, (0, 0))
        bg_list = build_board("Q1.png", "Q2.png", "Q3.png", "Q4.png")
        win.blit(bg_list[0], (0, 0))
        win.blit(bg_list[1], (262 + epsilon, 0))
        win.blit(bg_list[2], (262 + epsilon, 262 + epsilon))
        win.blit(bg_list[3], (0, 262 + epsilon))
        if SHOW_HITBOX:
            for hb in self.lists.hitbox_list:
                pygame.draw.rect(win, (255, 0, 0), hb)
        # for t in self.token_list:
        #     t.draw(win)
        self.objective.draw(win)
        self.lists.draw(win)

        self.buttons_lists.draw(win)
        # right = 1000
        right = 262*2
        # '''
        self.print_text(win, mouse_x, mouse_y)

        if self.player_not_selected:
            unselected_text = TEXT_FONT.render("Select a player before moving", True, (255, 255, 0))
            win.blit(unselected_text, (right, 200))
        pygame.display.update()

    def new_random_list(self):
        aux = [i for i in range(17)]
        random_list = []
        for i in range(17):
            random_list.append(aux.pop(randrange(1000) % len(aux)))
        self.random_list = random_list

        self.update_objective()
