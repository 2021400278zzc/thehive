from flask import Blueprint, request, jsonify
from app.services.project_service import ProjectService, SkillTypeService

project_bp = Blueprint('project', __name__)

@project_bp.route('/skill-types', methods=['GET'])
def get_skill_types():
    """
    获取所有技能类型API
    """
    try:
        skill_types = SkillTypeService.get_all_skill_types()
        return jsonify({'data': skill_types, 'total': len(skill_types)}), 200
    except Exception as e:
        return jsonify({'error': f'获取技能类型失败: {str(e)}'}), 500

@project_bp.route('/skill-types', methods=['POST'])
def create_skill_type():
    """
    创建技能类型API
    请求参数:
    {
        "name": "技能类型名称",
        "description": "技能类型描述"  # 可选
    }
    """
    data = request.get_json()
    
    # 参数验证
    if not data.get('name'):
        return jsonify({'error': '缺少必填字段: name'}), 400
    
    try:
        skill_type = SkillTypeService.create_skill_type(data)
        return jsonify({'message': '技能类型创建成功', 'data': skill_type.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': f'创建技能类型失败: {str(e)}'}), 500

@project_bp.route('/projects', methods=['POST'])
def create_project():
    """
    创建项目API
    请求参数:
    {
        "name": "项目名称",
        "project_type": "项目类型",
        "end_time": "项目结束时间",
        "description": "项目描述",  # 可选
        "goal": "项目目标",  # 可选
        "skill_requirements": [
            {
                "skill_type_id": 技能类型ID,
                "required_count": 数量,
                "importance": 重要程度(1-5),
                "description": "技能描述"  # 可选
            }
        ]
    }
    """
    data = request.get_json()
    
    # 参数验证
    required_fields = ['name', 'project_type', 'end_time']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    # 验证技能需求数据
    if 'skill_requirements' in data:
        for i, skill in enumerate(data['skill_requirements']):
            required_skill_fields = ['skill_type_id', 'required_count', 'importance']
            for field in required_skill_fields:
                if field not in skill:
                    return jsonify({'error': f'第{i+1}个技能需求缺少必填字段: {field}'}), 400
            
            # 验证重要程度是否在1-5范围
            if not (1 <= skill['importance'] <= 5):
                return jsonify({'error': f'第{i+1}个技能需求的重要程度必须在1-5之间'}), 400
            
            # 验证技能类型ID是否存在
            try:
                SkillTypeService.get_skill_type_by_id(skill['skill_type_id'])
            except:
                return jsonify({'error': f'第{i+1}个技能需求的技能类型ID不存在'}), 400
    
    try:
        project = ProjectService.create_project(data)
        return jsonify({'message': '项目创建成功', 'data': project.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': f'创建项目失败: {str(e)}'}), 500


@project_bp.route('/projects', methods=['GET'])
def get_project_list():
    """
    获取项目列表API，支持多种过滤条件
    
    请求参数 (URL查询参数):
    - name: 项目名称
    - project_types: 项目类别，多个用逗号分隔
    - status: 项目状态 (1-进行中、2-已完成)
    - recruitment_status: 招募状态 (1-开放申请、2-招募结束)
    - skill_type_ids: 所需技能ID，多个用逗号分隔
    - keyword: 关键词搜索（搜索项目描述和目标）
    """
    filters = {}
    
    # 获取并处理查询参数
    if request.args.get('name'):
        filters['name'] = request.args.get('name')
    
    if request.args.get('project_types'):
        filters['project_types'] = request.args.get('project_types').split(',')
    
    if request.args.get('status'):
        filters['status'] = request.args.get('status')
    
    if request.args.get('recruitment_status'):
        filters['recruitment_status'] = request.args.get('recruitment_status')
    
    if request.args.get('skill_type_ids'):
        filters['skill_type_ids'] = request.args.get('skill_type_ids').split(',')
    
    if request.args.get('keyword'):
        filters['keyword'] = request.args.get('keyword')
    
    try:
        projects = ProjectService.get_project_list(filters)
        return jsonify({'data': projects, 'total': len(projects)}), 200
    except Exception as e:
        return jsonify({'error': f'获取项目列表失败: {str(e)}'}), 500


@project_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project_detail(project_id):
    """
    获取项目详情API
    
    路径参数:
    - project_id: 项目ID
    """
    try:
        project = ProjectService.get_project_detail(project_id)
        return jsonify({'data': project}), 200
    except Exception as e:
        return jsonify({'error': f'获取项目详情失败: {str(e)}'}), 500 