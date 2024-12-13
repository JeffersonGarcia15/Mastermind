from flask import Blueprint, request, session
from flask_login import current_user, login_user, logout_user
from app.models.user import User
from app import db
from app.utils.responses import success_response, error_response

auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/")
def authenticate():
    """
    Checks if a user is currently authenticated.
    If yes, returns user data; if not, returns an error.
    """
    if current_user.is_authenticated:
        return success_response(current_user.to_dict())
    return error_response("Unauthorized", 401)


@auth_routes.route("/login", methods=["POST"])
def login():
    """
    Logs a user in using username and password.
    Expects JSON: { "username": "theusername", "password": "thepassword" }
    """
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return error_response("Missing username or password.", 400)

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(name=username).first()
    if not user or not user.check_password(password):
        return error_response("Invalid username or password.", 401)

    login_user(user)
    session.permanent = True
    return success_response(user.to_dict(), 200)


@auth_routes.route("/logout", methods=["POST"])
def logout():
    """
    Logs a user out.
    """
    if not current_user.is_authenticated:
        return error_response("User not logged in.", 400)
    logout_user()
    return success_response({"message": "User logged out"}, 200)


@auth_routes.route("/signup", methods=["POST"])
def sign_up():
    """
    Creates a new user and logs them in.
    Expects JSON: { "username": "theusername", "password": "thepassword" }
    """
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return error_response("Missing username or password.", 400)

    username = data["username"]
    password = data["password"]

    # Check for existing username or email
    existing_user = User.query.filter_by(name=username).first()
    if existing_user:
        return error_response("Username already exists.", 400)

    new_user = User(
        name=username,
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    session.permanent = True
    return success_response(new_user.to_dict(), 201)
