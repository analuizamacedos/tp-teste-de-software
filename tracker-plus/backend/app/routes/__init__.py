def register_routes(app):
    from .habits import habits_bp
    from .logs import logs_bp
    from .stats import stats_bp

    app.register_blueprint(habits_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(stats_bp)
