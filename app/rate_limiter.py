from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# https://flask-limiter.readthedocs.io/en/stable/configuration.html#ratelimit-string
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)