from flask import Blueprint, request

# https://flask-limiter.readthedocs.io/en/stable/
import requests
from flask_login import current_user
from ..rate_limiter import limiter
from ..utils.responses import success_response, error_response
from ..utils.generate_local_sequence import generate_local_sequence
from ..models.game import Game, Difficulty
from ..models.attempt import Attempt
from ..models.match_record import MatchRecord, Result
from app import db

from ..utils.get_hint import get_hint

BASE_URL_MEDIUM = "https://www.random.org/integers/?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new"
BASE_URL_HARD = "https://www.random.org/integers/?num=6&min=0&max=7&col=1&base=10&format=plain&rnd=new"
ALLOWED_DIFFICULTIES = ["medium", "hard"]

game_routes = Blueprint("game", __name__)


def fetch_random_sequence(difficulty):
    """Fetches a random sequence from Random.org based on difficulty.
    Falls back to local generation if the API fails"""
    if difficulty not in ALLOWED_DIFFICULTIES:
        # Early return if invalid difficulty
        return None, False, "Invalid difficulty level."

    # Select the appropriate URL based on difficulty
    url = BASE_URL_MEDIUM if difficulty == "medium" else BASE_URL_HARD

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.text.split()

        expected_length = 4 if difficulty == "medium" else 6
        if len(data) != expected_length or any(not line.isdigit() for line in data):
            return (
                None,
                False,
                "Invalid data received from the random number generator.",
            )

        sequence = "".join(data)
        return sequence, False, None
    except requests.exceptions.RequestException as error:
        print(error)
        response = generate_local_sequence(4 if difficulty == "medium" else 6)
        data = response.split()
        sequence = "".join(data)
        return sequence, True, "Random.org API failed. Generated sequence locally."


# 5 games per minute per IP address
# https://medium.com/analytics-vidhya/how-to-rate-limit-routes-in-flask-61c6c791961b#:~:text=In%20flask%20there%20is%20a,track%20of%20their%20IP%20address.
@game_routes.route("/start", methods=["POST"])
@limiter.limit("5 per minute")
def start_game():
    request_json = request.get_json()

    if not request_json or "difficulty" not in request_json:
        return error_response("Invalid request format.", 400)

    difficulty = request_json["difficulty"]
    sequence, fallback_used, err = fetch_random_sequence(difficulty)

    if err and not fallback_used:
        return error_response(err, 400)

    # Check if there is a user logged_in and if that's the case then we can store that in the Game table
    user_id = current_user.id if current_user.is_authenticated else None

    # https://docs.sqlalchemy.org/en/20/orm/quickstart.html#create-objects-and-persist

    game = Game(
        user_id=user_id,
        difficulty=Difficulty(difficulty),
        solution=sequence,
        fallback_used=fallback_used,
    )
    db.session.add(game)
    db.session.commit()

    response_data = {
        "game_id": str(game.id),
        "length": len(sequence),
        "is_sequence_locally_generated": fallback_used,
    }

    return success_response(response_data)


@game_routes.route("/guess", methods=["POST"])
def make_guess():
    try:
        request_json = request.get_json()

        # Validations
        if (
            not request_json
            or "game_id" not in request_json
            or "guess" not in request_json
        ):
            return error_response("Invalid request format.", 400)

        game_id = request_json["game_id"]
        guess = request_json["guess"]

        game = Game.query.filter_by(id=game_id).first()
        if not game:
            return error_response("Game ID not found.", 404)
        sequence = game.solution
        match_record_data = MatchRecord.query.filter_by(game_id=game.id).first()
        status = None
        if match_record_data:
            status = match_record_data.result

        if status and status.value in ["win", "lose"]:
            return error_response("This game has already ended.", 400)

        if (
            not isinstance(guess, str)
            or len(guess) != len(sequence)
            or not guess.isdigit()
        ):
            return error_response(f"Guess must be a {len(sequence)}-digit string.", 400)

        attempts_made = Attempt.query.filter_by(game_id=game_id).count()

        # Changing the logic so that guessing in the last attempt does not give you 0 points
        if attempts_made >= 10:
            return error_response("No attempts left. Game over.", 400)

        # Proceed to add the new attempt
        hints = get_hint(sequence, guess)
        correct_positions, correct_numbers_only = hints

        attempt = Attempt(
            game_id=game.id,
            guess=guess,
            hints=f"{correct_positions} correct positions, {correct_numbers_only} correct numbers",
        )
        db.session.add(attempt)
        db.session.commit()

        attempts_made += 1
        attempts_left = 10 - attempts_made

        response_data = {
            "correct_positions": correct_positions,
            "correct_numbers_only": correct_numbers_only,
            "attempts_left": attempts_left,
            "status": "ongoing",
        }

        # # Check if all of the positions and numbers are correct!
        if correct_positions == len(sequence):
            response_data["status"] = "win"
            response_data["solution"] = sequence
            # Ensure at least 1 point for medium difficulty
            if game.difficulty.value == "hard":
                score = attempts_left + 5
            else:
                score = max(attempts_left, 1)
            match_record = MatchRecord(
                game_id=game.id,
                result=Result.win,
                score=score,
            )
            db.session.add(match_record)
            db.session.commit()
            return success_response(response_data)

        # If not all but guess attempts_left is 0 then you lose!
        if attempts_left == 0:
            response_data["status"] = "lose"
            response_data["solution"] = sequence
            match_record = MatchRecord(game_id=game.id, result=Result.lose, score=0)
            db.session.add(match_record)
            db.session.commit()
            return success_response(response_data)

        return success_response(response_data)

    except Exception as error:
        return error_response(str(error), 500)
