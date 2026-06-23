def register_routes(app):
    from .habits import habits_bp
    app.register_blueprint(habits_bp)
