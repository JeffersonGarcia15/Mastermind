from flask import Blueprint, request
# https://flask-limiter.readthedocs.io/en/stable/
import requests
import uuid
from ..rate_limiter import limiter
from ..utils.responses import success_response, error_response

from ..utils.get_hint import get_hint

BASE_URL_MEDIUM = "https://www.random.org/integers/?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new"
BASE_URL_HARD = "https://www.random.org/integers/?num=6&min=0&max=7&col=1&base=10&format=plain&rnd=new"
ALLOWED_DIFFICULTIES = ["medium", "hard"]

game_routes = Blueprint("game", __name__)

game_states = {}

def fetch_random_sequence(difficulty):
    """Fetches a random sequence from Random.org based on difficulty."""
    if difficulty not in ALLOWED_DIFFICULTIES:
        # Early return if invalid difficulty
        return None, "Invalid difficulty level."

    # Select the appropriate URL based on difficulty
    url = BASE_URL_MEDIUM if difficulty == "medium" else BASE_URL_HARD

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.text.split()

        expected_length = 4 if difficulty == "medium" else 6
        if len(data) != expected_length or any(not line.isdigit() for line in data):
            return None, "Invalid data received from the random number generator."

        sequence = "".join(data)
        return sequence, None
    except requests.exceptions.RequestException as error:
        return None, str(error)

# 5 games per minute per IP address
# https://medium.com/analytics-vidhya/how-to-rate-limit-routes-in-flask-61c6c791961b#:~:text=In%20flask%20there%20is%20a,track%20of%20their%20IP%20address.
@game_routes.route("/start/<string:difficulty>", methods=["GET"])
@limiter.limit("5 per minute")
def start_game(difficulty):
    sequence, err = fetch_random_sequence(difficulty)
    if err:
        return error_response(err, 400 if "Invalid difficulty" in err else 500)

    game_id = str(uuid.uuid4())
    game_states[game_id] = {
        "solution": sequence,
        "attempts_left": 10,
        "status": "ongoing"
    }

    return success_response({
        "game_id": game_id,
        "length": len(sequence)
    })
        

@game_routes.route("/guess", methods=["POST"])
def make_guess():
    try:
        request_json = request.get_json()
        
        # Validations
        if not request_json or "game_id" not in request_json or "guess" not in request_json:
            return error_response("Invalid request format.", 400)
        
        game_id = request_json["game_id"]
        
        if game_id not in game_states:
            return error_response("Game ID not found.", 404)
        
        guess = request_json["guess"]
        current_game = game_states[game_id]
        sequence = current_game["solution"]
        attempts_left = current_game["attempts_left"]
        status = current_game["status"]
        
        if status in ["win", "lose"]:
            return error_response("This game has already ended.", 400)
        
        if not isinstance(guess, str) or len(guess) != len(sequence) or not guess.isdigit():
            return error_response(f"Guess must be a {len(sequence)}-digit string.", 400)
         
        hints = get_hint(sequence, guess)
        
        correct_positions, correct_numbers_only = hints 
        attempts_left -= 1

        # Check if all of the positions and numbers are correct!
        if correct_positions == len(sequence):
            current_game["status"] = "win"
            current_game["attempts_left"] = attempts_left
            return success_response({
                        "correct_positions": correct_positions,
                        "correct_numbers_only": correct_numbers_only,
                        "attempts_left": attempts_left,
                        "status": "win"  # could be "win", "lose", or "ongoing"
                    })
            
        # If not all but guess attempts_left is 0 then you lose!
        if correct_positions != len(sequence) and attempts_left == 0:
            current_game["status"] = "lose"
            current_game["attempts_left"] = attempts_left
            return success_response({
                        "correct_positions": correct_positions,
                        "correct_numbers_only": correct_numbers_only,
                        "attempts_left": attempts_left,
                        "status": "lose"  # could be "win", "lose", or "ongoing"
                    })
                
        
        # The game is yet to finish
        current_game["attempts_left"] = attempts_left
        
        return success_response({
                    "correct_positions": correct_positions,
                    "correct_numbers_only": correct_numbers_only,
                    "attempts_left": attempts_left,
                    "status": "ongoing"  # could be "win", "lose", or "ongoing"
                })
            
        
    except Exception as error:
        return error_response(str(error), 500)