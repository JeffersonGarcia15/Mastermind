from app import db
import datetime
import uuid
import enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Index

class Difficulty(enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    difficulty = db.Column(db.Enum(Difficulty), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    
game_user_id_index = Index("game_user_id_index", Game.user_id)