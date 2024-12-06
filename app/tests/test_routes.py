import pytest
from app.api.game_routes import game_routes, game_states
from flask import Flask
import requests_mock

BASE_URL = "https://www.random.org/integers/?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new"

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(game_routes, url_prefix="/api/game")
    with app.test_client() as client:
        yield client

def test_start_game(client, requests_mock):
    # The API returns text in one column with N numbers rather than a single line with all N numbers
    mock_data = "0\n1\n2\n3\n"
    requests_mock.get(BASE_URL, text=mock_data)

    response = client.get("/api/game/start")
    json_data = response.get_json()

    assert response.status_code == 200
    # JSON = {data: [{}], error: None}
    assert "game_id" in json_data["data"][0]
    game_id = json_data["data"][0]["game_id"]
    assert game_id in game_states
    assert game_states[game_id]["solution"] == "0123"
    assert game_states[game_id]["attempts_left"] == 10

def test_make_guess_win(client, requests_mock):
    mock_data = "1\n2\n3\n4\n"
    requests_mock.get(BASE_URL, text=mock_data)

    start_response = client.get("/api/game/start")
    game_id = start_response.get_json()["data"][0]["game_id"]

    # Simulate a winning guess
    response = client.post("/api/game/guess", json={
        "game_id": game_id,
        "guess": "1234"
    })
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["data"][0]["status"] == "win"
    assert json_data["data"][0]["correct_positions"] == 4
    assert json_data["data"][0]["correct_numbers_only"] == 0

def test_make_guess_lose(client, requests_mock):
    mock_data = "1\n2\n3\n4\n"
    requests_mock.get(BASE_URL, text=mock_data)

    start_response = client.get("/api/game/start")
    game_id = start_response.get_json()["data"][0]["game_id"]

    # Simulate losing by exhausting the 10 attempts
    for i in range(10):
        response = client.post("/api/game/guess", json={
            "game_id": game_id,
            "guess": "5678"  # Incorrect guess
        })
        json_data = response.get_json()
        assert json_data["data"][0]["status"] == ("lose" if i == 9 else "ongoing")
        assert json_data["data"][0]["attempts_left"] == (9 - i)
