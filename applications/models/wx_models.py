import datetime
from applications.extensions import db


class User(db.Model):
    __tablename__ = 'wx_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    name = db.Column(db.String(50), comment='用户名')
    realname = db.Column(db.String(50), comment='真实名字')
    age = db.Column(db.Integer, comment='年龄')
    password = db.Column(db.String(50), comment='密码')
    eamil = db.Column(db.String(50), comment='邮箱')

    def check_password(self, password):
        return password == self.password

class Health_Record(db.Model):
    __tablename__ = 'wx_health_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='记录ID')
    user_id = db.Column(db.Integer, db.ForeignKey('wx_usert.id'), primary_key=True)
    bp = db.Column(db.Float, comment='血压', default=0)
    bg = db.Column(db.Float, comment='血脂', default=0)
    bf = db.Column(db.Float, comment='血糖', default=0)
    weight = db.Column(db.Float, comment='体重', default=0)
    height = db.Column(db.Float, comment='身高', default=0)
    bmi = db.Column(db.Float, comment='BMI指数', default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
