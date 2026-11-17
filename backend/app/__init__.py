from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # 数据库配置（SQLite，文件存在项目目录下）
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diet.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # 全局异常处理
    from app.utils import APIException, APIResponse

    @app.errorhandler(APIException)
    def handle_api_exception(e):
        return APIResponse.error(e.message, e.code)

    @app.errorhandler(404)
    def handle_404(e):
        return APIResponse.error("接口不存在", 404)

    @app.errorhandler(500)
    def handle_500(e):
        return APIResponse.error("服务器内部错误", 500)

    # 注册路由
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # 自动创建数据库表
    with app.app_context():
        db.create_all()

    return app
