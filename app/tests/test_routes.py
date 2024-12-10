# import pytest
# from app.api.game_routes import game_routes, game_states
# from flask import Flask
# import requests_mock
# from unittest.mock import patch

# BASE_URL_MEDIUM = "https://www.random.org/integers/?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new"
# BASE_URL_HARD = "https://www.random.org/integers/?num=6&min=0&max=7&col=1&base=10&format=plain&rnd=new"

# @pytest.fixture
# def client():
#     app = Flask(__name__)
#     app.register_blueprint(game_routes, url_prefix="/api/game")
#     with app.test_client() as client:
#         yield client

# def test_start_game_medium(client, requests_mock):
#     """Test starting a medium difficulty game."""
#     # The API returns text in one column with N numbers rather than a single line with all N numbers
#     mock_data = "0\n1\n2\n3"
#     requests_mock.get(BASE_URL_MEDIUM, text=mock_data)

#     response = client.get("/api/game/start/medium")
#     json_data = response.get_json()

#     assert response.status_code == 200
#     # JSON = {data: [{}], error: None}
#     assert "game_id" in json_data["data"][0]
#     assert "length" in json_data["data"][0]
#     assert "is_sequence_locally_generated" in json_data["data"][0]
#     assert json_data["data"][0]["is_sequence_locally_generated"] == False
#     game_id = json_data["data"][0]["game_id"]
#     length = json_data["data"][0]["length"]
#     assert game_id in game_states
#     assert length == 4
#     assert game_states[game_id]["solution"] == "0123"
#     assert game_states[game_id]["status"] == "ongoing"
#     assert game_states[game_id]["attempts_left"] == 10
    
# def test_start_game_hard(client, requests_mock):
#     """Test starting a hard difficulty game."""
#     # The API returns text in one column with N numbers rather than a single line with all N numbers
#     mock_data = "0\n1\n2\n3\n4\n5"
#     requests_mock.get(BASE_URL_HARD, text=mock_data)

#     response = client.get("/api/game/start/hard")
#     json_data = response.get_json()

#     assert response.status_code == 200
#     # JSON = {data: [{}], error: None}
#     assert "game_id" in json_data["data"][0]
#     assert "length" in json_data["data"][0]
#     assert "is_sequence_locally_generated" in json_data["data"][0]
#     assert json_data["data"][0]["is_sequence_locally_generated"] == False
#     game_id = json_data["data"][0]["game_id"]
#     length = json_data["data"][0]["length"]
#     assert game_id in game_states
#     assert length == 6
#     assert game_states[game_id]["solution"] == "012345"
#     assert game_states[game_id]["status"] == "ongoing"
#     assert game_states[game_id]["attempts_left"] == 10
    
# def test_start_game_invalid_difficulty(client, requests_mock):
#     """Test starting a game with an invalid difficulty."""
#     response = client.get("/api/game/start/easy")
#     json_data = response.get_json()

#     assert response.status_code == 400
#     assert json_data["data"] == []
#     assert json_data["error"] == "Invalid difficulty level."

# def test_make_guess_win_medium(client, requests_mock):
#     mock_data = "1\n2\n3\n4"
#     requests_mock.get(BASE_URL_MEDIUM, text=mock_data)

#     start_response = client.get("/api/game/start/medium")
#     game_id = start_response.get_json()["data"][0]["game_id"]

#     # Simulate a winning guess
#     response = client.post("/api/game/guess", json={
#         "game_id": game_id,
#         "guess": "1234"
#     })
#     json_data = response.get_json()

#     assert response.status_code == 200
#     assert json_data["data"][0]["status"] == "win"
#     assert json_data["data"][0]["correct_positions"] == 4
#     assert json_data["data"][0]["correct_numbers_only"] == 0
#     assert json_data["data"][0]["attempts_left"] == 9
#     assert json_data["data"][0]["solution"] == "1234"
    
