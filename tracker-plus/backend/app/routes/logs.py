from datetime import date, datetime

from flask import Blueprint, request, jsonify

from app.database import db
from app.models import Habit, HabitLog, Score
from app.services.scoring import calculate_points
from app.services.streak import calculate_current_streak

logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/habits/<int:habit_id>/complete", methods=["POST"])
def complete_habit(habit_id):
    habit = db.session.get(Habit, habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404

    data = request.get_json(silent=True) or {}
    date_str = data.get("date")
    if date_str:
        try:
            completed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format; use YYYY-MM-DD"}), 400
    else:
        completed_date = date.today()

    existing_log = HabitLog.query.filter_by(habit_id=habit_id, date=completed_date).first()
    if existing_log:
        return jsonify({"error": "Habit already completed for this date"}), 409

    log = HabitLog(habit_id=habit_id, date=completed_date, completed=True)
    db.session.add(log)
    db.session.flush()

    logs = HabitLog.query.filter_by(habit_id=habit_id).all()
    dates = [entry.date for entry in logs]
    current_streak = calculate_current_streak(dates)
    points = calculate_points(current_streak)

    score = Score.query.filter_by(habit_id=habit_id).first()
    if not score:
        score = Score(habit_id=habit_id, points=0)
        db.session.add(score)

    score.points += points
    db.session.commit()

    return jsonify(log.to_dict()), 201


@logs_bp.route("/habits/<int:habit_id>/logs", methods=["GET"])
def get_logs(habit_id):
    habit = db.session.get(Habit, habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404

    logs = HabitLog.query.filter_by(habit_id=habit_id).order_by(HabitLog.date.desc()).all()
    return jsonify([entry.to_dict() for entry in logs]), 200
