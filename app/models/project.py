from app import db
from datetime import datetime

class SkillType(db.Model):
    """技能类型模型"""
    __tablename__ = 'skill_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True, comment='技能类型名称')
    description = db.Column(db.Text, nullable=True, comment='技能类型描述')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Project(db.Model):
    """项目模型"""
    __tablename__ = 'projects'
    
    # 项目状态常量
    STATUS_IN_PROGRESS = 1  # 进行中
    STATUS_COMPLETED = 2    # 已完成
    
    # 招募状态常量
    RECRUITMENT_OPEN = 1    # 开放申请
    RECRUITMENT_CLOSED = 2  # 招募结束
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='项目名称')
    project_type = db.Column(db.String(50), nullable=False, comment='项目类型')
    end_time = db.Column(db.DateTime, nullable=False, comment='项目结束时间')
    description = db.Column(db.Text, nullable=True, comment='项目描述')
    goal = db.Column(db.Text, nullable=True, comment='项目目标')
    status = db.Column(db.Integer, default=STATUS_IN_PROGRESS, comment='项目状态：1-进行中、2-已完成')
    recruitment_status = db.Column(db.Integer, default=RECRUITMENT_OPEN, comment='招募状态：1-开放申请、2-招募结束')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 建立与SkillRequirement的一对多关系
    skill_requirements = db.relationship('SkillRequirement', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'project_type': self.project_type,
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'description': self.description,
            'goal': self.goal,
            'status': self.status,
            'status_text': '进行中' if self.status == self.STATUS_IN_PROGRESS else '已完成',
            'recruitment_status': self.recruitment_status,
            'recruitment_status_text': '开放申请' if self.recruitment_status == self.RECRUITMENT_OPEN else '招募结束',
            'skill_requirements': [skill.to_dict() for skill in self.skill_requirements],
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class SkillRequirement(db.Model):
    """技能需求模型"""
    __tablename__ = 'skill_requirements'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    skill_type_id = db.Column(db.Integer, db.ForeignKey('skill_types.id'), nullable=False)
    required_count = db.Column(db.Integer, nullable=False, comment='所需人数')
    importance = db.Column(db.Integer, nullable=False, comment='重要程度(1-5星)')
    description = db.Column(db.Text, nullable=True, comment='技能描述')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 建立与SkillType的多对一关系
    skill_type = db.relationship('SkillType', backref='skill_requirements')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'skill_type_id': self.skill_type_id,
            'skill_type_name': self.skill_type.name if self.skill_type else None,
            'required_count': self.required_count,
            'importance': self.importance,
            'description': self.description
        } 