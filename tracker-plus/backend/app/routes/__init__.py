from flask import request, jsonify
from datetime import date
from app.database import db
from app.models import Habit, HabitLog


def register_routes(app):

    @app.route("/habits", methods=["POST"])
    def create_habit():
        data = request.get_json()

        try:
            habit = Habit(
                name=data.get("name"),
                description=data.get("description", "")
            )

            db.session.add(habit)
            db.session.commit()

            return jsonify(habit.to_dict()), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/habits", methods=["GET"])
    def get_habits():
        habits = Habit.query.all()
        return jsonify([habit.to_dict() for habit in habits]), 200

    @app.route("/habits/<int:habit_id>", methods=["GET"])
    def get_habit(habit_id):
        habit = db.session.get(Habit, habit_id)

        if not habit:
            return jsonify({"error": "Habit not found"}), 404

        return jsonify(habit.to_dict()), 200

    @app.route("/habits/<int:habit_id>", methods=["PUT"])
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

    @app.route("/habits/<int:habit_id>", methods=["DELETE"])
    def delete_habit(habit_id):
        habit = db.session.get(Habit, habit_id)

        if not habit:
            return jsonify({"error": "Habit not found"}), 404

        db.session.delete(habit)
        db.session.commit()

        return jsonify({"message": "Habit deleted successfully"}), 200
    
    @app.route("/habits/<int:habit_id>/complete", methods=["POST"])
    def complete_habit(habit_id):

        habit = db.session.get(Habit, habit_id)

        if not habit:
            return jsonify({"error": "Habit not found"}), 404

        today = date.today()

        existing_log = HabitLog.query.filter_by(
            habit_id=habit_id,
            date=today
        ).first()

        if existing_log:
            return jsonify({
                "error": "Habit already completed today"
            }), 400

        log = HabitLog(
            habit_id=habit_id,
            date=today,
            completed=True
        )

        db.session.add(log)
        db.session.commit()

        return jsonify(log.to_dict()), 201


    @app.route("/habits/<int:habit_id>/logs", methods=["GET"])
    def get_logs(habit_id):

        habit = db.session.get(Habit, habit_id)

        if not habit:
            return jsonify({"error": "Habit not found"}), 404

        logs = HabitLog.query.filter_by(
            habit_id=habit_id
        ).all()

        return jsonify(
            [log.to_dict() for log in logs]
        ), 200