from itertools import chain
from functools import wraps
import datetime
import json

from flask_sqlalchemy.query import Query
from sqlalchemy.orm import Query as _Query

from zvms import db
from zvms.res import *


class _QueryProperty:
    def __get__(self, obj, cls):
        return Query(db.session().query(cls))


def foo(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, '__iter__'):
            return (func(i, *args, **kwargs) for i in self)
        return func(self, *args, **kwargs)
    return wrapper


@foo
def select(self, *cols, **aliases):
    return dict(zip(chain(cols, aliases.values()), map(self.__getattribute__, chain(cols, aliases.keys()))))


@foo
def update(self, **updates):
    for k, v in updates.items():
        if hasattr(v, '__call__'):
            v = v(getattr(self, k))
        setattr(self, k, v)
    self.on_update()


@foo
def insert(self):
    db.session.add(self)
    db.session.flush()
    self.on_insert()
    return self


def incr(amount):
    return lambda x: x + amount


def select_value(self, col):
    return map(lambda x: getattr(x, col), self)



def list_or_error(self, message='未查询到相关信息'):
    ret = list(self)
    # 如果未查询到结果时需要404的话把注释去掉
    # if not ret:
    #     raise ZvmsError(404, message)
    return ret


class Query:
    select = select
    update = update
    insert = insert
    select_value = select_value

    def delete(self):
        for item in self:
            item.on_delete()
        self.__query.delete()

    def __init__(self, query):
        self.__query = query

    def get_or_error(self, ident, message='未查询到相关数据', code=404):
        ret = self.__query.get(ident)
        if not ret:
            raise ZvmsError(code, message)
        return ret

    def first_or_error(self, message='未查询到相关数据', code=404):
        ret = self.__query.first()
        if not ret:
            raise ZvmsError(code, message)
        return ret

    def one_or_error(self, message='未查询到相关数据', code=404):
        ret = self.__query.one()
        if not ret:
            raise ZvmsError(code, message)
        return ret

    def __iter__(self):
        return self.__query.__iter__()

    def __getattr__(self, *args, **kwargs):
        return Query.__deco(getattr(self.__query, *args, **kwargs))

    def __deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            return Query(ret) if isinstance(ret, _Query) else ret
        return wrapper


class ModelMixIn:
    select = select
    update = update
    insert = insert

    def on_insert(self):
        pass

    def on_update(self):
        pass

    def on_delete(self):
        pass

    query = _QueryProperty()


def success(message, **kwresult):
    ret = {'type': 'SUCCESS', 'message': message} | kwresult
    db.session.commit()
    return json.dumps(ret)


def error(code, message):
    db.session.rollback()
    return json.dumps({'type': 'ERROR', 'message': message}), code


def success(message, *result, **kwresult):
    ret = {'type': 'SUCCESS', 'message': message}
    if result:
        ret['result'] = result[0]
    elif kwresult:
        ret['result'] = kwresult
    db.session.commit()
    return json.dumps(ret)


class ZvmsError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


def try_parse_time(str):
    try:
        return datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ZvmsError(400, '请求接口错误: 非法的时间字符串')


def auth_self(id, token_data, message):
    if id != token_data['id'] and not (token_data['auth'] & Categ.SYSTEM):
        raise ZvmsError(403, message)


def auth_cls(cls, token_data, message='权限不足: 不能审核其他班级'):
    if cls != token_data['cls'] and not (token_data['auth'] & Categ.SYSTEM):
        raise ZvmsError(403, message)


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

def parse(json):
    return {
        int: lambda: 'number(int)',
        float: lambda: 'number(float)',
        bool: lambda: 'boolean',
        type(None): lambda: 'null',
        str: lambda: f'string({len(json)})',
        list: lambda: '[' + ', '.join(map(parse, json)) + ']',
        dict: lambda: '{' +
        ', '.join(
            map(lambda p: f'"{p[0]}": {parse(p[1])}', json.items())) + '}'
    }.get(type(json))()


def interface_error(expected, found):
    return json.dumps({'type': 'ERROR', 'message': '请求接口错误', 'expected': str(expected), 'found': parse(found)})
