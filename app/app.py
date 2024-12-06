from flask import Flask
from flask_cors import CORS

from .api.game_routes import game_routes

app = Flask(__name__)

app.register_blueprint(game_routes, url_prefix="/api/game")

CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!!</p>"