# def test_make_guess_win_hard(client, requests_mock):
#     mock_data = "0\n1\n2\n3\n4\n5"
#     requests_mock.get(BASE_URL_HARD, text=mock_data)

#     start_response = client.get("/api/game/start/hard")
#     game_id = start_response.get_json()["data"][0]["game_id"]

#     # Simulate a winning guess
#     response = client.post("/api/game/guess", json={
#         "game_id": game_id,
#         "guess": "012345"
#     })
#     json_data = response.get_json()

#     assert response.status_code == 200
#     assert json_data["data"][0]["status"] == "win"
#     assert json_data["data"][0]["correct_positions"] == 6
#     assert json_data["data"][0]["correct_numbers_only"] == 0
#     assert json_data["data"][0]["attempts_left"] == 9
#     assert json_data["data"][0]["solution"] == "012345"

# def test_make_guess_lose_medium(client, requests_mock):
#     mock_data = "1\n2\n3\n4"
#     requests_mock.get(BASE_URL_MEDIUM, text=mock_data)

#     start_response = client.get("/api/game/start/medium")
#     game_id = start_response.get_json()["data"][0]["game_id"]

#     # Simulate losing by exhausting the 10 attempts
#     for i in range(10):
#         response = client.post("/api/game/guess", json={
#             "game_id": game_id,
#             "guess": "5678"  # Incorrect guess
#         })
#         json_data = response.get_json()
#         assert json_data["data"][0]["status"] == ("lose" if i == 9 else "ongoing")
#         assert json_data["data"][0]["attempts_left"] == (9 - i)
#         if i < 9:
#             assert "solution" not in json_data["data"][0]
#         else:
#             assert "solution" in json_data["data"][0]
#             assert json_data["data"][0]["solution"] == "1234"
        
# def test_make_guess_lose_hard(client, requests_mock):
#     mock_data = "0\n1\n2\n3\n4\n5"
#     requests_mock.get(BASE_URL_HARD, text=mock_data)

#     start_response = client.get("/api/game/start/hard")
#     game_id = start_response.get_json()["data"][0]["game_id"]

#     # Simulate losing by exhausting the 10 attempts
#     for i in range(10):
#         response = client.post("/api/game/guess", json={
#             "game_id": game_id,
#             "guess": "567801"  # Incorrect guess
#         })
#         json_data = response.get_json()
#         assert json_data["data"][0]["status"] == ("lose" if i == 9 else "ongoing")
#         assert json_data["data"][0]["attempts_left"] == (9 - i)
#         if i < 9:
#             assert "solution" not in json_data["data"][0]
#         else:
#             assert "solution" in json_data["data"][0]
#             assert json_data["data"][0]["solution"] == "012345"

# def test_make_guess_after_win(client, requests_mock):
#     """Test making a guess after the game has been won."""
#     mock_data = "1\n2\n3\n4"
#     requests_mock.get(BASE_URL_MEDIUM, text=mock_data)

#     start_response = client.get("/api/game/start/medium")
#     game_id = start_response.get_json()["data"][0]["game_id"]

#     # Simulate a winning guess
#     client.post("/api/game/guess", json={
#         "game_id": game_id,
#         "guess": "1234"
#     })

#     # Attempt to guess again after winning
#     response = client.post("/api/game/guess", json={
#         "game_id": game_id,
#         "guess": "1234"
#     })
#     json_data = response.get_json()

#     assert response.status_code == 400
#     assert json_data["data"] == []
#     assert json_data["error"] == "This game has already ended."

# def test_make_guess_after_lose(client, requests_mock):
#     """Test making a guess after the game has been lost."""
#     mock_data = "1\n2\n3\n4"
#     requests_mock.get(BASE_URL_MEDIUM, text=mock_data)

#     start_response = client.get("/api/game/start/medium")
#     game_id = start_response.get_json()["data"][0]["game_id"]

