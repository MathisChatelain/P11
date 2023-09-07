from unittest.mock import patch


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_show_summary_with_valid_email(client):
    with patch(
        "server.clubs",
        [{"name": "club1", "email": "mail1", "points": "13"}],
    ):
        response = client.post(
            "/showSummary",
            data={"email": ["mail1"]},
        )
        assert response.status_code == 200
        assert "club1" in str(response.data)
        assert "13" in str(response.data)


def test_show_summary_with_invalid_email(client):
    with patch(
        "server.clubs",
        [{"name": "club1", "email": "mail1", "points": "13"}],
    ):
        response = client.post(
            "/showSummary",
            data={"email": ["mail2"]},
        )
        assert response.status_code == 200
        assert "We couldn&#39;t find any club with this email" in str(response.data)
        assert "club1" not in str(response.data)
        assert "13" not in str(response.data)


def test_found_to_many_clubs_with_this_email(client):
    with patch(
        "server.clubs",
        [
            {"name": "club1", "email": "mail1", "points": "13"},
            {"name": "club2", "email": "mail1", "points": "13"},
        ],
    ):
        response = client.post(
            "/showSummary",
            data={"email": ["mail1"]},
        )
        assert response.status_code == 200
        assert "We found multiple clubs with this email" in str(response.data)
        assert "club1" not in str(response.data)
        assert "club2" not in str(response.data)
        assert "13" not in str(response.data)
