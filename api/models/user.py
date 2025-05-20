from api import db
from datetime import datetime
import json


class User(db.Model):
    """用户模型"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True, comment="邮箱")
    full_name = db.Column(db.String(100), nullable=True, comment="全名")
    gender = db.Column(db.String(20), nullable=True, comment="性别")
    mbti = db.Column(db.String(10), nullable=True, comment="MBTI性格类型")
    star_sign = db.Column(db.String(20), nullable=True, comment="星座")
    skills = db.Column(db.Text, nullable=True, comment="技能")
    interests = db.Column(db.Text, nullable=True, comment="兴趣")
    year_of_study = db.Column(db.String(20), nullable=True, comment="学习年限")
    major = db.Column(db.String(100), nullable=True, comment="专业")
    key_factors = db.Column(db.Text, nullable=True, comment="关键因素，存储为JSON")
    lightning_answers = db.Column(
        db.Text, nullable=True, comment="快速回答，存储为JSON"
    )
    picture = db.Column(db.String(500), nullable=True, comment="用户头像URL")
    user_id = db.Column(
        db.String(100), nullable=False, unique=True, comment="Auth0用户标识"
    )
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 建立与项目的一对多关系
    projects = db.relationship("Project", backref="creator", lazy=True)

    def set_key_factors(self, key_factors):
        """设置关键因素，接受字典或字符串"""
        if isinstance(key_factors, dict):
            self.key_factors = json.dumps(key_factors)
        else:
            self.key_factors = key_factors

    def get_key_factors(self):
        """获取关键因素"""
        if self.key_factors:
            try:
                return json.loads(self.key_factors)
            except:
                return self.key_factors
        return {}

    def set_lightning_answers(self, answers):
        """设置快速回答"""
        if isinstance(answers, dict):
            self.lightning_answers = json.dumps(answers)
        else:
            self.lightning_answers = answers

    def get_lightning_answers(self):
        """获取快速回答"""
        if self.lightning_answers:
            try:
                return json.loads(self.lightning_answers)
            except:
                return {}
        return {}

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "gender": self.gender,
            "mbti": self.mbti,
            "star_sign": self.star_sign,
            "skills": self.skills,
            "interests": self.interests,
            "year_of_study": self.year_of_study,
            "major": self.major,
            "key_factors": self.get_key_factors(),
            "lightning_answers": self.get_lightning_answers(),
            "picture": self.picture,
            "user_id": self.user_id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
