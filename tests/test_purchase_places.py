from unittest.mock import patch

### UNIT TESTS ###


def test_purchasePlaces_valid_request(client):
    # Mock data
    competitions = [{"name": "Competition1", "numberOfPlaces": 10, "places": {}}]
    clubs = [{"name": "Club1", "points": 20, "email": "mail1"}]

    with patch("server.clubs", clubs), patch("server.competitions", competitions):
        response = client.post(
            "/purchasePlaces",
            data={"competition": "Competition1", "club": "Club1", "places": "5"},
        )

    assert b"Great-booking complete!" in response.data
    assert response.status_code == 200


def test_purchasePlaces_invalid_places(client):
    # Mock data
    competitions = [{"name": "Competition1", "numberOfPlaces": 10, "places": {}}]
    clubs = [{"name": "Club1", "points": 20, "email": "mail1"}]

    with patch("server.clubs", clubs), patch("server.competitions", competitions):
        response = client.post(
            "/purchasePlaces",
            data={"competition": "Competition1", "club": "Club1", "places": "0"},
        )

    assert b"You must purchase at least one place" in response.data
    assert response.status_code == 200


def test_purchasePlaces_not_enough_points(client):
    # Mock data
    competitions = [{"name": "Competition1", "numberOfPlaces": 10, "places": {}}]
    clubs = [{"name": "Club1", "points": 5, "email": "mail1"}]

    with patch("server.clubs", clubs), patch("server.competitions", competitions):
        response = client.post(
            "/purchasePlaces",
            data={"competition": "Competition1", "club": "Club1", "places": "10"},
        )

    assert b"Sorry, you do not have enough points" in response.data
    assert response.status_code == 200


def test_purchasePlaces_not_enough_places(client):
    # Mock data
    competitions = [{"name": "Competition1", "numberOfPlaces": 5, "places": {}}]
    clubs = [{"name": "Club1", "points": 20, "email": "mail1"}]

    with patch("server.clubs", clubs), patch("server.competitions", competitions):
        response = client.post(
            "/purchasePlaces",
            data={"competition": "Competition1", "club": "Club1", "places": "10"},
        )

    assert b"Sorry, there are not enough places remaining" in response.data
    assert response.status_code == 200


def test_purchasePlaces_trying_to_buy_to_much_places_in_total(client):
    # Mock data
    competitions = [
        {"name": "Competition1", "numberOfPlaces": 10, "places": {"mail1": 12}}
    ]
    clubs = [{"name": "Club1", "points": 20, "email": "mail1"}]

    with patch("server.clubs", clubs), patch("server.competitions", competitions):
        response = client.post(
            "/purchasePlaces",
            data={"competition": "Competition1", "club": "Club1", "places": "10"},
        )

    assert b"you already have 12 places booked for this competition" in response.data
    assert b"You cannot book more than 12 places for a competition" in response.data
    assert response.status_code == 200


def test_purchasePlaces_trying_to_buy_to_much_places(client):
    # Mock data
    competitions = [{"name": "Competition1", "numberOfPlaces": 10, "places": {}}]
    clubs = [{"name": "Club1", "points": 20, "email": "mail1"}]

    with patch("server.clubs", clubs), patch("server.competitions", competitions):
        response = client.post(
            "/purchasePlaces",
            data={"competition": "Competition1", "club": "Club1", "places": "13"},
        )

    assert b"you already have 0 places booked for this competition" in response.data
    assert b"You cannot book more than 12 places for a competition" in response.data
    assert response.status_code == 200
