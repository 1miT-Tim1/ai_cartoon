from flask import Flask
from flask_login import LoginManager
from config import config_map
from models import db, User
from controllers import register_blueprints

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录后再访问此页面。'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_name=None):
    """应用工厂函数"""
    if config_name is None:
        config_name = 'default'

    app = Flask(__name__)
    app.config.from_object(config_map[config_name])

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)

    # 注册蓝图（控制器）
    register_blueprints(app)

    # 创建数据库表
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)