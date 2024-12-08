from flask import Flask
from flask_cors import CORS

from .api.game_routes import game_routes
from .rate_limiter import limiter
from .utils.responses import error_response

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

# As per the docs: For example, an error handler for HTTPException might be useful for turning the default HTML errors pages into JSON.
# https://flask.palletsprojects.com/en/stable/errorhandling/
@app.errorhandler(429)
def ratelimit_handler(error):
    return error_response("Rate limit exceeded: 5 per minute.", 429)    


@app.route("/")
def hello_world():
    return "<p>Hello, World!!</p>"