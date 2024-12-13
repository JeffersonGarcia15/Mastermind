import redis
from flask import Flask
from .rate_limiter import limiter, cors
from .utils.responses import error_response
from .utils.generate_local_sequence import generate_local_sequence
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import os
import click
import random
import datetime

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
# Credits to: https://pypi.org/project/redis/
# The docs mention localhost but given that redis is on Docker we need to reference that service
r = redis.Redis(host="redis", port=6379, db=0)

def create_app():
    """Factory function to create a Flask app instance."""
    # https://flask.palletsprojects.com/en/stable/tutorial/factory/
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") 
    app.config["SESSION_TYPE"] = os.getenv("SESSION_TYPE")

    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cors.init_app(app)
    login.init_app(app)

    # Added this because I wanted to follow the convention of /api/*
    from .api.game_routes import game_routes
    from .api.user_routes import auth_routes
    from .api.history_routes import history_routes
    from .api.leaderboard_routes import leaderboard_routes
    # We should have different versions of API if we're making any changes to them that may break clients. The versioning can be done according to semantic version (for example, 2.0.6 to indicate major version 2 and the sixth patch) like most apps do nowadays.
    # Credits to: https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/
    # Since the way we return data will change, this will for sure break many clients.
    app.register_blueprint(game_routes, url_prefix="/api/v2/game")
    app.register_blueprint(auth_routes, url_prefix="/api/v2/auth")
    app.register_blueprint(history_routes, url_prefix="/api/v2/history")
    app.register_blueprint(leaderboard_routes, url_prefix="/api/v2/leaderboard")
    
    # My tables were not being created unless I imported the models
    from .models.user import User
    from .models.game import Game, Difficulty ,game_user_id_index
    from .models.attempt import Attempt, attempt_game_id_index
    from .models.match_record import MatchRecord, Result, match_record_score_index
    
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
    
    @app.cli.command("seed")
    @click.option("--games-per-user", default=None, help="Optional override for games per user.")
    def seed(games_per_user):
        """
        Seed the database with sample data.
        """
        # Clear existing data if needed
        # Reference: https://github.com/JeffersonGarcia15/Astrogram/blob/main/app/seeds/users.py
        
        # Error: sqlalchemy.exc.ArgumentError: Textual SQL expression 'TRUNCATE users CASCADE;' should be explicitly declared as text('TRUNCATE users CASCADE;')
        # Credits to: https://stackoverflow.com/questions/54483184/sqlalchemy-warning-textual-column-expression-should-be-explicitly-declared
        db.session.execute(text("TRUNCATE users RESTART IDENTITY CASCADE;"))
        db.session.execute(text("TRUNCATE games RESTART IDENTITY CASCADE;"))
        db.session.execute(text("TRUNCATE attempts RESTART IDENTITY CASCADE;"))
        db.session.execute(text("TRUNCATE match_records RESTART IDENTITY CASCADE;"))
        db.session.commit()
        click.echo("Database tables truncated successfully.")

        # Create 15 users. This is useful for the Leaderboard feature I will implement if I have the time.
        users = []
        for i in range(15):
            user = User(name=f"user{i+1}")
            user.set_password("password")
            users.append(user)
            db.session.add(user)
        db.session.commit()

        difficulties = [Difficulty.medium, Difficulty.hard]

        # For each user, create (user_id) games if no override, else use the override which is going to use the val from click to specify the number of games per user
        for user in users:
            # Create 1 game for the first user, 2 for user 2, 3 for user 3,... n - 1 for user n - 1...
            num_games = user.id if not games_per_user else games_per_user
            for g in range(num_games):
                difficulty = random.choice(difficulties)
                random_sequence = generate_local_sequence(4 if difficulty.value == "medium" else 6)
                data = random_sequence.split()
                solution = "".join(data)
                game = Game(
                    user_id=user.id,
                    difficulty=difficulty,
                    solution=solution,
                    fallback_used=bool(random.getrandbits(1)),
                    created_at=datetime.datetime.now()
                )
                db.session.add(game)
                db.session.commit()

                # Random number of attempts [0, 10]
                attempts_count = random.randint(0, 10)
                correct_positions = random.randint(0, len(solution))
                correct_numbers_only = random.randint(0, len(solution) - correct_positions)

                # Create attempts
                for a_idx in range(attempts_count):
                    attempt = Attempt(
                        game_id=game.id,
                        guess="".join(str(random.randint(0, 7)) for _ in range(len(solution))),
                        hints=f"{correct_positions} correct positions, {correct_numbers_only} correct numbers"
                    )
                    db.session.add(attempt)

                # Determine if the game ended (if attempts_count reached 10 or all correct)
                if correct_positions == len(solution) or attempts_count == 10:
                    # Game ended, determine result (win if correct_positions == len(solution))
                    result = Result.win if correct_positions == len(solution) else Result.lose
                    score = 10 - attempts_count
                    match_record = MatchRecord(
                        game_id=game.id,
                        result=result,
                        score=score + 5 if difficulty.value == "hard" else score,
                        time_taken=datetime.timedelta(seconds=random.randint(10,300))
                    )
                    db.session.add(match_record)

                db.session.commit()

        print("Seeding completed successfully!")
    
    return app
