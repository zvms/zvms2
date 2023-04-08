from sqlalchemy import Column, Integer, String, SmallInteger, DateTime, Date
from flask_sqlalchemy import SQLAlchemy

from zvms.res import *
from zvms.util import ModelMixIn, render_markdown, select_value, count, init_util, list_or_error

db = SQLAlchemy()

init_util(db)

class Class(ModelMixIn, db.Model):
    __tablename__ = 'class'

    id = Column(Integer, primary_key=True)
    name = Column(String(5))

    def on_delete(self):
        ClassNotice.query.filter_by(cls_id=self.id).delete()
        ClassVol.query.filter_by(cls_id=self.id).delete()
        User.query.filter_by(cls_id=self.id).delete()

    @property
    def members(self):
        return User.query.filter_by(cls_id=self.id)


class User(ModelMixIn, db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(5))
    cls_id = Column(Integer, name='class')
    pwd = Column(String(32))
    auth = Column(Integer)

    def on_delete(self):
        UserNotice.query.filter_by(user_id=self.user_id).delete()
        StuVol.query.filter_by(stu_id=self.user_id).delete()
        Volunteer.query.filter_by(holder_id=self.id).delete()

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
        return self.__filter_thoughts(VolType.OUTSIDE)

    @property
    def large(self):
        return self.__filter_thoughts(VolType.LARGE)


class Notice(ModelMixIn, db.Model):
    __tablename__ = 'notice'

    def on_delete(self):
        UserNotice.query.filter_by(notice_id=self.id).delete()
        ClassNotice.query.filter_by(notice_id=self.id).delete()
        SchoolNotice.query.filter_by(notice_id=self.id).delete()

    id = Column(Integer, primary_key=True)
    title = Column(String(32))
    content = Column(String(1024))
    sender = Column(Integer)
    sendtime = Column(DateTime)
    deadtime = Column(DateTime)

    @property
    def sender_name(self):
        return User.query.get(self.sender).name


class Volunteer(ModelMixIn, db.Model):
    __tablename__ = 'volunteer'

    def on_delete(self):
        StuVol.query.filter_by(vol_id=self.id).delete()

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    description = Column(String(1024))
    status = Column(SmallInteger)
    holder_id = Column(Integer, name='holder')
    time = Column(DateTime)
    type = Column(SmallInteger)
    reward = Column(Integer)

    @property
    def joiners(self):
        return list(User.query.filter(User.id.in_(StuVol.query.filter(StuVol.vol_id == self.id,
            StuVol.status != ThoughtStatus.WAITING_FOR_SIGNUP_AUDIT).select_value('stu_id'))).select('name', 'id'))

    @property
    def holder(self):
        return User.query.get(self.holder_id)


class StuVol(ModelMixIn, db.Model):
    __tablename__ = 'stu_vol'

    vol_id = Column(Integer, primary_key=True)
    stu_id = Column(Integer, primary_key=True)
    status = Column(SmallInteger)
    thought = Column(String(1024))
    reason = Column(String(64))
    reward = Column(Integer)

    @property
    def pics(self):
        return list_or_error(Picture.query.filter_by(stu_id=self.stu_id, vol_id=self.vol_id).select('hash', type='extension'))

    @property
    def stu(self):
        return User.query.get(self.stu_id)

    @property
    def stu_name(self):
        return User.query.get(self.stu_id).name
    
    @property
    def vol(self):
        return Volunteer.query.get(self.vol_id)

    @property
    def vol_name(self):
        return self.vol.name


class ClassVol(ModelMixIn, db.Model):
    __tablename__ = 'class_vol'

    vol_id = Column(Integer, primary_key=True)
    cls_id = Column(Integer, primary_key=True, name='class_id')
    max = Column(Integer)

    @property
    def now(self):
        return count(StuVol.query.filter_by(vol_id=self.vol_id), lambda sv: sv.stu.cls_id == self.cls_id)


class Picture(ModelMixIn, db.Model):
    __tablename__ = 'picture'

    vol_id = Column(Integer, primary_key=True)
    stu_id = Column(Integer, primary_key=True)
    hash = Column(String(32), primary_key=True)
    extension = Column(String(5))


class UserNotice(ModelMixIn, db.Model):
    __tablename__ = 'user_notice'

    user_id = Column(Integer, primary_key=True)
    notice_id = Column(Integer, primary_key=True)


class ClassNotice(ModelMixIn, db.Model):
    __tablename__ = 'class_notice'

    cls_id = Column(Integer, primary_key=True, name='class_id')
    notice_id = Column(Integer, primary_key=True)


class SchoolNotice(ModelMixIn, db.Model):
    __tablename__ = 'school_notice'

    notice_id = Column(Integer, primary_key=True)


class Log(ModelMixIn, db.Model):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, autoincrement=True)

class UserMapping(ModelMixIn, db.Model):
    __tablename__ = 'user_mapping'
    fake_id = Column(String(32), primary_key=True)
    real_id = Column(Integer)