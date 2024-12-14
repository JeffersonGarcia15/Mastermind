from flask import Blueprint
from app import db, r
from app.models.user import User
from app.models.game import Game
from app.models.match_record import MatchRecord
from app.utils.responses import success_response
from sqlalchemy import desc
from sqlalchemy.sql import functions
import logging

leaderboard_routes = Blueprint("leaderboard", __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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


@leaderboard_routes.route("/score", methods=["GET"])
def leaderboard_score():
    # Checking the redis cache first
    top_10 = r.zrevrange("leaderboard_scores", 0, 9, withscores=True)
    if len(top_10) == 0:
        logger.debug("Cache miss for leaderboard_scores: Fetching data from the database.")
        results = (
            db.session.query(
                User.name, functions.sum(MatchRecord.score).label("total_score")
            )
            .join(Game, Game.user_id == User.id)
            .join(MatchRecord, MatchRecord.game_id == Game.id)
            .filter(MatchRecord.score != None)
            .group_by(User.name)
            .order_by(desc("total_score"))
            .limit(10)
            .all()
        )

        data = []
        for r_ in results:
            data.append({"name": r_.name, "total_score": r_.total_score})

        for d in data:
            r.zadd("leaderboard_scores", {d["name"]: d["total_score"]})
        # 5 minutes might be too generous when it comes to deleting the keys to force an update in the cache
        # and avoid the cache becoming stale and becoming out of sync with the db.
        r.expire("leaderboard_scores", 60)
        logger.debug("leaderboard_scores cache updated with fresh data.")
    else:
        logger.debug("Cache hit for leaderboard_scores: Serving data from Redis cache.")
        data = []
        for name, score in top_10:
            # error: TypeError: Object of type bytes is not JSON serializable
            # solution: https://stackoverflow.com/questions/44682018/typeerror-object-of-type-bytes-is-not-json-serializable
            data.append({"name": name.decode("utf-8"), "total_score": int(score)})
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
    top_10 = r.zrevrange("leaderboard_games", 0, 9, withscores=True)
    if len(top_10) == 0:
        logger.debug("Cache miss for leaderboard_games: Fetching data from the database.")
        results = (
            db.session.query(User.name, functions.count(Game.id).label("total_games"))
            .join(User, User.id == Game.user_id)
            .group_by(User.name)
            .order_by(desc("total_games"))
            .limit(10)
            .all()
        )

        data = []
        for r_ in results:
            data.append({"name": r_.name, "total_games": r_.total_games})

        for d in data:
            r.zadd("leaderboard_games", {d["name"]: d["total_games"]})
            #! Set to 60 seconds just so that we don't have to wait 5 minutes for the leaderboard to reflect new changes during the presentation.
        r.expire("leaderboard_games", 60)
        logger.debug("leaderboard_games cache updated with fresh data.")
    else:
        logger.debug("Cache hit for leaderboard_games: Serving data from Redis cache.")
        data = []
        for name, score in top_10:
            data.append({"name": name.decode("utf-8"), "total_score": int(score)})

    return success_response(data)


# For debugging purposes only.
@leaderboard_routes.route("/score/refresh", methods=["POST"])
def refresh_leaderboard_score():
    r.delete("leaderboard_scores")
    return success_response({"message": "Leaderboard cache refreshed."})


# For debugging purposes only.
@leaderboard_routes.route("/games/refresh", methods=["POST"])
def refresh_leaderboard_game():
    r.delete("leaderboard_games")
    return success_response({"message": "Leaderboard cache refreshed."})