from unittest.mock import patch


# Ideal case scenario integration test
def test_base_app_rundown(client):
    # Mock data
    clubs = [
        {"name": "Club1", "email": "mail1", "points": "13"},
        {"name": "Club2", "email": "mail2", "points": "4"},
        {"name": "Club3", "email": "mail3", "points": "12"},
    ]
    competitions = [
        {
            "name": "Competition1",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
            "places": {},
        },
        {
            "name": "Competition2",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13",
            "places": {},
        },
        {
            "name": "Competition3",
            "date": "2024-12-22 13:30:00",
            "numberOfPlaces": "17",
            "places": {},
        },
    ]

    with patch("server.clubs", clubs), patch("server.competitions", competitions):
        home_page_response = client.get("/")
        assert home_page_response.status_code == 200

        login_response = client.post(
            "/showSummary", data={"email": "mail1", "password": "password"}
        )
        assert login_response.status_code == 200
        assert "Club1" in str(login_response.data)
        assert "13" in str(login_response.data)

        booking_response = client.get("/book/Competition1/Club1")

        assert booking_response.status_code == 200

        purchase_places_response = client.post(
            "/purchasePlaces",
            data={"competition": "Competition1", "club": "Club1", "places": "10"},
        )

        assert b"Great-booking complete!" in purchase_places_response.data
        assert purchase_places_response.status_code == 200

        logout_response = client.get("/logout")
        assert logout_response.status_code == 302


# worst case scenario integration test
def test_worst_app_rundown(client):
    clubs = [
        {"name": "Club1", "email": "mail1", "points": "13"},
        {"name": "Club2", "email": "mail2", "points": "4"},
        {"name": "Club3", "email": "mail3", "points": "12"},
    ]
    competitions = [
        {
            "name": "Competition1",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
            "places": {},
        },
        {
            "name": "Competition2",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13",
            "places": {},
        },
        {
            "name": "Competition3",
            "date": "2024-12-22 13:30:00",
            "numberOfPlaces": "17",
            "places": {},
        },
    ]
    with patch("server.clubs", clubs), patch("server.competitions", competitions):
        home_page_response = client.get("/")
        assert home_page_response.status_code == 200

        login_response = client.post(
            "/showSummary", data={"email": "mail17", "password": "passworaaaad"}
        )
        assert login_response.status_code == 200
        assert "We couldn&#39;t find any club with this email" in str(
            login_response.data
        )

        response = client.get("/book/CompetitionX/ClubX")

        assert (
            b"You tried to manually access a club that does not exist, please use list below"
            in response.data
        )
        assert response.status_code == 200

        response = client.post(
            "/purchasePlaces",
            data={"competition": "Competition1", "club": "Club1", "places": "0"},
        )

        assert b"You must purchase at least one place" in response.data
        assert response.status_code == 200

        response = client.post(
            "/purchasePlaces",
            data={"competition": "Competition1", "club": "Club1", "places": "12"},
        )
        assert response.status_code == 200

        response = client.post(
            "/purchasePlaces",
            data={"competition": "Competition1", "club": "Club1", "places": "15"},
        )

        assert (
            b"you already have too many places booked for this competition"
            in response.data
        )
        assert response.status_code == 200

        response = client.post(
            "/purchasePlaces",
            data={"competition": "Competition1", "club": "Club1", "places": "10"},
        )
        assert response.status_code == 200
        assert b"Great-booking complete!" not in response.data

        logout_response = client.get("/logout")
        assert logout_response.status_code == 302
