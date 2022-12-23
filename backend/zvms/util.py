from flask_sqlalchemy.query import Query
from sqlalchemy.sql import and_
import datetime

from zvms import db
from zvms.res import *
import json

def success(message, *result, **kwresult):
    ret = {'type': 'SUCCESS', 'message': message}
    if result:
        ret['result'] = result[0]
    elif kwresult:
        ret['result'] = kwresult
    db.session.commit()
    return json.dumps(ret)

def error(message):
    return json.dumps({'type': 'ERROR', 'message': message})

class ZvmsError(Exception):
    def __init__(self, message):
        self.message = message

def select(self, *cols, **aliases):
    return dict(zip(cols + tuple(aliases.values()), map(self.__getattribute__, cols + tuple(aliases.keys()))))

def update(self, **kwargs):
    for k, v in kwargs.items():
        self.__setattr__(k, v)

def insert(self):
    db.session.add(self)
    db.session.flush()
    return self

def get_or_error(self, *args):
    ret = self.get(*args)
    if ret:
        return ret
    raise ZvmsError('未查询到相关数据')

def __init__(self, **kwargs):
    for k, v in kwargs.items():
        self.__setattr__(k, v)

# 我管这种东西叫扩展方法
# 我知道这很不好, 但写起来是真的爽
# 如果不合适的话可以改掉

db.Model.select = select
db.Model.update = update
db.Model.insert = insert
db.Model.__init__ = __init__

def apply(func):
    return lambda self, *cols, **aliases: map(lambda x: func(x, *cols, **aliases), self)

Query.select = apply(select)
Query.update = apply(update)
Query.select_value = apply(db.Model.__getattribute__)
Query.get_or_error = get_or_error

def try_parse_time(str):
    try:
        return datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ZvmsError('请求接口错误: 非法的时间字符串')

def auth_self(id, token_data, message):
    print(id, token_data['id'], (token_data['auth'] & AUTH.SYSTEM))
    if id != token_data['id'] and not (token_data['auth'] & AUTH.SYSTEM):
        raise ZvmsError(message)