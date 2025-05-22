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
    
    # 创建者Auth0标识，现在添加外键约束
    user_id = db.Column(db.String(100), db.ForeignKey('users.user_id'), nullable=False, comment='创建者Auth0用户标识')
    
    # 建立与SkillRequirement的一对多关系
    skill_requirements = db.relationship('SkillRequirement', backref='project', lazy=True, cascade='all, delete-orphan')
    
    # 建立与ProjectApplication的一对多关系
    applications = db.relationship('ProjectApplication', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        creator_info = None
        if self.creator:
            creator_info = {
                'user_id': self.creator.user_id,
                'picture': self.creator.picture,
                'full_name': self.creator.full_name,
                'major': self.creator.major,
                'year_of_study': self.creator.year_of_study
            }
            
        # 获取最近5个参与者信息
        recent_participants = []
        approved_applications = ProjectApplication.query.filter_by(
            project_id=self.id, 
            status=ProjectApplication.STATUS_PENDING
        ).order_by(ProjectApplication.updated_at.desc()).limit(5).all()
        
        for app in approved_applications:
            if app.applicant:
                participant_info = {
                    'user_id': app.applicant.user_id,
                    'picture': app.applicant.picture,
                    'full_name': app.applicant.full_name
                }
                recent_participants.append(participant_info)
            
        return {
            'id': self.id,
            'name': self.name,
            'project_type': self.project_type,
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'description': self.description,
            'goal': self.goal,
            'status': self.status,
            'status_text': 'In progress' if self.status == self.STATUS_IN_PROGRESS else 'Completed',
            'recruitment_status': self.recruitment_status,
            'recruitment_status_text': 'Open for application' if self.recruitment_status == self.RECRUITMENT_OPEN else 'Application closed',
            'user_id': self.user_id,
            'creator_info': creator_info,
            'recent_participants': recent_participants,
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


class ProjectApplication(db.Model):
    """项目申请模型"""
    __tablename__ = 'project_applications'
    
    # 申请状态常量
    STATUS_PENDING = 1    # 待处理
    STATUS_APPROVED = 2   # 已接受
    STATUS_REJECTED = 3   # 已拒绝
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False, comment='项目ID')
    user_id = db.Column(db.String(100), db.ForeignKey('users.user_id'), nullable=False, comment='申请者ID')
    skill_type_id = db.Column(db.Integer, db.ForeignKey('skill_types.id'), nullable=False, comment='申请的技能类型')
    message = db.Column(db.Text, nullable=True, comment='申请消息')
    status = db.Column(db.Integer, default=STATUS_PENDING, comment='申请状态：1-待处理、2-已接受、3-已拒绝')
    response_message = db.Column(db.Text, nullable=True, comment='回复消息')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='申请时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关联关系
    applicant = db.relationship('User', backref='applications', foreign_keys=[user_id])
    skill_type = db.relationship('SkillType')
    
    def to_dict(self):
        """转换为字典"""
        status_text = {
            self.STATUS_PENDING: 'Pending',
            self.STATUS_APPROVED: 'Approved',
            self.STATUS_REJECTED: 'Rejected'
        }.get(self.status, 'Unknown status')
        
            
        # 项目信息包含项目负责人信息
        project_info = None
        creator_info = None
        if self.project:
            
            if self.project.creator:
                creator_info = {
                    'user_id': self.project.creator.user_id,
                    'full_name': self.project.creator.full_name,
                    'picture': self.project.creator.picture
                }
                
            project_info = {
                'id': self.project.id,
                'name': self.project.name,
                'project_type': self.project.project_type,
                'user_id': self.project.user_id,
            }
            
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'skill_type_id': self.skill_type_id,
            'skill_type_name': self.skill_type.name if self.skill_type else None,
            'message': self.message,
            'status': self.status,
            'status_text': status_text,
            'response_message': self.response_message,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'project_info': project_info,
            'creator_info': creator_info
        } 