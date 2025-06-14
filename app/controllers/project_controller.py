from flask import Blueprint, request, jsonify, send_from_directory
from app.services.project_service import ProjectService, SkillTypeService, ProjectApplicationService, ProjectDeliverableService, DeliverableConfirmationService
from app.models.project import ProjectApplication
from datetime import datetime

project_bp = Blueprint('project', __name__, url_prefix='/api')

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
        "user_id": 创建者用户ID,  # 必填
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
    print(data)
    # 参数验证
    required_fields = ['name', 'project_type', 'end_time', 'user_id']
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
    
    # 获取创建者ID
    user_id = data.get('user_id')
    
    try:
        project = ProjectService.create_project(data, user_id)
        return jsonify({'message': '项目创建成功', 'data': project.to_dict()}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
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

@project_bp.route('/projects/founder', methods=['GET'])
def get_founder_projects():
    """
    获取我创建的项目列表API
    
    请求体参数:
    - user_id: 用户ID (必需)
    
    请求参数 (URL查询参数):
    - name: 项目名称
    - project_types: 项目类别，多个用逗号分隔
    - status: 项目状态 (1-进行中、2-已完成)
    - recruitment_status: 招募状态 (1-开放申请、2-招募结束)
    - skill_type_ids: 所需技能ID，多个用逗号分隔
    - keyword: 关键词搜索（搜索项目描述和目标）
    """
    # 从请求体获取 user_id
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': '缺少必需的 user_id 参数'}), 400
    
    # 首先创建基础过滤条件，包含 user_id
    filters = {
        'user_id': user_id
    }
    
    # 获取并处理其他查询参数
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
        projects = ProjectService.get_founder_project_list(filters)
        return jsonify({'data': projects, 'total': len(projects)}), 200
    except Exception as e:
        return jsonify({'error': f'获取项目列表失败: {str(e)}'}), 500

@project_bp.route('/projects/participant', methods=['GET'])
def get_participant_projects():
    """
    获取我参与的项目列表API
    
    请求体参数:
    - user_id: 用户ID (必需)
    
    请求参数 (URL查询参数):
    - name: 项目名称
    - project_types: 项目类别，多个用逗号分隔
    - status: 项目状态 (1-进行中、2-已完成)
    - recruitment_status: 招募状态 (1-开放申请、2-招募结束)
    - skill_type_ids: 所需技能ID，多个用逗号分隔
    - keyword: 关键词搜索（搜索项目描述和目标）
    """
    # 从请求体获取 user_id
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': '缺少必需的 user_id 参数'}), 400
    
    # 首先创建基础过滤条件，包含 user_id
    filters = {
        'user_id': user_id
    }
    
    # 获取并处理其他查询参数
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
        projects = ProjectService.get_participant_project_list(filters)
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


@project_bp.route('/project-applications', methods=['POST'])
def apply_for_project():
    """
    申请加入项目API
    请求参数:
    {
        "project_id": 项目ID,
        "skill_type_id": 技能类型ID,
        "message": "申请消息"  # 可选
    }
    """
    data = request.get_json()
    
    # 参数验证
    required_fields = ['project_id', 'skill_type_id', 'user_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    # 获取申请者ID
    user_id = data.get('user_id')
    
    try:
        application = ProjectApplicationService.apply_for_project(data, user_id)
        return jsonify({'message': '申请提交成功', 'data': application.to_dict()}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'提交申请失败: {str(e)}'}), 500


@project_bp.route('/project-applications/<int:application_id>', methods=['PUT'])
def process_application(application_id):
    """
    处理项目申请API
    请求参数:
    {
        "status": 状态码(2-接受, 3-拒绝),
        "response_message": "回复消息",  # 可选
        "user_id": "处理人ID"  # 必填，必须是项目负责人
    }
    """
    data = request.get_json()
    
    # 参数验证
    if 'status' not in data:
        return jsonify({'error': '缺少必填字段: status'}), 400
    
    if data['status'] not in [ProjectApplication.STATUS_APPROVED, ProjectApplication.STATUS_REJECTED]:
        return jsonify({'error': '状态码无效，必须为2(接受)或3(拒绝)'}), 400
    
    if 'user_id' not in data:
        return jsonify({'error': '缺少必填字段: user_id'}), 400
    
    try:
        application = ProjectApplicationService.process_application(
            application_id,
            data['status'],
            data.get('response_message'),
            data['user_id']
        )
        return jsonify({'message': '申请处理成功', 'data': application.to_dict()}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'处理申请失败: {str(e)}'}), 500


@project_bp.route('/my-applications', methods=['GET'])
def get_my_applications():
    """
    获取我提交的申请列表API
    
    请求参数 (URL查询参数):
    - user_id: 用户ID
    """
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': '缺少必填参数: user_id'}), 400
    
    try:
        applications = ProjectApplicationService.get_my_applications(user_id)
        return jsonify({'data': applications, 'total': len(applications)}), 200
    except Exception as e:
        return jsonify({'error': f'获取申请列表失败: {str(e)}'}), 500


