from casino import Casino, Player, NotEnoughPlayersError
from pytest import raises


def test_player_init_name():
    jack = Player("Jack Black")
    assert jack.name == "Jack Black"


def test_start_player_points():
    jack = Player("Jack Black")
    assert jack.points == 0


def test_dice_after_roll(monkeypatch):
    jack = Player("Jack Black")
    lasVegas = Casino()

    def fake_roll(a):
        return [1, 2, 3, 4]

    monkeypatch.setattr('casino.Casino.roll_dice', fake_roll)
    lasVegas.add_player(jack)
    lasVegas.play_game()
    assert jack.dice == [1, 2, 3, 4]


def test_empty_casino():
    lasVegas = Casino()
    assert lasVegas.players == []


def test_points_all_odd_four_same(monkeypatch):
    jack = Player("Jack Black")
    lasVegas = Casino()

    def fake_roll(a):
        return [5, 5, 5, 5]

    monkeypatch.setattr('casino.Casino.roll_dice', fake_roll)
    lasVegas.add_player(jack)
    lasVegas.play_game()
    assert jack.points == 30


def test_points_all_odd_three_same(monkeypatch):
    jack = Player("Jack Black")
    lasVegas = Casino()

    def fake_roll(a):
        return [1, 3, 1, 1]

    monkeypatch.setattr('casino.Casino.roll_dice', fake_roll)
    lasVegas.add_player(jack)
    lasVegas.play_game()
    assert jack.points == 9


def test_points_all_odd_one_pair(monkeypatch):
    jack = Player("Jack Black")
    lasVegas = Casino()

    def fake_roll(a):
        return [1, 3, 1, 5]

    monkeypatch.setattr('casino.Casino.roll_dice', fake_roll)
    lasVegas.add_player(jack)
    lasVegas.play_game()
    assert jack.points == 13


def test_points_all_odd_two_pairs(monkeypatch):
    jack = Player("Jack Black")
    lasVegas = Casino()

    def fake_roll(a):
        return [1, 5, 1, 5]

    monkeypatch.setattr('casino.Casino.roll_dice', fake_roll)
    lasVegas.add_player(jack)
    lasVegas.play_game()
    assert jack.points == 15


def test_points_all_even_four_same(monkeypatch):
    jack = Player("Jack Black")
    lasVegas = Casino()

    def fake_roll(a):
        return [2, 2, 2, 2]

    monkeypatch.setattr('casino.Casino.roll_dice', fake_roll)
    lasVegas.add_player(jack)
    lasVegas.play_game()
    assert jack.points == 12


def test_points_all_even_three_same(monkeypatch):
    jack = Player("Jack Black")
    lasVegas = Casino()

    def fake_roll(a):
        return [4, 4, 4, 2]

    monkeypatch.setattr('casino.Casino.roll_dice', fake_roll)
    lasVegas.add_player(jack)
    lasVegas.play_game()
    assert jack.points == 16


def test_points_all_even_one_pair(monkeypatch):
    jack = Player("Jack Black")
    lasVegas = Casino()

    def fake_roll(a):
        return [4, 2, 2, 6]

    monkeypatch.setattr('casino.Casino.roll_dice', fake_roll)
    lasVegas.add_player(jack)
    lasVegas.play_game()
    assert jack.points == 16


def test_points_all_even_two_pairs(monkeypatch):
    jack = Player("Jack Black")
    lasVegas = Casino()

    def fake_roll(a):
        return [2, 2, 6, 6]

    monkeypatch.setattr('casino.Casino.roll_dice', fake_roll)
    lasVegas.add_player(jack)
    lasVegas.play_game()
    assert jack.points == 18


def test_check_win(monkeypatch):
    lasVegas = Casino()
    player1 = Player("Jack Black")
    player2 = Player("Alex")
    lasVegas.add_player(player1)
    lasVegas.add_player(player2)
    player1.dice = [2, 2, 2, 2]
    player2.dice = [1, 1, 1, 1]
    player1.calculate_points()
    player2.calculate_points()
    lasVegas.pick_winner()
    assert lasVegas._winner.name == "Jack Black"
    assert lasVegas.play_game() is player1


def test_check_draw(monkeypatch):
    lasVegas = Casino()
    player1 = Player("Jack Black")
    player2 = Player("Alex")
    lasVegas.add_player(player1)
    lasVegas.add_player(player2)

    def fake_roll(a):
        return [5, 2, 2, 5]

    monkeypatch.setattr('casino.Casino.roll_dice', fake_roll)
    lasVegas.play_game()
    assert lasVegas.play_game() is None


def test_check_draw_zero_points(monkeypatch):
    lasVegas = Casino()
    player1 = Player("Jack Black")
    player2 = Player("Alex")
    lasVegas.add_player(player1)
    lasVegas.add_player(player2)

    def fake_roll(a):
        return [1, 2, 3, 4]

    monkeypatch.setattr('casino.Casino.roll_dice', fake_roll)
    lasVegas.play_game()
    assert lasVegas.play_game() is None


def test_zero_points(monkeypatch):
    jack = Player("Jack Black")
    lasVegas = Casino()

    def fake_roll(a):
        return [2, 3, 1, 5]

    monkeypatch.setattr('casino.Casino.roll_dice', fake_roll)
    lasVegas.add_player(jack)
    lasVegas.play_game()
    assert jack.points == 0


def test_add_same_players():
    with raises(ValueError) as excinfo:
        jack = Player("Jack Black")
        lasVegas = Casino()
        lasVegas.add_player(jack)
        lasVegas.add_player(jack)
    assert "One player cannot be added twice" in str(excinfo.value)


def test_check_play_draw(monkeypatch):
    lasVegas = Casino()
    player1 = Player("Jack Black")
    player2 = Player("Alex")
    lasVegas.add_player(player1)
    lasVegas.add_player(player2)

    def set_win(a):
        return None

    monkeypatch.setattr('casino.Casino.pick_winner', set_win)
    assert lasVegas.play_game() is None


def test_game_one_winner(monkeypatch):
    lasVegas = Casino()
    player1 = Player("Jack Black")
    player2 = Player("Alex")
    lasVegas.add_player(player1)
    lasVegas.add_player(player2)

    def set_win(a):
        return player1

    monkeypatch.setattr('casino.Casino.pick_winner', set_win)
    assert lasVegas.play_game() is player1


def test_check_remove_player():
    lasVegas = Casino()
    player1 = Player("Jack Black")
    player2 = Player("Alex")
    lasVegas.add_player(player1)
    lasVegas.add_player(player2)
    lasVegas.remove_player(player1)
    assert player1 not in lasVegas.players


def test_check_remove_non_existing_player():
    lasVegas = Casino()
    player1 = Player("Jack Black")
    player2 = Player("Alex")
    lasVegas.add_player(player1)
    with raises(ValueError) as excinfo:
        lasVegas.remove_player(player2)
    assert "Player is not in the casino" in str(excinfo.value)


def test_zero_players_in_game():
    lasVegas = Casino()
    with raises(NotEnoughPlayersError) as excinfo:
        lasVegas.play_game()
    assert "Incorrect number of players" in str(excinfo.value)
