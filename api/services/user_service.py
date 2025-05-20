from api import db
from api.models.user import User
from sqlalchemy import or_

class UserService:
    @staticmethod
    def create_user(data):
        """
        创建新用户
        :param data: 包含用户信息的字典
        :return: 创建的用户对象
        """
        # 检查邮箱是否已存在
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            raise ValueError(f"邮箱 {data['email']} 已被注册")
        
        # 创建用户
        user = User(
            email=data['email'],
            full_name=data.get('full_name'),
            gender=data.get('gender'),
            mbti=data.get('mbti'),
            star_sign=data.get('star_sign'),
            skills=data.get('skills'),
            interests=data.get('interests'),
            year_of_study=data.get('year_of_study'),
            major=data.get('major'),
            picture=data.get('picture'),
            user_id=data.get('user_id')
        )
        
        # 处理关键因素
        if 'key_factors' in data:
            user.set_key_factors(data['key_factors'])
        
        # 处理快速回答
        if 'lightning_answers' in data:
            user.set_lightning_answers(data['lightning_answers'])
        
        # 保存到数据库
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        根据ID获取用户
        :param user_id: 用户ID
        :return: 用户对象
        """
        return User.query.get_or_404(user_id)
    
    @staticmethod
    def get_user_by_email(email):
        """
        根据邮箱获取用户
        :param email: 用户邮箱
        :return: 用户对象
        """
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_user_by_auth_id(auth_id):
        """
        根据Auth0标识获取用户
        :param auth_id: Auth0用户标识
        :return: 用户对象
        """
        return User.query.filter_by(user_id=auth_id).first()
    
    @staticmethod
    def get_user_list(filters=None):
        """
        获取用户列表，支持过滤条件
        :param filters: 过滤条件字典
        :return: 用户列表
        """
        query = User.query
        
        if filters:
            # 邮箱筛选
            if 'email' in filters and filters['email']:
                query = query.filter(User.email.like(f"%{filters['email']}%"))
            
            # 全名筛选
            if 'full_name' in filters and filters['full_name']:
                query = query.filter(User.full_name.like(f"%{filters['full_name']}%"))
            
            # 性别筛选
            if 'gender' in filters and filters['gender']:
                query = query.filter(User.gender == filters['gender'])
            
            # MBTI筛选
            if 'mbti' in filters and filters['mbti']:
                query = query.filter(User.mbti == filters['mbti'])
            
            # 星座筛选
            if 'star_sign' in filters and filters['star_sign']:
                query = query.filter(User.star_sign == filters['star_sign'])
            
            # 专业筛选
            if 'major' in filters and filters['major']:
                query = query.filter(User.major.like(f"%{filters['major']}%"))
            
            # Auth0标识筛选
            if 'user_id' in filters and filters['user_id']:
                query = query.filter(User.user_id == filters['user_id'])
        
        # 返回用户列表
        users = query.all()
        return [user.to_dict() for user in users] 