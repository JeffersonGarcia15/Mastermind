from flask import Flask
from flask_cors import CORS

from .api.game_routes import game_routes
from .rate_limiter import limiter

app = Flask(__name__)

"""
ImportError: cannot import name 'limiter' from partially initialized module 'app.app' 
(most likely due to a circular import)
"""
# https://flask-limiter.readthedocs.io/en/stable/configuration.html#ratelimit-string
# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=["200 per day", "50 per hour"]
# )

limiter.init_app(app)
app.register_blueprint(game_routes, url_prefix="/api/game")

CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!!</p>"