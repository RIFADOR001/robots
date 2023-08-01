from piecesPlayersTokens import listsPenguinPlayersHitbox
from buttons import ButtonLists
from graphics import BLUE, bg, SHOW_HITBOX
import pygame
from game_config import*


class GameInfo(object):
    def __init__(self, pieces_list, buttons_lists, players_list, hitbox_list, token_list):
        # self.pieces_list = pieces_list
        self.buttons_lists = buttons_lists
        # self.player_list = players_list
        self.position_list = [[(p.x, p.y) for p in players_list]]
        self.index = 0
        self.tokens = 0
        self.timer = False
        self.hourglass = False
        self.max_time = 30
        self.steps = 0
        self.player_not_selected = True
        self.active_player = None
        self.objective = None
        self.remaining_time = self.max_time
        self.lists = listsPenguinPlayersHitbox(pieces_list, players_list, hitbox_list)
        self.token_list = token_list

    def new_position_list(self):
        self.position_list = [[(p.x, p.y) for p in self.lists.players_list]]
        self.index = 0

    def update_position_list(self):
        self.position_list.append([(p.x, p.y) for p in self.lists.players_list])
        self.index += 1

    def update_active_player(self, player):
        self.active_player = player

    def draw(self, win, mouse_x, mouse_y):
        win.fill(BLUE)
        win.blit(bg, (0, 0))
        if SHOW_HITBOX:
            for hb in self.lists.hitbox_list:
                pygame.draw.rect(win, (255, 0, 0), hb)
        for t in self.token_list:
            t.draw(win)
        self.lists.draw(win)

        self.objective.draw(win)
        aux = 10
        self.buttons_lists.draw(win)


        # '''
        score_info = TEXT_FONT.render(f"Tokens obtained: {self.tokens}", True, (255, 255, 0))
        win.blit(score_info, (1000, 200 + aux * 20))
        steps_info = TEXT_FONT.render(f"GLOBAL Steps: {self.steps}", True, (255, 255, 0))
        win.blit(steps_info, (1000, 200 + (aux + 1) * 20))
        time_info = TEXT_FONT.render(f"Time: {self.remaining_time}", True, (255, 255, 0))
        win.blit(time_info, (1000, 200 + (aux + 2) * 20))
        timer_info = TEXT_FONT.render(f"Time: {self.timer}", True, (255, 255, 0))
        win.blit(timer_info, (1000, 200 + (aux + 3) * 20))
        # steps01_info = TEXT_FONT.render(f"Steps: {steps}", True, (255, 255, 0))
        # win.blit(steps01_info, (1000, 200 + (aux + 4) * 20))
        steps01_info = TEXT_FONT.render(f"Active player: {self.active_player.name}", True, (255, 255, 0))
        win.blit(steps01_info, (1000, 200 + (aux + 5) * 20))
        waiting_info = TEXT_FONT.render(f"Waiting time: {self.hourglass}", True, (255, 255, 0))
        win.blit(waiting_info, (1000, 200 + (aux + 6) * 20))
        INDEX_info = TEXT_FONT.render(f"INDEX: {self.index}", True, (255, 255, 0))
        win.blit(INDEX_info, (1000, 200 + (aux + 7) * 20))
        # '''
        pieces_text = TEXT_FONT.render("Select your penguin", True, (255, 255, 0))
        coords_text = COORDS_FONT.render(f"Coords:  {mouse_x}, {mouse_y}", True, (255, 0, 255))


        win.blit(coords_text, (10, 10))
        win.blit(pieces_text, (1000, 20))
        if self.player_not_selected:
            unselected_text = TEXT_FONT.render("Select a player before moving", True, (255, 255, 0))
            win.blit(unselected_text, (1000, 200))

