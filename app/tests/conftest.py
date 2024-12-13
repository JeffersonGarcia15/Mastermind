# https://stackoverflow.com/questions/58660378/how-use-pytest-to-unit-test-sqlalchemy-orm-classes
# https://medium.com/@johnidouglasmarangon/how-to-setup-memory-database-test-with-pytest-and-sqlalchemy-ca2872a92708
from sqlalchemy import create_engine
from flask import Flask
from flask_login import LoginManager, login_user
from ..api.game_routes import game_routes
from ..api.user_routes import auth_routes
from app import db
import pytest
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, scoped_session
import os

# sqlalchemy.exc.NoReferencedTableError: Foreign key associated with column 'games.user_id' could not find table 'users' with which to generate a foreign key to target
# NOTE am I facing this issue because I am not importing the models like I did in __init__.py?
# NOTE yes...
from ..models.user import User
from ..models.game import Game, game_user_id_index
from ..models.attempt import Attempt, attempt_game_id_index
from ..models.match_record import MatchRecord, match_record_score_index

load_dotenv(".env.test")


@pytest.fixture(scope="session")
def db_engine():
    """yields a SQLAlchemy engine, lasts for the duration of the entire test run"""
    DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    engine = create_engine(DATABASE_URI)

    yield engine

    engine.dispose()


@pytest.fixture(scope="session")
def tables(db_engine):
    # beforeAll equivalent in Jest
    db.metadata.create_all(db_engine)
    yield
    # afterAll equivalent in Jest
    db.metadata.drop_all(db_engine)


@pytest.fixture
def db_session(db_engine, tables):
    """Creates a new database session for a test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = scoped_session(Session)

    # https://stackoverflow.com/questions/21078696/why-is-my-scoped-session-raising-an-attributeerror-session-object-has-no-attr
    # db.session = session -> AttributeError: 'Session' object has no attribute 'remove'
    # https://docs.sqlalchemy.org/en/20/orm/contextual.html

    db.session = session

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def app(db_engine, tables):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "super secret key"

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(game_routes, url_prefix="/api/v2/game")
    app.register_blueprint(auth_routes, url_prefix="/api/v2/auth")

    yield app

    # Similar to the afterAll/afterEach in Jest.
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# Centralize this in order to avoid creating this for every user test
@pytest.fixture
def flask_login_fixture(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return login_manager
