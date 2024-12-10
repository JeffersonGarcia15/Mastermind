from flask import Flask
from .rate_limiter import limiter, cors
from .utils.responses import error_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Factory function to create a Flask app instance."""
    # https://flask.palletsprojects.com/en/stable/tutorial/factory/
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cors.init_app(app)

    # Added this because I wanted to follow the convention of /api/*
    from .api.game_routes import game_routes
    app.register_blueprint(game_routes, url_prefix="/api/game")
    
    # My tables were not being created unless I imported the models
    from .models.user import User
    from .models.game import Game, game_user_id_index
    from .models.attempt import Attempt, attempt_game_id_index
    from .models.match_record import MatchRecord, match_record_score_index
    
    # As per the docs: For example, an error handler for HTTPException might be useful for turning the default HTML errors pages into JSON.
    # https://flask.palletsprojects.com/en/stable/errorhandling/
    @app.errorhandler(429)
    def ratelimit_handler(error):
        return error_response("Rate limit exceeded: 5 per minute.", 429)    

    @app.cli.command("create-db")
    def create_db():
        with app.app_context():
            # As per the docs: After all models and tables are defined, call SQLAlchemy.create_all() to create the table schema in the database. 
            db.create_all()
            print("Database created successfully!")

    # https://stackoverflow.com/questions/14419299/adding-indexes-to-sqlalchemy-models-after-table-creation
    # https://www.opcito.com/blogs/a-guide-to-postgresql-indexing-with-sqlalchemy
    # Create a CLI command to create indexes
    @app.cli.command("create-indexes")
    def create_indexes():
        with app.app_context():
            engine = db.get_engine(app=app)
            
            # Create the indexes
            attempt_game_id_index.create(bind=engine)
            game_user_id_index.create(bind=engine)
            match_record_score_index.create(bind=engine)

            print("LOG: Indexes created successfully!")
            
    return app
