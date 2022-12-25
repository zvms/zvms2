import datetime
import json

from flask_sqlalchemy.query import Query
from sqlalchemy.sql import and_

from zvms import db
from zvms.res import *

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

def get_or_error(self, args, message='未查询到相关数据'):
    ret = self.get(args)
    if ret:
        return ret
    raise ZvmsError(message)

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

select_value = apply(object.__getattribute__)

Query.select = apply(select)
Query.update = apply(update)
Query.select_value = select_value
Query.get_or_error = get_or_error

def try_parse_time(str):
    try:
        return datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ZvmsError('请求接口错误: 非法的时间字符串')

def auth_self(id, token_data, message):
    if id != token_data['id'] and not (token_data['auth'] & AUTH.SYSTEM):
        raise ZvmsError(message)

def auth_cls(cls, token_data, message='权限不足: 不能审核其他班级'):
    if cls != token_data['cls'] and not (token_data['auth'] & AUTH.SYSTEM):
        raise ZvmsError(message)

def count(seq, predicate):
    ret = 0
    for i in seq:
        if predicate(i):
            ret += 1
    return ret

def exists(seq, predicate):
    for i in seq:
        if predicate(i):
            return True
    return False

class Named:
    def __init__(self, raw, name):
        self.raw = raw
        self.name = name
    
    def __call__(self, json):
        return self.raw(json)

    def __str__(self):
        return self.name

# 下面的谓词开头大写是因为它们有"类型"的含义(虽然实际上不是), 同时还避免了与内置函数重名
Any = Named(lambda _: True, 'any')
Int = Named(lambda x: isinstance(x, int), 'number(int)')
Float = Named(lambda x: isinstance(x, float), 'number(float)')
Number = Named(lambda x: isinstance(x, (int, float)), 'number')
Boolean = Named(lambda x: isinstance(x, bool), 'boolean')
String = Named(lambda x: isinstance(x, str), 'string')
Null = Named(lambda x: x is None, 'null')

class Array:
    def __init__(self, sub, allow_empty=False):
        self.sub = sub
        self.allow_empty = allow_empty

    def __call__(self, json):
        if not isinstance(json, list):
            return False
        for i in json:
            if not self.sub(i):
                return False
        return self.allow_empty or json

    def __str__(self):
        return f'[{self.sub}, ...]{"" if self.allow_empty else "(不可为空)"}'

class Object:
    def __init__(self, **members):
        self.members = members

    def __call__(self, json):
        if not isinstance(json, dict):
            return False
        for k, v in self.members.items():
            if k not in json or not v(json[k]):
                return False
        return True

    def __str__(self):
        return '{' + ', '.join(map(lambda p: f'"{p[0]}": {p[1]}', self.members.items())) + '}'

class Extends(Object):
    def __init__(self, super, **members):
        self.members = super.members | members

class Option:
    def __init__(self, *options):
        self.options = options

    def __call__(self, json):
        for i in self.options:
            if i(json):
                return True
        return False

    def __str__(self):
        return '(' + ' | '.join(map(str, self.options)) + ')'

class Group:
    def __init__(self, *items):
        self.items = items

    def __call__(self, json):
        for i in self.items:
            if not i(json):
                return False
        return True

    def __str__(self):
        return '(' + ' & '.join(map(str, self.options)) + ')'

def parse(json):
    return {
        int: lambda: 'number(int)',
        float: lambda: 'number(float)',
        bool: lambda: 'boolean',
        type(None): lambda: 'null',
        str: lambda: 'string',
        list: lambda: '[' + ', '.join(map(parse, json)) + ']',
        dict: lambda: '{' + ', '.join(map(lambda p: f'"{p[0]}": {parse(p[1])}', json.items())) + '}'
    }.get(type(json))()

def interface_error(expected, found):
    return json.dumps({'type': 'ERROR', 'message': '请求接口错误', 'expected': str(expected), 'found': parse(found)})