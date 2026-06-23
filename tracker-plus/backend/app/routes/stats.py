from datetime import datetime

from flask import Blueprint, jsonify

from app.database import db
from app.models import Habit, HabitLog, Score
from app.services.streak import calculate_current_streak, calculate_max_streak

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/habits/<int:habit_id>/streak", methods=["GET"])
def get_streak(habit_id):
    habit = db.session.get(Habit, habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404

    logs = HabitLog.query.filter_by(habit_id=habit_id).all()
    dates = [entry.date for entry in logs]
    return jsonify({
        "habit_id": habit_id,
        "current_streak": calculate_current_streak(dates),
        "max_streak": calculate_max_streak(dates),
    }), 200


@stats_bp.route("/habits/<int:habit_id>/score", methods=["GET"])
def get_score(habit_id):
    habit = db.session.get(Habit, habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404

    score = Score.query.filter_by(habit_id=habit_id).first()
    points = score.points if score else 0
    return jsonify({"habit_id": habit_id, "points": points}), 200


@stats_bp.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    habits = Habit.query.join(Score, Score.habit_id == Habit.id).order_by(Score.points.desc()).all()
    leaderboard = []
    for habit in habits:
        score = habit.score
        logs = HabitLog.query.filter_by(habit_id=habit.id).all()
        dates = [entry.date for entry in logs]
        leaderboard.append({
            "habit_id": habit.id,
            "name": habit.name,
            "points": score.points if score else 0,
            "streak": calculate_current_streak(dates),
        })

    return jsonify(leaderboard), 200
