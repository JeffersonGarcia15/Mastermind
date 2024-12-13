from app import db
import enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Index


class Result(enum.Enum):
    win = "win"
    lose = "lose"


class MatchRecord(db.Model):
    __tablename__ = "match_records"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(UUID(as_uuid=True), db.ForeignKey("games.id"))
    result = db.Column(db.Enum(Result), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Interval, nullable=True)

    def to_dict(self):
        """Convert the MatchRecord object into a dictionary."""
        return {
            "id": self.id,
            "game_id": str(self.game_id),
            "result": self.result.value,
            "score": self.score,
            "time_taken": str(self.time_taken),
        }


match_record_score_index = Index("match_record_score_index", MatchRecord.score)
