from app import db
import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Index

class Attempt(db.Model):
    __tablename__ = "attempts"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(UUID(as_uuid=True), db.ForeignKey("games.id"))
    guess = db.Column(db.String(10), nullable=False)
    hints = db.Column(db.String(10), nullable=False)
    time = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    

    def to_dict(self):
        """Convert the Attempt object into a dictionary."""
        return {
            "id": self.id,
            "game_id": str(self.game_id),
            "guess": self.guess,
            "hints": self.hints,
            "time": self.time.isoformat()
        }
# Since I forgot to add index=true when creating the db, I will add them separately to avoid dropping the db
attempt_game_id_index = Index("attempt_game_id_index", Attempt.game_id)