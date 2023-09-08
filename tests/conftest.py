import pytest
from flask import Flask
from server import app as server_app


@pytest.fixture()
def app():
    app = server_app
    app.secret_key = "something_special"
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app: Flask):
    return app.test_client()