#     # Simulate 10 incorrect guesses
#     for _ in range(10):
#         client.post("/api/game/guess", json={
#             "game_id": game_id,
#             "guess": "5678"  # Incorrect guess
#         })

#     # Attempt to guess again after losing
#     response = client.post("/api/game/guess", json={
#         "game_id": game_id,
#         "guess": "5678"
#     })
#     json_data = response.get_json()

#     assert response.status_code == 400
#     assert json_data["data"] == []
#     assert json_data["error"] == "This game has already ended."

# def test_make_guess_invalid_game_id(client, requests_mock):
#     """Test making a guess with an invalid game_id."""
#     response = client.post("/api/game/guess", json={
#         "game_id": "invalid-game-id",
#         "guess": "1234"
#     })
#     json_data = response.get_json()

#     assert response.status_code == 404
#     assert json_data["data"] == []
#     assert json_data["error"] == "Game ID not found."

# def test_make_guess_invalid_payload_missing_game_id(client):
#     """Test making a guess with missing game_id."""
#     response = client.post("/api/game/guess", json={
#         "guess": "1234"
#     })
#     json_data = response.get_json()

#     assert response.status_code == 400
#     assert json_data["data"] == []
#     assert json_data["error"] == "Invalid request format."

# def test_make_guess_invalid_payload_missing_guess(client):
#     """Test making a guess with missing guess."""
#     response = client.post("/api/game/guess", json={
#         "game_id": "some-game-id"
#     })
#     json_data = response.get_json()

#     assert response.status_code == 400
#     assert json_data["data"] == []
#     assert json_data["error"] == "Invalid request format."

# def test_make_guess_invalid_guess_length(client, requests_mock):
#     """Test making a guess with invalid guess length."""
#     mock_data = "1\n2\n3\n4\n"
#     requests_mock.get(BASE_URL_MEDIUM, text=mock_data)

#     start_response = client.get("/api/game/start/medium")
#     game_id = start_response.get_json()["data"][0]["game_id"]

#     # Guess with incorrect length
#     response = client.post("/api/game/guess", json={
#         "game_id": game_id,
#         "guess": "123"  # Should be 4 digits
#     })
#     json_data = response.get_json()

#     assert response.status_code == 400
#     assert json_data["data"] == []
#     assert json_data["error"] == "Guess must be a 4-digit string."

# def test_make_guess_non_digit_guess(client, requests_mock):
#     """Test making a guess with non-digit characters."""
#     mock_data = "1\n2\n3\n4\n"
#     requests_mock.get(BASE_URL_MEDIUM, text=mock_data)

#     start_response = client.get("/api/game/start/medium")
#     game_id = start_response.get_json()["data"][0]["game_id"]

#     # Guess with non-digit characters
#     response = client.post("/api/game/guess", json={
#         "game_id": game_id,
#         "guess": "12a4"
#     })
#     json_data = response.get_json()

#     assert response.status_code == 400
#     assert json_data["data"] == []
#     assert json_data["error"] == "Guess must be a 4-digit string."

# def test_start_game_medium_fallback(client, requests_mock):
#     """Test starting a medium difficulty game when Random.org API fails, triggering fallback."""
#     # Simulate API failure. This is to test the utils/generate_local_sequence function
#     requests_mock.get(BASE_URL_MEDIUM, status_code=503)

#     # config = {'method.return_value': 3, 'other.side_effect': KeyError}
    
#     # Mocking the response returned by the function in the context of the API rather than where it was defined
#     with patch("app.api.game_routes.generate_local_sequence", return_value="0\n1\n2\n3"):
#         response = client.get("/api/game/start/medium")
#         json_data = response.get_json()

#         assert response.status_code == 200
#         # JSON = {data: [{}], error: None}
#         assert "game_id" in json_data["data"][0]
#         assert "length" in json_data["data"][0]
#         assert "is_sequence_locally_generated" in json_data["data"][0]
#         assert json_data["data"][0]["is_sequence_locally_generated"] == True

