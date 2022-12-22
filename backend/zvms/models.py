from operator import attrgetter
import datetime
import hashlib

from zvms import db
from zvms.res import *

class Class(db.Model):
    __tablename__ = 'class'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5))

    @property
    def members(self):
        return User.query.filter_by(clz_id=self.id)

    @property
    def notices_received(self):
        return Notice.query.filter_by(id.in_(ClassNotice.query.filter_by(clz_id=self.id).select_value('notice_id')))

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5))
    clz_id = db.Column(db.Integer, name='class')
    pwd = db.Column(db.String(32))
    auth = db.Column(db.Integer)

    @property
    def notices_sent(self):
        return Notice.query.filter_by(sender=self.id)

    @property
    def notices_received(self):
        return Notice.query.filter_by(id.in_(UserNotice.query.filter_by(user_id=self.id).select_value('notice_id')))

    @property
    def inside(self):
        return 

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

class StuVol(db.Model):
    __tablename__ = 'stu_vol'

    stu_id = db.Column(db.Integer, primary_key=True)
    vol_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.SMALLINT)
    thought = db.Column(db.String(1024))
    reason = db.Column(db.String(1024))
    reward = db.Column(db.Integer)

class ClassVol(db.Model):
    __tablename__ = 'class_vol'

    clz_id = db.Column(db.Integer, primary_key=True)
    vol_id = db.Column(db.Integer, primary_key=True)
    max = db.Column(db.Integer)

class Picture(db.Model):
    __tablename__ = 'picture'

    stu_id = db.Column(db.Integer, primary_key=True)
    vol_id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(32))

class UserNotice(db.Model):
    __tablename__ = 'user_notice'

    user_id = db.Column(db.Integer, primary_key=True)
    notice_id = db.Column(db.Integer, primary_key=True)

class ClassNotice(db.Model):
    __tablename__ = 'class_notice'

    clz_id = db.Column(db.Integer, primary_key=True)
    notice_id = db.Column(db.Integer, primary_key=True)

class SchoolNotice(db.Model):
    __tablename__ = 'school_notice'

    notice_id = db.Column(db.Integer, primary_key=True)

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)