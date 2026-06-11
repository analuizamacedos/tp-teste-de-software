from datetime import datetime
from sqlalchemy import UniqueConstraint
from .database import db


class Habit(db.Model):
    __tablename__ = "habit"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300), nullable=True, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    logs = db.relationship("HabitLog", backref="habit", cascade="all, delete-orphan")
    score = db.relationship("Score", backref="habit", cascade="all, delete-orphan", uselist=False)

    def __init__(self, name: str, description: str = ""):
        if not name or not name.strip():
            raise ValueError("Habit name cannot be empty")
        self.name = name.strip()
        self.description = description
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class HabitLog(db.Model):
    __tablename__ = "habit_log"
    __table_args__ = (UniqueConstraint("habit_id", "date"),)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "habit_id": self.habit_id,
            "date": self.date.isoformat(),
            "completed": self.completed,
        }


class Score(db.Model):
    __tablename__ = "score"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    habit_id = db.Column(db.Integer, db.ForeignKey("habit.id"), nullable=False)
    points = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "habit_id": self.habit_id,
            "points": self.points,
        }
