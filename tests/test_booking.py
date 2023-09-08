from unittest.mock import patch

### UNIT TESTS ###


def test_book_valid_route(client):
    # Mock data
    clubs = [{"name": "Club1", "email": "mail1"}, {"name": "Club2", "email": "mail2"}]
    competitions = [{"name": "Competition1"}, {"name": "Competition2"}]

    with patch("server.clubs", clubs), patch("server.competitions", competitions):
        response = client.get("/book/Competition1/Club1")

    assert response.status_code == 200


def test_book_invalid_route(client):
    # Mock data
    clubs = [{"name": "Club1", "email": "mail1"}, {"name": "Club2", "email": "mail2"}]
    competitions = [
        {"name": "Competition1", "numberOfPlaces": "10"},
        {"name": "Competition2", "numberOfPlaces": "4"},
    ]

    with patch("server.clubs", clubs), patch("server.competitions", competitions):
        response = client.get("/book/Competition3/Club3")

    assert (
        b"You tried to manually access a club that does not exist, please use list below"
        in response.data
    )
    assert response.status_code == 200


def test_book_invalid_to_many_clubs(client):
    # Mock data
    clubs = [{"name": "Club1", "email": "mail1"}, {"name": "Club1", "email": "mail2"}]
    competitions = [
        {"name": "Competition1", "numberOfPlaces": "10"},
        {"name": "Competition2", "numberOfPlaces": "4"},
    ]

    with patch("server.clubs", clubs), patch("server.competitions", competitions):
        response = client.get("/book/Competition1/Club1")

    assert (
        b"There are multiple clubs with this name, please use list below"
        in response.data
    )
    assert response.status_code == 200
