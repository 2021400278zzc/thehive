from app import create_app, db
from app.models.project import Project, SkillRequirement, SkillType
from flask_migrate import Migrate
from sqlalchemy import create_engine, text

app = create_app()
migrate = Migrate(app, db)

@app.cli.command("init-db")
def init_db():
    """初始化数据库"""
    # 先创建数据库
    try:
        # 连接MySQL服务器（不指定数据库）
        engine = create_engine('mysql://root:123456@localhost')
        
        # 创建数据库
        with engine.connect() as conn:
            conn.execute(text("CREATE DATABASE IF NOT EXISTS neon DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print("数据库'neon'创建成功或已存在")
    except Exception as e:
        print(f"创建数据库失败: {str(e)}")
        return
    
    # 然后创建表并初始化数据
    db.create_all()
    print("数据库表创建完成")
    
    # 从init_db.py导入并添加初始数据
    try:
        from init_db import add_initial_data
        add_initial_data()
        print("初始数据添加完成")
    except Exception as e:
        print(f"添加初始数据失败: {str(e)}")

@app.route('/')
def index():
    return "TheHive API 服务正常运行"

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0') 