from app import db
from app.models.project import Project, SkillRequirement, SkillType
from datetime import datetime
from sqlalchemy import or_, and_

class SkillTypeService:
    @staticmethod
    def get_all_skill_types():
        """
        获取所有技能类型
        :return: 技能类型列表
        """
        skill_types = SkillType.query.all()
        return [skill_type.to_dict() for skill_type in skill_types]
    
    @staticmethod
    def get_skill_type_by_id(skill_type_id):
        """
        根据ID获取技能类型
        :param skill_type_id: 技能类型ID
        :return: 技能类型对象
        """
        return SkillType.query.get_or_404(skill_type_id)
    
    @staticmethod
    def create_skill_type(data):
        """
        创建新技能类型
        :param data: 包含技能类型信息的字典
        :return: 创建的技能类型对象
        """
        skill_type = SkillType(
            name=data['name'],
            description=data.get('description')
        )
        db.session.add(skill_type)
        db.session.commit()
        return skill_type

class ProjectService:
    @staticmethod
    def create_project(data):
        """
        创建新项目
        :param data: 包含项目信息的字典
        :return: 创建的项目对象
        """
        # 创建项目
        project = Project(
            name=data['name'],
            project_type=data['project_type'],
            end_time=datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S'),
            description=data.get('description'),
            goal=data.get('goal'),
            status=Project.STATUS_IN_PROGRESS,
            recruitment_status=Project.RECRUITMENT_OPEN
        )
        
        # 添加技能需求
        skills_data = data.get('skill_requirements', [])
        for skill_data in skills_data:
            skill = SkillRequirement(
                skill_type_id=skill_data['skill_type_id'],
                required_count=skill_data['required_count'],
                importance=skill_data['importance'],
                description=skill_data.get('description')
            )
            project.skill_requirements.append(skill)
        
        # 保存到数据库
        db.session.add(project)
        db.session.commit()
        
        return project
    
    @staticmethod
    def get_project_list(filters=None):
        """
        获取项目列表，支持多种过滤条件
        :param filters: 过滤条件字典
        :return: 项目列表
        """
        query = Project.query
        
        if filters:
            # 项目名称筛选
            if 'name' in filters and filters['name']:
                query = query.filter(Project.name.like(f"%{filters['name']}%"))
            
            # 项目类别筛选（多选）
            if 'project_types' in filters and filters['project_types']:
                query = query.filter(Project.project_type.in_(filters['project_types']))
            
            # 项目状态筛选
            if 'status' in filters and filters['status']:
                status_value = int(filters['status'])
                query = query.filter(Project.status == status_value)
            
            # 招募状态筛选
            if 'recruitment_status' in filters and filters['recruitment_status']:
                recruitment_status_value = int(filters['recruitment_status'])
                query = query.filter(Project.recruitment_status == recruitment_status_value)
            
            # 所需技能筛选（多选）
            if 'skill_type_ids' in filters and filters['skill_type_ids']:
                skill_ids = [int(id) for id in filters['skill_type_ids']]
                skill_filter = or_(*[SkillRequirement.skill_type_id == skill_id for skill_id in skill_ids])
                query = query.join(SkillRequirement).filter(skill_filter).distinct()
            
            # 描述关键词筛选
            if 'keyword' in filters and filters['keyword']:
                keyword = f"%{filters['keyword']}%"
                query = query.filter(or_(
                    Project.description.like(keyword),
                    Project.goal.like(keyword)
                ))
                
        # 返回项目列表
        projects = query.all()
        return [project.to_dict() for project in projects]
    
    @staticmethod
    def get_project_detail(project_id):
        """
        获取项目详情
        :param project_id: 项目ID
        :return: 项目详情
        """
        project = Project.query.get_or_404(project_id)
        return project.to_dict() 