#         game_id = json_data["data"][0]["game_id"]
#         length = json_data["data"][0]["length"]
#         assert game_id in game_states
#         assert length == 4
#         assert game_states[game_id]["solution"] == "0123"
#         assert len(game_states[game_id]["solution"]) == 4
#         assert game_states[game_id]["status"] == "ongoing"
#         assert game_states[game_id]["attempts_left"] == 10

# def test_start_game_hard_fallback(client, requests_mock):
#     """Test starting a hard difficulty game when Random.org API fails, triggering fallback."""
#     # Simulate API failure
#     requests_mock.get(BASE_URL_HARD, status_code=503)

#     with patch("app.api.game_routes.generate_local_sequence", return_value="0\n1\n2\n3\n4\n5"):
#         response = client.get("/api/game/start/hard")
#         json_data = response.get_json()

#         assert response.status_code == 200
#         # JSON = {data: [{}], error: None}
#         assert "game_id" in json_data["data"][0]
#         assert "length" in json_data["data"][0]
#         assert "is_sequence_locally_generated" in json_data["data"][0]
#         assert json_data["data"][0]["is_sequence_locally_generated"] == True

#         game_id = json_data["data"][0]["game_id"]
#         length = json_data["data"][0]["length"]
#         assert game_id in game_states
#         assert length == 6
#         assert game_states[game_id]["solution"] == "012345" 
#         assert len(game_states[game_id]["solution"]) == 6
#         assert game_states[game_id]["status"] == "ongoing"
#         assert game_states[game_id]["attempts_left"] == 10

# # Resource for mocking my endpoint which calls a function to generate it in case the third party API fails: 
# # https://stackoverflow.com/questions/53590758/how-to-mock-function-call-in-flask-restul-resource-method
# def test_make_guess_with_fallback_sequence_revealed_on_win(client, requests_mock):
#     """Test that when a game started with a fallback, the solution is revealed upon winning."""
#     # Simulate API failure
#     requests_mock.get(BASE_URL_MEDIUM, status_code=503)

#     with patch("app.api.game_routes.generate_local_sequence", return_value="0\n1\n2\n3"):
#         start_response = client.get("/api/game/start/medium")
#         game_id = start_response.get_json()["data"][0]["game_id"]

#         # Simulate a winning guess
#         response = client.post("/api/game/guess", json={
#             "game_id": game_id,
#             "guess": "0123"
#         })
#         json_data = response.get_json()

#         assert response.status_code == 200
#         assert json_data["data"][0]["status"] == "win"
#         assert json_data["data"][0]["correct_positions"] == 4
#         assert json_data["data"][0]["correct_numbers_only"] == 0
#         assert json_data["data"][0]["attempts_left"] == 9
#         assert json_data["data"][0]["solution"] == "0123"

# def test_make_guess_with_fallback_sequence_revealed_on_lose(client, requests_mock):
#     """Test that when a game started with a fallback, the solution is revealed upon losing."""
#     # Simulate API failure
#     requests_mock.get(BASE_URL_MEDIUM, status_code=503)
    
#     with patch("app.api.game_routes.generate_local_sequence", return_value="0\n1\n2\n3"):
#         start_response = client.get("/api/game/start/medium")
#         game_id = start_response.get_json()["data"][0]["game_id"]

#         # Simulate losing by exhausting the 10 attempts
#         for i in range(10):
#             response = client.post("/api/game/guess", json={
#                 "game_id": game_id,
#                 "guess": "5678"  # Incorrect guess
#             })
#             json_data = response.get_json()
#             assert json_data["data"][0]["status"] == ("lose" if i == 9 else "ongoing")
#             assert json_data["data"][0]["attempts_left"] == (9 - i)
#             if i < 9:
#                 assert "solution" not in json_data["data"][0]
#             else:
#                 assert "solution" in json_data["data"][0]
#                 assert json_data["data"][0]["solution"] == "0123"