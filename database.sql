-- 创建数据库
CREATE DATABASE IF NOT EXISTS neon DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE neon;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
    full_name VARCHAR(100) COMMENT '全名',
    gender VARCHAR(20) COMMENT '性别',
    mbti VARCHAR(10) COMMENT 'MBTI性格类型',
    star_sign VARCHAR(20) COMMENT '星座',
    skills TEXT COMMENT '技能',
    interests TEXT COMMENT '兴趣',
    year_of_study VARCHAR(20) COMMENT '学习年限',
    major VARCHAR(100) COMMENT '专业',
    key_factors TEXT COMMENT '关键因素，存储为JSON',
    lightning_answers TEXT COMMENT '快速回答，存储为JSON',
    picture VARCHAR(500) COMMENT '用户头像URL',
    user_id VARCHAR(100) NOT NULL UNIQUE COMMENT 'Auth0用户标识',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 创建技能类型表
CREATE TABLE IF NOT EXISTS skill_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE COMMENT '技能类型名称',
    description TEXT COMMENT '技能类型描述',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='技能类型表';

-- 创建项目表
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '项目名称',
    project_type VARCHAR(50) NOT NULL COMMENT '项目类型',
    end_time DATETIME NOT NULL COMMENT '项目结束时间',
    description TEXT COMMENT '项目描述',
    goal TEXT COMMENT '项目目标',
    status TINYINT DEFAULT 1 COMMENT '项目状态：1-进行中、2-已完成',
    recruitment_status TINYINT DEFAULT 1 COMMENT '招募状态：1-开放申请、2-招募结束',
    user_id VARCHAR(100) NOT NULL COMMENT '创建者Auth0用户标识',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目表';

-- 创建技能需求表
CREATE TABLE IF NOT EXISTS skill_requirements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL COMMENT '项目ID',
    skill_type_id INT NOT NULL COMMENT '技能类型ID',
    required_count INT NOT NULL COMMENT '所需人数',
    importance INT NOT NULL COMMENT '重要程度(1-5星)',
    description TEXT COMMENT '技能描述',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_type_id) REFERENCES skill_types(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='技能需求表';

-- 创建项目申请表
CREATE TABLE IF NOT EXISTS project_applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL COMMENT '项目ID',
    user_id VARCHAR(100) NOT NULL COMMENT '申请者ID',
    skill_type_id INT NOT NULL COMMENT '申请的技能类型',
    message TEXT COMMENT '申请消息',
    status TINYINT DEFAULT 1 COMMENT '申请状态：1-待处理、2-已接受、3-已拒绝',
    response_message TEXT COMMENT '回复消息',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '申请时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_type_id) REFERENCES skill_types(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目申请表';

-- 插入初始技能类型数据
INSERT INTO skill_types (name, description) VALUES
('软件开发', '开发各类软件应用，包括桌面应用、服务端应用等'),
('网站开发', '开发各类网站应用，包括前端、后端开发等'),
('手机app开发', '开发iOS、Android等移动平台的应用程序'),
('AI或机器学习开发', '开发人工智能和机器学习相关算法、模型和应用'),
('UI或UX设计', '设计用户界面和用户体验，提升产品易用性'),
('平面设计', '设计各类平面视觉内容，包括Logo、海报等'),
('市场营销', '负责产品推广、市场分析和用户增长等工作'),
('内容创作', '创作各类内容，包括文案、视频、音频等'),
('项目管理', '负责项目的计划、执行、监控和收尾等管理工作'),
('数据分析', '分析各类数据，提供数据洞察和决策支持'),
('金融/会计', '负责财务规划、资金管理和会计核算等工作')
ON DUPLICATE KEY UPDATE description=VALUES(description); 