from flask.testing import FlaskClient


def test_request_example(client: FlaskClient):
    response = client.get("/")
    print(client)
    assert b"<h2>Hello, World!</h2>" in response.data
