from flask import Blueprint
from flask_login import current_user
from app import db
from app.models.game import Game
from app.models.match_record import MatchRecord
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