from zvms import db
from zvms.res import *
from zvms.utils import *

class Class(db.Model):
    __tablename__ = 'class'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5))

    @property
    def members(self):
        return User.query.filter_by(cls_id=self.id)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5))
    cls_id = db.Column(db.Integer, name='class')
    pwd = db.Column(db.String(32))
    auth = db.Column(db.Integer)

    @property
    def notices_sent(self):
        return Notice.query.filter_by(sender=self.id)

    @property
    def cls(self):
        return Class.query.get(self.cls_id)

    def __filter_thoughts(self, type):
        return sum(select_value(filter(lambda sv: Volunteer.query.get(sv.vol_id).
                    type == type and sv.reward is not None,
                    StuVol.query.filter_by(stu_id=self.id)), 'reward'))

    @property
    def inside(self):
        return self.__filter_thoughts(VolType.INSIDE)

    @property
    def outside(self):
        return self.__filter_thoughts(VOL_TYPE.OUTSIDE)

    @property
    def large(self):
        return self.__filter_thoughts(VOL_TYPE.LARGE)

class Notice(db.Model):
    __tablename__ = 'notice'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    content = db.Column(db.String(1024))
    sender = db.Column(db.Integer)
    deadtime = db.Column(db.DateTime)

class Volunteer(db.Model):
    __tablename__ = 'volunteer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(1024))
    holder_id = db.Column(db.Integer, name='holder')
    time = db.Column(db.DateTime)
    type = db.Column(db.SMALLINT)
    reward = db.Column(db.Integer)

    @property
    def joiners(self):
        return list(User.query.filter(User.id.in_(StuVol.query.filter(StuVol.vol_id == self.id,
            StuVol.status != STATUS.WAITING_FOR_SIGNUP_AUDIT).select_value('stu_id'))).select('name', 'id'))

class StuVol(db.Model):
    __tablename__ = 'stu_vol'

    stu_id = db.Column(db.Integer, primary_key=True)
    vol_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.SMALLINT)
    thought = db.Column(db.String(1024))
    reason = db.Column(db.String(1024))
    reward = db.Column(db.Integer)

    @property
    def pics(self):
        return Picture.query.filter_by(stu_id=self.stu_id, vol_id=self.vol_id).select_value('hash')

    @property
    def stu(self):
        return User.query.get(self.stu_id)

    @property
    def stu_name(self):
        return User.query.get(self.stu_id).name

    @property
    def vol_name(self):
        return Volunteer.query.get(self.vol_id).name

class ClassVol(db.Model):
    __tablename__ = 'class_vol'

    cls_id = db.Column(db.Integer, primary_key=True, name='class_id')
    vol_id = db.Column(db.Integer, primary_key=True)
    max = db.Column(db.Integer)

    @property
    def now(self):
        return count(StuVol.query.filter_by(vol_id=self.vol_id), lambda sv: sv.stu.cls_id == self.cls_id)

class Picture(db.Model):
    __tablename__ = 'picture'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # 这一列其实不需要, 但sqlalchemy强制表要有主键
    stu_id = db.Column(db.Integer)
    vol_id = db.Column(db.Integer)
    hash = db.Column(db.String(32))

class UserNotice(db.Model):
    __tablename__ = 'user_notice'

    user_id = db.Column(db.Integer, primary_key=True)
    notice_id = db.Column(db.Integer, primary_key=True)

class ClassNotice(db.Model):
    __tablename__ = 'class_notice'

    cls_id = db.Column(db.Integer, primary_key=True, name='class_id')
    notice_id = db.Column(db.Integer, primary_key=True)

class SchoolNotice(db.Model):
    __tablename__ = 'school_notice'

    notice_id = db.Column(db.Integer, primary_key=True)

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)