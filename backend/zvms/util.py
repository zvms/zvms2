from itertools import chain
from functools import wraps
from typing import Callable, Iterable
import hashlib
import datetime
import json

from flask_sqlalchemy.query import Query
from sqlalchemy.orm import Query as _Query

from zvms import db
from zvms.res import *

def md5ify(str):
    md5 = hashlib.md5()
    md5.update(str.encode())
    return md5.hexdigest()


class _QueryProperty:
    def __get__(self, obj, cls):
        return Query(db.session().query(cls))


def foo(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if isinstance(self, Iterable):
            return (func(i, *args, **kwargs) for i in self)
        return func(self, *args, **kwargs)
    return wrapper


@foo
def select(self, *cols, **aliases):
    return dict(zip(chain(cols, aliases.values()), map(self.__getattribute__, chain(cols, aliases.keys()))))


@foo
def update(self, **updates):
    for k, v in updates.items():
        if isinstance(v, Callable):
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
    #     raise ZvmsError(message)
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

    def get_or_error(self, ident, message='未查询到相关数据'):
        ret = self.__query.get(ident)
        if not ret:
            raise ZvmsError(message)
        return ret

    def first_or_error(self, message='未查询到相关数据'):
        ret = self.__query.first()
        if not ret:
            raise ZvmsError(message)
        return ret

    def one_or_error(self, message='未查询到相关数据'):
        ret = self.__query.one()
        if not ret:
            raise ZvmsError(message)
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
        raise ZvmsError('请求接口错误: 非法的时间字符串')


def auth_self(id, token_data, message):
    if id != token_data['id'] and not (token_data['auth'] & Categ.SYSTEM):
        raise ZvmsError(message)


def auth_cls(cls, token_data, message='权限不足: 不能审核其他班级'):
    if cls != token_data['cls'] and not (token_data['auth'] & Categ.SYSTEM):
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

def parse(json):
    if isinstance(json, int):
        return 'number(int)'
    if isinstance(json, float):
        return 'number(float)'
    if isinstance(json, bool):
        return 'boolean'
    if isinstance(json, type(None)):
        return 'null'
    if isinstance(json, str):
        return f'string({len(json)})'
    if isinstance(json, (list, tuple)):
        return '[' + ', '.join(map(parse, json)) + ']'
    if isinstance(json, dict):
        return '{' + ', '.join(map(lambda p: f'"{p[0]}": {parse(p[1])}', json.items())) + '}'


def interface_error(expected, found):
    print(expected, found)
    return json.dumps({'type': 'ERROR', 'message': '请求接口错误', 'expected': str(expected), 'found': parse(found)})