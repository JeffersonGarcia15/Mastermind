from flask import Blueprint
from flask_login import current_user
from app import db
from app.models.game import Game
from app.models.match_record import MatchRecord
from app.models.attempt import Attempt
from flask_login import login_required
from app.utils.responses import success_response, error_response

history_routes = Blueprint('history', __name__)

@history_routes.route('/all_games', methods=['GET'])
@login_required
def get_all_games():
    """
    Returns all games played by the current authenticated user.
    Fields: game_id, difficulty, created_at, final_status (win/lose/ongoing?), score if ended.
    
    Ideally, if you ever leave a game, it should automatically become a lose if you don't select the option to continue your previous game.
    """
    user_id = current_user.id

    games = db.session.query(Game).filter_by(user_id=user_id).all()

    data = []
    for g in games:
        match_record = MatchRecord.query.filter_by(game_id=g.id).first()
        status = "ongoing"
        score = None
        if match_record:
            status = match_record.result.value
            score = match_record.score
        
        data.append({
            "game_id": str(g.id),
            "difficulty": g.difficulty.value,
            "created_at": g.created_at.isoformat(),
            "status": status,
            "score": score
        })

    return success_response(data)

@history_routes.route('/game_details/<string:game_id>', methods=['GET'])
@login_required
def get_game_details(game_id):
    user_id = current_user.id
    game = Game.query.filter_by(id=game_id).first()
    if not game:
        return error_response("Game not found.", 404)

    attempts = Attempt.query.filter_by(game_id=game.id).all()
    attempts_data = []
    for a in attempts:
        # Example hints format: "2 correct positions, 1 correct number"
        parts = a.hints.split(',') # ["2 correct positions", " 1 correct number"]
        # parts[0] -> "2 correct positions"
        # parts[1] -> " 1 correct number"
        correct_positions_string = parts[0].split()
        correct_numbers_only_string = parts[1].split()
        correct_positions = int(correct_positions_string[0])
        correct_numbers_only = int(correct_numbers_only_string[0])
        
        attempts_data.append({
            "guess": a.guess,
            "hints": a.hints,
            "correct_positions": correct_positions,
            "correct_numbers_only": correct_numbers_only
        })

    match_record = MatchRecord.query.filter_by(game_id=game.id).first()
    status = "ongoing"
    score = None
    solution = None
    if match_record:
        status = match_record.result.value
        score = match_record.score
        solution = game.solution
        
    data = {
            "game_id": str(game.id),
            "difficulty": game.difficulty.value,
            "created_at": game.created_at.isoformat(),
            "status": status,
            "score": score,
            "solution": solution,
            "attempts": attempts_data
        }

    return success_response(data)
