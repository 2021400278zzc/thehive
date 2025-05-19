import sys
import os
from flask import Flask
from app import db, create_app
from app.models.project import SkillType

# 创建Flask应用
app = create_app()

# 初始技能类型数据
initial_skill_types = [
    {
        "name": "软件开发",
        "description": "开发各类软件应用，包括桌面应用、服务端应用等"
    },
    {
        "name": "网站开发",
        "description": "开发各类网站应用，包括前端、后端开发等"
    },
    {
        "name": "手机app开发",
        "description": "开发iOS、Android等移动平台的应用程序"
    },
    {
        "name": "AI或机器学习开发",
        "description": "开发人工智能和机器学习相关算法、模型和应用"
    },
    {
        "name": "UI或UX设计",
        "description": "设计用户界面和用户体验，提升产品易用性"
    },
    {
        "name": "平面设计",
        "description": "设计各类平面视觉内容，包括Logo、海报等"
    },
    {
        "name": "市场营销",
        "description": "负责产品推广、市场分析和用户增长等工作"
    },
    {
        "name": "内容创作",
        "description": "创作各类内容，包括文案、视频、音频等"
    },
    {
        "name": "项目管理",
        "description": "负责项目的计划、执行、监控和收尾等管理工作"
    },
    {
        "name": "数据分析",
        "description": "分析各类数据，提供数据洞察和决策支持"
    },
    {
        "name": "金融/会计",
        "description": "负责财务规划、资金管理和会计核算等工作"
    }
]

def init_db():
    """初始化数据库"""
    with app.app_context():
        # 创建neon数据库
        try:
            db.session.execute(db.text("CREATE DATABASE IF NOT EXISTS neon DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print("neon数据库创建成功或已存在")
            
            # 切换到neon数据库
            db.session.execute(db.text("USE neon"))
            print("已切换到neon数据库")
            
            # 创建所有表
            db.create_all()
            print("数据库表创建完成")
            
            # 添加初始数据
            add_initial_data()
            print("初始数据添加完成")
        except Exception as e:
            print(f"初始化数据库失败: {str(e)}")
        
def add_initial_data():
    """添加初始数据"""
    with app.app_context():
        # 添加技能类型
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

if __name__ == "__main__":
    init_db()
    print("数据库初始化完成") 