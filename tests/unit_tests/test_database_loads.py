from server import loadClubs, loadCompetitions

### UNIT TESTS ###


def test_load_competitions():
    competitions = loadCompetitions()
    assert len(competitions) == 3
    assert type(competitions) == list
    assert type(competitions[0]) == dict


def test_load_clubs():
    clubs = loadClubs()
    assert len(clubs) == 3
    assert type(clubs) == list
    assert type(clubs[0]) == dict
