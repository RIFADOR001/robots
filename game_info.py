


class GameInfo(object):
    def __init__(self, pieces_list, buttons, players_list):
        self.pieces_list = pieces_list
        self.buttons = buttons
        self.player_list = players_list
        self.position_list = [[(p.x, p.y) for p in players_list]]
        self.index = 0
        self.tokens = 0
        self.timer = False
        self.hourglass = False
        self.max_time = 30
        self.steps = 0
        self.player_not_selected = True
        self.active_player = None

    def new_position_list(self):
        self.position_list = [[(p.x, p.y) for p in self.players_list]]
        self.index = 0

    def update_position_list(self):
        self.position_list.append([(p.x, p.y) for p in self.players_list])
        self.index += 1

    def update_active_player(self, player):
        self.active_player = player


