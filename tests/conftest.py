import pytest
from flask import Flask


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.secret_key = "something_special"
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