@project_bp.route('/projects/<int:project_id>/applications', methods=['GET'])
def get_project_applications(project_id):
    """
    获取项目收到的申请列表API
    
    请求参数 (URL查询参数):
    - user_id: 当前用户ID (可选，不再用于权限验证)
    """
    try:
        applications = ProjectApplicationService.get_project_applications(project_id)
        return jsonify({'data': applications, 'total': len(applications)}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'获取项目申请列表失败: {str(e)}'}), 500

@project_bp.route('/projects/participants', methods=['DELETE'])
def remove_project_participant():
    """
    移除项目参与者API
    
    路径参数:
    - project_id: 项目ID
    - participant_user_id: 要移除的参与者ID
    
    请求参数 (URL查询参数):
    - creator_id: 操作者ID (必须是项目创建者)
    """
    creator_id = request.args.get('creator_id')
    participant_user_id = request.args.get('participant_user_id')
    project_id = request.args.get('project_id')
    if not creator_id:
        return jsonify({'error': '缺少必填参数: creator_id'}), 400
    
    try:
        result = ProjectApplicationService.remove_project_participant(project_id, participant_user_id, creator_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': f'移除项目参与者失败: {str(e)}'}), 500

@project_bp.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """
    更新项目信息API
    请求参数:
    {
        "name": "项目名称",  # 可选
        "project_type": "项目类型",  # 可选
        "end_time": "项目结束时间",  # 可选,格式:YYYY-MM-DD HH:MM:SS
        "description": "项目描述",  # 可选
        "goal": "项目目标",  # 可选
        "status": 项目状态,  # 可选,1-进行中、2-已完成
        "recruitment_status": 招募状态,  # 可选,1-开放申请、2-招募结束
        "skill_requirements": [  # 可选
            {
                "skill_type_id": 技能类型ID,
                "required_count": 数量,
                "importance": 重要程度(1-5),
                "description": "技能描述"  # 可选
            }
        ],
        "user_id": 操作者ID  # 必填，必须是项目创建者
    }
    """
    data = request.get_json()
    
    # 参数验证
    if not data:
        return jsonify({'error': '请求体不能为空'}), 400
    
    if 'user_id' not in data:
        return jsonify({'error': '缺少必填字段: user_id'}), 400
    
    # 验证日期格式
    if 'end_time' in data:
        try:
            datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'error': '结束时间格式无效,请使用YYYY-MM-DD HH:MM:SS格式'}), 400
    
    # 验证状态值
    if 'status' in data:
        if data['status'] not in [1, 2]:
            return jsonify({'error': '项目状态值无效,必须为1(进行中)或2(已完成)'}), 400
    
    if 'recruitment_status' in data:
        if data['recruitment_status'] not in [1, 2]:
            return jsonify({'error': '招募状态值无效,必须为1(开放申请)或2(招募结束)'}), 400
    
    # 验证技能需求数据
    if 'skill_requirements' in data:
        if not isinstance(data['skill_requirements'], list):
            return jsonify({'error': 'skill_requirements必须是数组'}), 400
            
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
        project = ProjectService.update_project(project_id, data, data['user_id'])
        return jsonify({
            'message': '项目更新成功',
            'data': project.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': f'更新项目失败: {str(e)}'}), 500

@project_bp.route('/projects', methods=['DELETE'])
def delete_project():
    """
    删除项目API
    
    请求参数 (URL查询参数):
    - user_id: 操作者ID (必填，必须是项目创建者)
    """
    project_id = request.args.get('project_id')
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': '缺少必填参数: user_id'}), 400
    
    try:
        result = ProjectService.delete_project(project_id, user_id)
        return jsonify({
            'message': '项目删除成功',
            'data': result
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': f'删除项目失败: {str(e)}'}), 500

@project_bp.route('/projects/deliverables', methods=['GET'])
def get_project_deliverables():
    """
    获取项目交付物列表，支持返回当前用户确认状态
    """
    project_id = request.args.get('project_id')
    user_id = request.args.get('user_id')
    try:
        deliverables = ProjectDeliverableService.get_deliverables_by_project(project_id)
        # 如果带 user_id，补充确认状态
        if user_id:
            for d in deliverables:
                status = DeliverableConfirmationService.get_deliverable_confirm_status(d['id'], user_id)
                d['confirmed'] = status.get('confirmed', False)
        return jsonify({'data': deliverables, 'total': len(deliverables)}), 200
    except Exception as e:
        return jsonify({'error': f'获取交付物失败: {str(e)}'}), 500

@project_bp.route('/projects/deliverables', methods=['POST'])
def upload_project_deliverable():
    """
    上传交付物（支持文件和URL导入）
    支持 form-data: file, file_type, file_name, file_size, link_url, status, uploader_id
    """
    try:
        project_id = request.form.get('project_id')
        uploader_id = request.form.get('uploader_id')
        if not uploader_id:
            return jsonify({'error': '缺少必填参数: uploader_id'}), 400
        data = {
            'project_id': project_id,
            'file_type': request.form.get('file_type'),
            'file_name': request.form.get('file_name'),
            'file_size': request.form.get('file_size'),
            'link_url': request.form.get('link_url'),
            'status': int(request.form.get('status', 0)),
        }
        file = request.files.get('file')
        deliverable = ProjectDeliverableService.create_deliverable(project_id, data, uploader_id, file)
        return jsonify({'message': '交付物上传成功', 'data': deliverable.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': f'上传交付物失败: {str(e)}'}), 500

@project_bp.route('/deliverables', methods=['DELETE'])
def delete_project_deliverable():
    """
    删除交付物（仅上传者可删）
    需传 uploader_id
    """
    deliverable_id = request.args.get('deliverable_id')
    uploader_id = request.args.get('uploader_id')
    if not uploader_id:
        return jsonify({'error': '缺少必填参数: uploader_id'}), 400
    try:
        ProjectDeliverableService.delete_deliverable(deliverable_id, uploader_id)
        return jsonify({'message': '交付物删除成功'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': f'删除交付物失败: {str(e)}'}), 500

@project_bp.route('/deliverables/status', methods=['PUT'])
def update_deliverable_status():
    """
    更新交付物状态（提交/审核）
    需传 status, reviewer_id（审核时）
    """
    data = request.get_json()
    deliverable_id = data.get('deliverable_id')
    if 'status' not in data:
        return jsonify({'error': '缺少必填字段: status'}), 400
    try:
        deliverable = ProjectDeliverableService.update_status(deliverable_id, data['status'], data.get('reviewer_id'))
        # 若为审核通过，自动检查项目是否可标记为已完成
        if data['status'] == 2:
            ProjectDeliverableService.check_and_complete_project(deliverable.project_id)
        return jsonify({'message': '交付物状态更新成功', 'data': deliverable.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': f'更新交付物状态失败: {str(e)}'}), 500

@project_bp.route('/static/deliverables', methods=['GET'])
def get_deliverable_file():
    """
    下载交付物文件
    """
    project_id = request.args.get('project_id')
    filename = request.args.get('filename')
    project_id = str(project_id)
    return send_from_directory(f'static/deliverables/{project_id}',filename)

@project_bp.route('/deliverables', methods=['GET'])
def get_deliverable_detail():
    """
    获取交付物详情
    """
    try:
        deliverable_id = request.args.get('deliverable_id')
        deliverable = ProjectDeliverableService.get_deliverable_by_id(deliverable_id)
        if not deliverable:
            return jsonify({'error': '交付物不存在'}), 404
        return jsonify({'data': deliverable.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': f'获取交付物详情失败: {str(e)}'}), 500

@project_bp.route('/deliverables/confirm', methods=['POST'])
def confirm_deliverable():
    """
    贡献者确认交付物
    需传 user_id
    """
    deliverable_id = request.json.get('deliverable_id')
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'error': '缺少必填参数: user_id'}), 400
    try:
        confirmation = DeliverableConfirmationService.confirm_deliverable(deliverable_id, user_id)
        # 检查项目是否可自动完成
        DeliverableConfirmationService.check_and_complete_project_by_confirmation(confirmation.project_id)
        return jsonify({'message': '交付物确认成功', 'data': confirmation.to_dict()}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': f'交付物确认失败: {str(e)}'}), 500

@project_bp.route('/deliverables/confirm-status', methods=['GET'])
def get_deliverable_confirm_status():
    """
    查询某用户对某交付物的确认状态
    """
    deliverable_id = request.args.get('deliverable_id')
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': '缺少必填参数: user_id'}), 400
    try:
        status = DeliverableConfirmationService.get_deliverable_confirm_status(deliverable_id, user_id)
        return jsonify({'data': status}), 200
    except Exception as e:
        return jsonify({'error': f'查询交付物确认状态失败: {str(e)}'}), 500

@project_bp.route('/projects/confirm-status', methods=['GET'])
def get_project_confirm_status():
    """
    查询某用户对整个项目交付物的确认状态
    """
    project_id = request.args.get('project_id')
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': '缺少必填参数: user_id'}), 400
    try:
        status = DeliverableConfirmationService.get_project_confirm_status(project_id, user_id)
        return jsonify({'data': status}), 200
    except Exception as e:
        return jsonify({'error': f'查询项目交付物确认状态失败: {str(e)}'}), 500 