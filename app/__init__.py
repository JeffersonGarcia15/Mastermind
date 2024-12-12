from flask import Flask
from .rate_limiter import limiter, cors
from .utils.responses import error_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app():
    """Factory function to create a Flask app instance."""
    # https://flask.palletsprojects.com/en/stable/tutorial/factory/
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cors.init_app(app)
    login.init_app(app)

    # Added this because I wanted to follow the convention of /api/*
    from .api.game_routes import game_routes
    from .api.user_routes import auth_routes
    # We should have different versions of API if we're making any changes to them that may break clients. The versioning can be done according to semantic version (for example, 2.0.6 to indicate major version 2 and the sixth patch) like most apps do nowadays.
    # Credits to: https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/
    # Since the way we return data will change, this will for sure break many clients.
    app.register_blueprint(game_routes, url_prefix="/api/v2/game")
    app.register_blueprint(auth_routes, url_prefix="/api/v2/auth")
    
    # My tables were not being created unless I imported the models
    from .models.user import User
    from .models.game import Game, game_user_id_index
    from .models.attempt import Attempt, attempt_game_id_index
    from .models.match_record import MatchRecord, match_record_score_index
    
    # Error: Exception: Missing user_loader or request_loader. Refer to http://flask-login.readthedocs.io/#how-it-works for more info.
    # Solution and credits to: https://medium.com/@zahmed333/solving-the-missing-user-loader-error-with-flask-login-daa1ab4efffb#:~:text=Exception%3A%20Missing%20user_loader%20or%20request_loader,registered%20with%20the%20LoginManager%20instance.
    @login.user_loader
    def load_user(user_id):
        # Return the user object for the given user_id
        return User.query.get(int(user_id))
    
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
