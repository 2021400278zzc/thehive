from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import text
import os

# 创建数据库实例
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # 配置数据库 - 使用MySQLdb驱动
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/neon'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 配置静态文件
    app.config['STATIC_FOLDER'] = 'static'
    app.config['STATIC_URL_PATH'] = '/api/static'
    
    # 确保静态文件目录存在
    os.makedirs(os.path.join(app.root_path, 'static', 'deliverables'), exist_ok=True)
    
    # 初始化插件
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # 创建API蓝图
    api_bp = Blueprint('api', __name__)
    
    @api_bp.route('/')
    def index():
        return "TheHive API 服务正常运行"
    
    @api_bp.route('/health')
    def health_check():
        """健康检查端点"""
        try:
            # 检查数据库连接
            db.session.execute(text('SELECT 1'))
            return {"status": "healthy", "database": "connected"}, 200
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}, 500
    
    # 注册蓝图
    from app.controllers.project_controller import project_bp
    from app.controllers.user_controller import user_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(project_bp)
    app.register_blueprint(user_bp)
    
    return app 