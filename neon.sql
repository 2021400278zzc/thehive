/*
 Navicat Premium Data Transfer

 Source Server         : localhost-MySQL
 Source Server Type    : MySQL
 Source Server Version : 80033 (8.0.33)
 Source Host           : localhost:3306
 Source Schema         : neon

 Target Server Type    : MySQL
 Target Server Version : 80033 (8.0.33)
 File Encoding         : 65001

 Date: 24/06/2025 16:12:57
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for deliverable_confirmations
-- ----------------------------
DROP TABLE IF EXISTS `deliverable_confirmations`;
CREATE TABLE `deliverable_confirmations`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL COMMENT '项目ID',
  `deliverable_id` int NOT NULL COMMENT '交付物ID',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '贡献者ID',
  `confirmed` tinyint(1) NULL DEFAULT NULL COMMENT '是否已确认',
  `confirmed_at` datetime NULL DEFAULT NULL COMMENT '确认时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `project_id`(`project_id` ASC) USING BTREE,
  INDEX `deliverable_id`(`deliverable_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `deliverable_confirmations_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `deliverable_confirmations_ibfk_2` FOREIGN KEY (`deliverable_id`) REFERENCES `project_deliverables` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `deliverable_confirmations_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of deliverable_confirmations
-- ----------------------------

-- ----------------------------
-- Table structure for project_applications
-- ----------------------------
DROP TABLE IF EXISTS `project_applications`;
CREATE TABLE `project_applications`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL COMMENT '项目ID',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '申请者ID',
  `skill_type_id` int NOT NULL COMMENT '申请的技能类型',
  `message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '申请消息',
  `status` int NULL DEFAULT NULL COMMENT '申请状态：1-待处理、2-已接受、3-已拒绝',
  `response_message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '回复消息',
  `created_at` datetime NULL DEFAULT NULL COMMENT '申请时间',
  `updated_at` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `project_id`(`project_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `skill_type_id`(`skill_type_id` ASC) USING BTREE,
  CONSTRAINT `project_applications_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `project_applications_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `project_applications_ibfk_3` FOREIGN KEY (`skill_type_id`) REFERENCES `skill_types` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of project_applications
-- ----------------------------

-- ----------------------------
-- Table structure for project_contributions
-- ----------------------------
DROP TABLE IF EXISTS `project_contributions`;
CREATE TABLE `project_contributions`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL COMMENT '项目ID',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '贡献者Auth0用户标识',
  `role` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '在项目中的角色',
  `stars_earned` int NULL DEFAULT NULL COMMENT '获得的星级评价 (1-5)',
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `project_id`(`project_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `project_contributions_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `project_contributions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of project_contributions
-- ----------------------------

-- ----------------------------
-- Table structure for project_deliverables
-- ----------------------------
DROP TABLE IF EXISTS `project_deliverables`;
CREATE TABLE `project_deliverables`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL COMMENT '项目ID',
  `uploader_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '上传者ID',
  `file_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '文件存储URL',
  `file_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '文件类型',
  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '文件名',
  `file_size` int NULL DEFAULT NULL COMMENT '文件大小（字节）',
  `link_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '外部链接（如为URL导入）',
  `status` int NULL DEFAULT NULL COMMENT '交付物状态：0-草稿，1-已提交，2-已审核',
  `created_at` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `project_id`(`project_id` ASC) USING BTREE,
  INDEX `uploader_id`(`uploader_id` ASC) USING BTREE,
  CONSTRAINT `project_deliverables_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `project_deliverables_ibfk_2` FOREIGN KEY (`uploader_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of project_deliverables
-- ----------------------------

-- ----------------------------
-- Table structure for project_likes
-- ----------------------------
DROP TABLE IF EXISTS `project_likes`;
CREATE TABLE `project_likes`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL COMMENT '项目ID',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '点赞用户Auth0标识',
  `created_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `project_id`(`project_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `project_likes_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `project_likes_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of project_likes
-- ----------------------------
INSERT INTO `project_likes` VALUES (6, 1, 'auth0|admin123456789', '2025-06-23 17:05:39');
INSERT INTO `project_likes` VALUES (30, 3, 'auth0|683e86ad15b8d8c645cbe322', '2025-06-24 15:48:50');

-- ----------------------------
-- Table structure for projects
-- ----------------------------
DROP TABLE IF EXISTS `projects`;
CREATE TABLE `projects`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '项目名称',
  `project_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '项目类型',
  `end_time` datetime NOT NULL COMMENT '项目结束时间',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '项目描述',
  `goal` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '项目目标',
  `status` int NULL DEFAULT NULL COMMENT '项目状态：1-进行中、2-已完成',
  `recruitment_status` int NULL DEFAULT NULL COMMENT '招募状态：1-开放申请、2-招募结束',
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '创建者Auth0用户标识',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of projects
-- ----------------------------
INSERT INTO `projects` VALUES (1, '项目名称', '项目类型', '2025-06-05 12:13:23', '项目描述', '项目目标', 2, 1, '2025-06-23 14:38:35', '2025-06-23 14:46:14', 'auth0|test123456789');
INSERT INTO `projects` VALUES (2, 'test233335488', 'Software', '2025-06-23 23:59:59', 'ooooooooooooo', '先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也', 1, 1, '2025-06-23 15:24:23', '2025-06-23 15:24:23', 'auth0|683e86ad15b8d8c645cbe322');
INSERT INTO `projects` VALUES (3, '313414', 'Hardware', '2020-06-01 23:59:59', '21312312', '8.愿陛下托臣以讨贼兴复之效，不效，则治臣之罪，以告先帝之灵。若无兴德之言，则责攸之、祎、允等之慢，以彰其咎；陛下亦宜自谋，以咨诹善道', 1, 1, '2025-06-24 13:46:26', '2025-06-24 13:46:26', 'auth0|683e86ad15b8d8c645cbe322');

-- ----------------------------
-- Table structure for skill_requirements
-- ----------------------------
DROP TABLE IF EXISTS `skill_requirements`;
CREATE TABLE `skill_requirements`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `skill_type_id` int NOT NULL,
  `required_count` int NOT NULL COMMENT '所需人数',
  `importance` int NOT NULL COMMENT '重要程度(1-5星)',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '技能描述',
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `project_id`(`project_id` ASC) USING BTREE,
  INDEX `skill_type_id`(`skill_type_id` ASC) USING BTREE,
  CONSTRAINT `skill_requirements_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `skill_requirements_ibfk_2` FOREIGN KEY (`skill_type_id`) REFERENCES `skill_types` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of skill_requirements
-- ----------------------------
INSERT INTO `skill_requirements` VALUES (1, 1, 1, 5, 3, '技能描述', '2025-06-23 14:38:35', '2025-06-23 14:38:35');
INSERT INTO `skill_requirements` VALUES (2, 2, 9, 5, 5, '然侍卫之臣不懈于内，忠志之士忘身于外者，盖追先帝之殊遇，欲报之于陛下也', '2025-06-23 15:24:23', '2025-06-23 15:24:23');
INSERT INTO `skill_requirements` VALUES (3, 3, 10, 4, 5, '臣本布衣，躬耕于南阳，苟全性命于乱世，不求闻达于诸侯', '2025-06-24 13:46:26', '2025-06-24 13:46:26');

-- ----------------------------
-- Table structure for skill_types
-- ----------------------------
DROP TABLE IF EXISTS `skill_types`;
CREATE TABLE `skill_types`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '技能类型名称',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '技能类型描述',
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of skill_types
-- ----------------------------
INSERT INTO `skill_types` VALUES (1, 'Software Development', 'Develop various software applications, including desktop and server applications', '2025-06-23 13:39:29', '2025-06-23 13:39:29');
INSERT INTO `skill_types` VALUES (2, 'Web Development', 'Develop various website applications, including frontend and backend development', '2025-06-23 13:39:29', '2025-06-23 13:39:29');
INSERT INTO `skill_types` VALUES (3, 'Mobile App Development', 'Develop applications for mobile platforms like iOS and Android', '2025-06-23 13:39:29', '2025-06-23 13:39:29');
INSERT INTO `skill_types` VALUES (4, 'AI/Machine Learning Development', 'Develop artificial intelligence and machine learning related algorithms, models and applications', '2025-06-23 13:39:29', '2025-06-23 13:39:29');
INSERT INTO `skill_types` VALUES (5, 'UI/UX Design', 'Design user interfaces and user experiences to improve product usability', '2025-06-23 13:39:29', '2025-06-23 13:39:29');
INSERT INTO `skill_types` VALUES (6, 'Graphic Design', 'Design various visual content, including logos, posters, etc.', '2025-06-23 13:39:29', '2025-06-23 13:39:29');
INSERT INTO `skill_types` VALUES (7, 'Marketing', 'Responsible for product promotion, market analysis and user growth', '2025-06-23 13:39:29', '2025-06-23 13:39:29');
INSERT INTO `skill_types` VALUES (8, 'Content Creation', 'Create various types of content, including copy, video, audio, etc.', '2025-06-23 13:39:29', '2025-06-23 13:39:29');
INSERT INTO `skill_types` VALUES (9, 'Project Management', 'Responsible for project planning, execution, monitoring and closing', '2025-06-23 13:39:29', '2025-06-23 13:39:29');
INSERT INTO `skill_types` VALUES (10, 'Data Analysis', 'Analyze various data, provide data insights and decision support', '2025-06-23 13:39:29', '2025-06-23 13:39:29');
INSERT INTO `skill_types` VALUES (11, 'Finance/Accounting', 'Responsible for financial planning, fund management and accounting', '2025-06-23 13:39:29', '2025-06-23 13:39:29');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '邮箱',
  `full_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '全名',
  `gender` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '性别',
  `mbti` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT 'MBTI性格类型',
  `star_sign` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '星座',
  `skills` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '技能',
  `interests` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '兴趣',
  `year_of_study` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '学习年限',
  `major` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '专业',
  `key_factors` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '关键因素，存储为JSON',
  `lightning_answers` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '快速回答，存储为JSON',
  `fun_facts` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '趣事，存储为JSON',
  `best_working_experience` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '最佳工作经历',
  `tags` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '标签，存储为JSON',
  `picture` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户头像URL',
  `user_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Auth0用户标识',
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin@thehive.com', '系统管理员', '男', NULL, NULL, '项目管理, 系统管理', '技术, 管理', NULL, '计算机科学', NULL, NULL, NULL, NULL, NULL, 'https://s.gravatar.com/avatar/5d920db6767f734055bbcc817733c827?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fa.png', 'auth0|admin123456789', '2025-06-23 13:39:29', '2025-06-23 13:39:29');
INSERT INTO `users` VALUES (2, 'test@thehive.com', '测试用户', '女', NULL, NULL, '软件测试, 质量保证', '测试, 质量', NULL, '软件工程', NULL, NULL, NULL, NULL, NULL, 'https://s.gravatar.com/avatar/6d920db6767f734055bbcc817733c828?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Ft.png', 'auth0|test123456789', '2025-06-23 13:39:29', '2025-06-23 13:39:29');
INSERT INTO `users` VALUES (3, '3411033801@qq.com', '123123', 'Male', 'ENTJ', 'Taurus', 'sadfasf', 'asdfasf', 'Year 1', '123123', '{\"1\": \"Like-Minded\", \"2\": \"Teamwork\", \"3\": \"Self-Motivation\"}', '{\"0\": \"Cat\", \"1\": \"Call\", \"2\": \"Accuracy\", \"3\": \"Earn Money\"}', NULL, NULL, NULL, 'https://s.gravatar.com/avatar/fd92ea1c5e4ff32cff32fe02f6526b2a?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2F34.png', 'auth0|683e86ad15b8d8c645cbe322', '2025-06-23 15:22:52', '2025-06-23 15:22:52');

SET FOREIGN_KEY_CHECKS = 1;
