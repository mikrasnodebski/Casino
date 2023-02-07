from random import choices


class NotEnoughPlayersError(Exception):
    def __init__(self):
        super().__init__("Incorrect number of players")


class Player:
    def __init__(self, name: str):
        self._name = name
        self._points = 0
        self._dice = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @property
    def dice(self):
        return self._dice

    @dice.setter
    def dice(self, new_dice: list):
        self._dice = new_dice

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, new_points):
        self._points = new_points

    def calculate_points(self):
        possible_score = {}
        all_odd = True
        all_even = True

        for value in self._dice:
            if value % 2 == 0:
                all_even = False
            else:
                all_odd = False

            if value not in possible_score:
                possible_score[value] = 1
            else:
                possible_score[value] += 1

        for key, value in possible_score.items():
            if value == 4:
                self._points = key * 6
            elif value == 3:
                self._points = key * 4
            elif value == 2:
                self._points = max(key * 2, self._points)

        if all_odd:
            self._points = max(sum(self._dice) + 2, self._points)
        elif all_even:
            self._points = max(sum(self._dice) + 3, self._points)

        if not possible_score:
            self._points = 0
        return self._points


class Casino:
    def __init__(self, players=None):
        self._players = [] if not players else players

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, new_players):
        self._players = new_players

    def add_player(self, player: Player):
        if player in self._players:
            raise ValueError("One player cannot be added twice")
        self._players.append(player)

    def remove_player(self, player: Player):
        if player not in self._players:
            raise ValueError("Player is not in the casino")
        self._players.remove(player)

    def roll_dice(self):
        return choices(range(1, 7), k=4)

    def play_game(self):
        if not self._players:
            raise NotEnoughPlayersError()
        for player in self._players:
            player.dice = self.roll_dice()
            player.calculate_points()
        return self.pick_winner()

    def pick_winner(self):
        player_points = []
        for player in self._players:
            player_points.append(player.points)
        highScore = max(player_points)
        if player_points.count(highScore) > 1:
            self._winner = None
        else:
            winnerIndex = player_points.index(highScore)
            self._winner = self._players[winnerIndex]
        return self._winner
