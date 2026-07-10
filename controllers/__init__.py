from .main_controller import main_bp
from .auth_controller import auth_bp


def register_blueprints(app):
    """注册所有蓝图"""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)