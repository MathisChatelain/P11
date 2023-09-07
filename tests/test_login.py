import pytest
from unittest.mock import Mock, patch


def test_show_summary_with_valid_email(client):
    mock_load_clubs = Mock(return_value=[{"email": "test@test.com"}])
    with patch("server.loadClubs", mock_load_clubs):
        print("here", mock_load_clubs())
        clubs = mock_load_clubs()
        response = client.post(
            "/showSummary",
            data={"email": ["test@test.com"]},
        )
        assert response.status_code == 200
