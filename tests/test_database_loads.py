from server import loadClubs, loadCompetitions


def test_load_competitions():
    competitions = loadCompetitions()
    assert len(competitions) == 2


def test_load_clubs():
    clubs = loadClubs()
    assert len(clubs) == 3
