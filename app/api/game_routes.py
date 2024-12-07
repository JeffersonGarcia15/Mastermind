from flask import Blueprint, request
import requests
import uuid

from ..utils.get_hint import get_hint

BASE_URL = "https://www.random.org/integers/?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new"

game_routes = Blueprint("game", __name__)

game_states = {}

@game_routes.route("/start")
def start_game():
    try:
        response = requests.get(BASE_URL)
        # As per the docs: Response.raise_for_status() will raise an HTTPError if the HTTP request returned an unsuccessful status code.
        response.raise_for_status()
        # content-type: text/plain;charset=UTF-8 so since it is not JSON we use .text
        data = response.text.split()
        
        sequence = "".join(data)
        id = str(uuid.uuid4())
        game_states[id] = {
            "solution": sequence,
            "attempts_left": 10
        }
        
        print("GAME STATES", game_states)
    

        return {
            "data": [
                {   
                    "game_id": id,
                }
            ],
            "error": None
        }
    except requests.exceptions.RequestException as error:
        return {
            "data": [],
            "error": str(error)
        }
        

@game_routes.route("/guess", methods=["POST"])
def make_guess():
    try:
        request_json = request.get_json()
        current_game = game_states[request_json["game_id"]]
        sequence = current_game["solution"]
        attempts_left = current_game["attempts_left"]
        
        guess = request_json["guess"]
        hints = get_hint(sequence, guess)
        
        correct_positions, correct_numbers_only = hints 
        attempts_left -= 1
        
        print("THE HINTS", hints)

        # Check if all of the positions and numbers are correct!
        if correct_positions == len(sequence):
            return {
                "data": [
                    {
                        "correct_positions": correct_positions,
                        "correct_numbers_only": correct_numbers_only,
                        "attempts_left": attempts_left,
                        "status": "win"  # could be "win", "lose", or "ongoing"
                    }
                ],
                "error": None
            }
            
        # If not all but guess attempts_left is 0 then you lose!
        if correct_positions != len(sequence) and attempts_left == 0:
            return {
                "data": [
                    {
                        "correct_positions": correct_positions,
                        "correct_numbers_only": correct_numbers_only,
                        "attempts_left": attempts_left,
                        "status": "lose"  # could be "win", "lose", or "ongoing"
                    }
                ],
                "error": None
            }
        
        # The game is yet to finish
        current_game["attempts_left"] = attempts_left
        
        return {
            "data": [
                {
                    "correct_positions": correct_positions,
                    "correct_numbers_only": correct_numbers_only,
                    "attempts_left": attempts_left,
                    "status": "ongoing"  # could be "win", "lose", or "ongoing"
                }
            ],
            "error": None
        }
        
    except requests.exceptions.RequestException as error:
        return {
            "data": [],
            "error": str(error)
        }