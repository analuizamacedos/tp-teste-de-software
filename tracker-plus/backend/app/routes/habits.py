from flask import Blueprint, request, jsonify
from datetime import date
from app.database import db
from app.models import Habit, HabitLog, Score

habits_bp = Blueprint("habits", __name__)


@habits_bp.route("/habits", methods=["POST"])
def create_habit():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400

    try:
        habit = Habit(
            name=data.get("name"),
            description=data.get("description", "")
        )
        db.session.add(habit)
        db.session.flush()

        score = Score(habit_id=habit.id, points=0)
        db.session.add(score)
        db.session.commit()

        return jsonify(habit.to_dict()), 201

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@habits_bp.route("/habits", methods=["GET"])
def get_habits():
    habits = Habit.query.order_by(Habit.created_at.desc()).all()
    return jsonify([habit.to_dict() for habit in habits]), 200


@habits_bp.route("/habits/<int:habit_id>", methods=["GET"])
def get_habit(habit_id):
    habit = db.session.get(Habit, habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404
    return jsonify(habit.to_dict()), 200


@habits_bp.route("/habits/<int:habit_id>", methods=["PUT"])
def update_habit(habit_id):
    habit = db.session.get(Habit, habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404

    data = request.get_json()
    if "name" in data:
        if not data["name"].strip():
            return jsonify({"error": "Habit name cannot be empty"}), 400
        habit.name = data["name"].strip()
    if "description" in data:
        habit.description = data["description"]

    db.session.commit()
    return jsonify(habit.to_dict()), 200


@habits_bp.route("/habits/<int:habit_id>", methods=["DELETE"])
def delete_habit(habit_id):
    habit = db.session.get(Habit, habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404

    db.session.delete(habit)
    db.session.commit()
    return jsonify({"message": "Habit deleted"}), 200


@habits_bp.route("/habits/<int:habit_id>/complete", methods=["POST"])
def complete_habit(habit_id):
    habit = db.session.get(Habit, habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404

    today = date.today()
    existing_log = HabitLog.query.filter_by(habit_id=habit_id, date=today).first()
    if existing_log:
        return jsonify({"error": "Habit already completed today"}), 409

    log = HabitLog(habit_id=habit_id, date=today, completed=True)
    db.session.add(log)
    db.session.commit()
    return jsonify(log.to_dict()), 201


@habits_bp.route("/habits/<int:habit_id>/logs", methods=["GET"])
def get_logs(habit_id):
    habit = db.session.get(Habit, habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404

    logs = HabitLog.query.filter_by(habit_id=habit_id).all()
    return jsonify([log.to_dict() for log in logs]), 200
