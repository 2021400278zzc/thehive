# TheHive 项目协作平台

TheHive是一个创业社交网站的项目协作功能，类似于GitHub的项目协作功能，但不提交代码。主要以项目制来推动人与人之间的合作。

## 项目结构

```
app/
  ├── __init__.py         # Flask应用初始化
  ├── models/             # 数据模型
  │   ├── project.py      # 项目、技能需求和技能类型模型
  │   └── user.py         # 用户模型
  ├── services/           # 服务层
  │   ├── project_service.py  # 项目和技能类型服务
  │   └── user_service.py     # 用户服务
  └── controllers/        # 控制器层
      ├── project_controller.py  # 项目控制器
      └── user_controller.py     # 用户控制器
app.py                    # 应用入口
init_db.py                # 数据库初始化脚本
database.sql              # SQL数据库创建和初始化脚本
requirements.txt          # 项目依赖
```

## 数据库表结构

1. **users表**：存储用户信息
   - id: 主键
   - email: 用户邮箱
   - full_name: 用户全名
   - gender: 性别
   - mbti: MBTI性格类型
   - star_sign: 星座
   - skills: 技能
   - interests: 兴趣
   - year_of_study: 学习年限
   - major: 专业
   - key_factors: 关键因素（JSON格式）
   - lightning_answers: 快速回答（JSON格式）
   - picture: 用户头像URL
   - user_id: Auth0用户标识

2. **skill_types表**：存储技能类型
   - id: 主键
   - name: 技能类型名称
   - description: 技能类型描述

3. **projects表**：存储项目基本信息
   - id: 主键
   - name: 项目名称
   - project_type: 项目类型
   - end_time: 项目结束时间
   - description: 项目描述
   - goal: 项目目标
   - status: 项目状态 (1-进行中、2-已完成)
   - recruitment_status: 招募状态 (1-开放申请、2-招募结束)
   - user_id: 创建者Auth0用户标识，直接对应users表中的user_id字段

4. **skill_requirements表**：存储项目所需技能
   - id: 主键
   - project_id: 项目ID (外键)
   - skill_type_id: 技能类型ID (外键)
   - required_count: 所需人数
   - importance: 重要程度(1-5星)
   - description: 技能描述

## 安装和配置

1. 克隆仓库

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置数据库
确保MySQL数据库已启动，并创建名为`neon`的数据库

4. 初始化数据库

方法一: 使用SQL脚本初始化数据库
```bash
mysql -u root -p123456 < database.sql
```

方法二: 使用Python脚本初始化数据库
```bash
python init_db.py
```

方法三: 使用Flask命令初始化数据库
```bash
flask init-db
```

## 运行项目
```bash
python app.py
```

服务将在 http://localhost:5000 上运行

## API 接口

### 1. 用户相关

#### 1.1 创建用户
- **URL**: `/api/users`
- **方法**: `POST`
- **请求体**:
```json
{
    "email": "用户邮箱",
    "full_name": "用户全名",
    "gender": "性别",
    "mbti": "MBTI性格类型",
    "star_sign": "星座",
    "skills": "技能",
    "interests": "兴趣",
    "year_of_study": "学习年限",
    "major": "专业",
    "key_factors": {},
    "lightning_answers": {},
    "picture": "用户头像URL",
    "user_id": "Auth0用户标识"
}
```

#### 1.2 获取用户信息
- **URL**: `/api/users/:user_id`
- **方法**: `GET`

#### 1.3 通过Auth0 ID获取用户
- **URL**: `/api/users/by-auth-id/:auth_id`
- **方法**: `GET`

### 2. 技能类型

#### 2.1 获取所有技能类型
- **URL**: `/api/skill-types`
- **方法**: `GET`

#### 2.2 创建技能类型
- **URL**: `/api/skill-types`
- **方法**: `POST`
- **请求体**:
```json
{
    "name": "技能类型名称",
    "description": "技能类型描述" // 可选
}
```

### 3. 创建项目

- **URL**: `/api/projects`
- **方法**: `POST`
- **请求体**:
```json
{
    "name": "项目名称",
    "project_type": "项目类型",
    "end_time": "项目结束时间",
    "description": "项目描述",  // 可选
    "goal": "项目目标",  // 可选
    "user_id": "创建者Auth0用户标识",  // 必填，字符串形式
    "skill_requirements": [
        {
            "skill_type_id": 技能类型ID,
            "required_count": 数量,
            "importance": 重要程度(1-5),
            "description": "技能描述"  // 可选
        }
    ]
}
```

### 4. 项目列表查询

- **URL**: `/api/projects`
- **方法**: `GET`
- **查询参数**:
  - `name`: 项目名称
  - `project_types`: 项目类别，多个用逗号分隔
  - `status`: 项目状态 (1-进行中、2-已完成)
  - `recruitment_status`: 招募状态 (1-开放申请、2-招募结束)
  - `skill_type_ids`: 所需技能类型ID，多个用逗号分隔
  - `keyword`: 关键词搜索（搜索项目描述和目标）

### 5. 项目详细查询

- **URL**: `/api/projects/:project_id`
- **方法**: `GET`
- **路径参数**:
  - `project_id`: 项目ID 