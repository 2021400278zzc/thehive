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
    status TINYINT DEFAULT 1 COMMENT 'Project status: 1- In Progress, 2- Completed',
    recruitment_status TINYINT DEFAULT 1 COMMENT 'Recruitment status: 1- Open, 2- Closed',
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
    status TINYINT DEFAULT 1 COMMENT 'Application status: 1- Pending, 2- Accepted, 3- Rejected',
    response_message TEXT COMMENT '回复消息',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '申请时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (skill_type_id) REFERENCES skill_types(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目申请表';

-- 项目交付物表
CREATE TABLE IF NOT EXISTS project_deliverables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL COMMENT '项目ID',
    uploader_id VARCHAR(100) NOT NULL COMMENT '上传者ID',
    file_url VARCHAR(255) COMMENT '文件存储URL',
    file_type VARCHAR(50) COMMENT '文件类型',
    file_name VARCHAR(255) COMMENT '文件名',
    file_size INT COMMENT '文件大小（字节）',
    link_url VARCHAR(255) COMMENT '外部链接（如为URL导入）',
    status TINYINT DEFAULT 0 COMMENT '交付物状态：0-草稿，1-已提交，2-已审核',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (uploader_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目交付物表';

-- 交付物确认表
CREATE TABLE IF NOT EXISTS deliverable_confirmations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL COMMENT '项目ID',
    deliverable_id INT NOT NULL COMMENT '交付物ID',
    user_id VARCHAR(100) NOT NULL COMMENT '贡献者ID',
    confirmed TINYINT(1) DEFAULT 1 COMMENT '是否已确认',
    confirmed_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '确认时间',
    UNIQUE KEY uq_deliverable_user (deliverable_id, user_id),
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (deliverable_id) REFERENCES project_deliverables(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='交付物确认表';

-- 插入初始技能类型数据
INSERT INTO skill_types (name, description) VALUES
('Software Development', 'Develop various software applications, including desktop and server applications'),
('Web Development', 'Develop various website applications, including frontend and backend development'),
('Mobile App Development', 'Develop applications for mobile platforms like iOS and Android'),
('AI/Machine Learning Development', 'Develop artificial intelligence and machine learning related algorithms, models and applications'),
('UI/UX Design', 'Design user interfaces and user experiences to improve product usability'),
('Graphic Design', 'Design various visual content, including logos, posters, etc.'),
('Marketing', 'Responsible for product promotion, market analysis and user growth'),
('Content Creation', 'Create various types of content, including copy, video, audio, etc.'),
('Project Management', 'Responsible for project planning, execution, monitoring and closing'),
('Data Analysis', 'Analyze various data, provide data insights and decision support'),
('Finance/Accounting', 'Responsible for financial planning, fund management and accounting')
ON DUPLICATE KEY UPDATE description=VALUES(description); 