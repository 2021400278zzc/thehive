from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
# 创建数据库实例
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/neon'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化插件
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # 注册蓝图
    from app.controllers.project_controller import project_bp
    from app.controllers.user_controller import user_bp
    
    app.register_blueprint(project_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    
    return app 