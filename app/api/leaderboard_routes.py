from flask import Blueprint
from app import db, r
from app.models.user import User
from app.models.game import Game
from app.models.match_record import MatchRecord
from app.utils.responses import success_response, error_response
from sqlalchemy import desc
from sqlalchemy.sql import functions

leaderboard_routes = Blueprint('leaderboard', __name__)

# /score: shows top 10 users by best average or total score
# Goal: Show rankings in DES order as ranking | player | score (Similar to how Mobile Legends does it)
# MatchRecord table has score
# User table has name/player
# The ranking is simply the index at which this rank is located + 1(since indexes are 0-based)
# There is no connection between the user_id and the match_records so we need help from Games

"""
SELECT users.name, SUM(match_records.score) as total_score https://stackoverflow.com/questions/11830980/sqlalchemy-simple-example-of-sum-average-min-max
FROM games
INNER JOIN match_records ON match_records.game_id = games.id
INNER JOIN users ON games.user_id = users.id
GROUP BY users.name
ORDER BY SUM(match_records.score) DESC https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending
LIMIT 10;
"""
@leaderboard_routes.route('/score', methods=['GET'])
def leaderboard_score():
    # Checking the redis cache first
    top_10 = r.zrevrange("leaderboard_scores", 0, 9, withscores=True)
    if len(top_10) == 0:
        results = db.session.query(
            User.name,
            functions.sum(MatchRecord.score).label("total_score")
        ).join(Game, Game.user_id == User.id)\
        .join(MatchRecord, MatchRecord.game_id == Game.id)\
        .group_by(User.name)\
        .order_by(desc("total_score"))\
        .limit(10).all()

        data = []
        for r_ in results:
            data.append({
                "name": r_.name,
                "total_score": r_.total_score
            })
            
        for d in data:
            r.zadd("leaderboard_scores", {d["name"]: d["total_score"]})
    else:
        data = []
        for name, score in top_10:
            # error: TypeError: Object of type bytes is not JSON serializable
            # solution: https://stackoverflow.com/questions/44682018/typeerror-object-of-type-bytes-is-not-json-serializable
            data.append({
                "name": name.decode("utf-8"),
                "total_score": int(score)
            })
    return success_response(data)

# /games: shows top 10 users by number of games played
# GOAL: Show players with the most number of games played
# User table has the name
# Games has a user_id that we can use to GROUP BY based on the number of games associated with a user_id
"""
SELECT users.name, COUNT(games) as total_games
FROM games
INNER JOIN users ON users.id = games.user_id
GROUP BY users.name
ORDER BY COUNT(games) DESC
LIMIT 10
"""
@leaderboard_routes.route("/games", methods=["GET"])
def leaderboard_games():
    results = db.session.query(
       User.name,
       functions.count(Game.id).label("total_games") 
    ).join(User, User.id == Game.user_id)\
     .group_by(User.name)\
     .order_by(desc("total_games"))\
     .limit(10).all()
     
    data = []
    for r in results:
        data.append({
            "name": r.name,
            "total_games": r.total_games
        })
        
    return success_response(data)