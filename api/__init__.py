import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv

# 创建数据库实例
db = SQLAlchemy()
load_dotenv()


def create_app():
    app = Flask(__name__)

    # 配置数据库
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SERVICE_DB_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 初始化插件
    db.init_app(app)

    with app.app_context():
        db.create_all()

    CORS(app)

    # 注册蓝图
    from api.controllers.project_controller import project_bp
    from api.controllers.user_controller import user_bp

    app.register_blueprint(project_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")

    return app
