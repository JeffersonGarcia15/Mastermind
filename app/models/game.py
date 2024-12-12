from app import db
import datetime
import uuid
import enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Index

class Difficulty(enum.Enum):
    medium = "medium"
    hard = "hard"

class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    difficulty = db.Column(db.Enum(Difficulty), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    solution = db.Column(db.String(10), nullable=False)
    fallback_used = db.Column(db.Boolean, default=False, nullable=False)
    
    attempts = db.relationship("Attempt", backref="game", lazy=True)
    match_record = db.relationship("MatchRecord", backref="game", uselist=False)

    def to_dict(self, reveal_solution=False):
        """Convert the Game object into a dictionary for JSON responses."""
        data = {
            "game_id": str(self.id),
            "difficulty": self.difficulty.value,
            "created_at": self.created_at.isoformat(),
            "is_sequence_locally_generated": self.fallback_used,
            "attempts_left": 10 - len(self.attempts)
        }
        if reveal_solution or (self.match_record and self.match_record.result in ["win", "lose"]):
            data["solution"] = self.solution
        return data
game_user_id_index = Index("game_user_id_index", Game.user_id)