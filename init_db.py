import sys
import os
from flask import Flask
from sqlalchemy import create_engine, text
from app import db, create_app
from app.models.project import SkillType, ProjectApplication
from app.models.user import User

# 创建neon数据库
def create_database():
    try:
        # 连接MySQL服务器（不指定数据库）
        engine = create_engine('mysql://root:123456@localhost')
        
        # 创建数据库
        with engine.connect() as conn:
            conn.execute(text("CREATE DATABASE IF NOT EXISTS neon DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print("数据库'neon'创建成功或已存在")
    except Exception as e:
        print(f"创建数据库失败，错误: {str(e)}")
        sys.exit(1)

# 创建Flask应用
app = create_app()

# 初始技能类型数据
initial_skill_types = [
    {
        "name": "Software Development",
        "description": "Develop various software applications, including desktop and server applications"
    },
    {
        "name": "Web Development",
        "description": "Develop various website applications, including frontend and backend development"
    },
    {
        "name": "Mobile App Development",
        "description": "Develop applications for mobile platforms like iOS and Android"
    },
    {
        "name": "AI/Machine Learning Development",
        "description": "Develop artificial intelligence and machine learning related algorithms, models and applications"
    },
    {
        "name": "UI/UX Design",
        "description": "Design user interfaces and user experiences to improve product usability"
    },
    {
        "name": "Graphic Design",
        "description": "Design various visual content, including logos, posters, etc."
    },
    {
        "name": "Marketing",
        "description": "Responsible for product promotion, market analysis and user growth"
    },
    {
        "name": "Content Creation",
        "description": "Create various types of content, including copy, video, audio, etc."
    },
    {
        "name": "Project Management",
        "description": "Responsible for project planning, execution, monitoring and closing"
    },
    {
        "name": "Data Analysis",
        "description": "Analyze various data, provide data insights and decision support"
    },
    {
        "name": "Finance/Accounting",
        "description": "Responsible for financial planning, fund management and accounting"
    }
]

# 初始用户数据
initial_users = [
    {
        "email": "admin@thehive.com",
        "full_name": "系统管理员",
        "gender": "男",
        "skills": "项目管理, 系统管理",
        "interests": "技术, 管理",
        "major": "计算机科学",
        "picture": "https://s.gravatar.com/avatar/5d920db6767f734055bbcc817733c827?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fa.png",
        "user_id": "auth0|admin123456789"
    },
    {
        "email": "test@thehive.com",
        "full_name": "测试用户",
        "gender": "女",
        "skills": "软件测试, 质量保证",
        "interests": "测试, 质量",
        "major": "软件工程",
        "picture": "https://s.gravatar.com/avatar/6d920db6767f734055bbcc817733c828?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Ft.png",
        "user_id": "auth0|test123456789"
    }
]

def init_db():
    """初始化数据库"""
    # 先创建数据库
    create_database()
    
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("数据库表创建完成")
        
        # 添加初始数据
        add_initial_data()
        print("初始数据添加完成")
        
def add_initial_data():
    """添加初始数据"""
    with app.app_context():
        # 添加技能类型
        add_skill_types()
        
        # 添加用户
        add_users()

def add_skill_types():
    """添加技能类型数据"""
    with app.app_context():
        for skill_data in initial_skill_types:
            # 检查是否已存在
            existing = SkillType.query.filter_by(name=skill_data['name']).first()
            if not existing:
                skill = SkillType(
                    name=skill_data['name'],
                    description=skill_data['description']
                )
                db.session.add(skill)
        
        # 提交事务
        db.session.commit()
        print(f"已添加 {len(initial_skill_types)} 个技能类型")

def add_users():
    """添加用户数据"""
    with app.app_context():
        for user_data in initial_users:
            # 检查是否已存在
            existing = User.query.filter_by(email=user_data['email']).first()
            if not existing:
                user = User(
                    email=user_data['email'],
                    full_name=user_data.get('full_name'),
                    gender=user_data.get('gender'),
                    mbti=user_data.get('mbti'),
                    star_sign=user_data.get('star_sign'),
                    skills=user_data.get('skills'),
                    interests=user_data.get('interests'),
                    year_of_study=user_data.get('year_of_study'),
                    major=user_data.get('major'),
                    picture=user_data.get('picture'),
                    user_id=user_data.get('user_id')
                )
                db.session.add(user)
        
        # 提交事务
        db.session.commit()
        print(f"已添加 {len(initial_users)} 个用户")

if __name__ == "__main__":
    init_db()
    print("数据库初始化完成") 