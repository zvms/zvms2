from functools import wraps, partial
from typing import Callable, Iterable
import itertools
import hashlib
import datetime
import json
import re

from flask_sqlalchemy.query import Query
from sqlalchemy.orm import Query as _Query
from mistune import Markdown, HTMLRenderer

from zvms import db
from zvms.res import *

markdown = Markdown(HTMLRenderer())
rule_remove_links = re.compile(r'<a.*?>(.*?)</a>', re.S)

def render_markdown(md):
    return rule_remove_links.sub(r'<a>\1</a>', markdown.parse(md))

def md5ify(str):
    md5 = hashlib.md5()
    md5.update(str.encode())
    return md5.hexdigest()


class _QueryProperty:
    def __get__(self, obj, cls):
        return Query(db.session().query(cls))

def foo(func):
    return wraps(func)(lambda self, *args, **kwargs: 
        map(self, lambda t: func(t, *args, **kwargs)) if isinstance(self, Iterable) else
        func(self, *args, **kwargs))

def foreach(iterable, func):
    ret = None
    for item in iterable:
        ret = func(item)
    return ret

def bar(func):
    return wraps(func)(lambda self, *args, **kwargs: 
        foreach(self, lambda t: func(t, *args, **kwargs)) if isinstance(self, Iterable) else
        func(self, *args, **kwargs))


@foo
def select(self, *cols, **aliases):
    return dict(zip(chain(cols, aliases.values()), map(self.__getattribute__, chain(cols, aliases.keys()))))

@foo
def select(self, *cols, **aliases):
    return dict(chain(zip(cols, map(partial(getattr, self), cols)), 
        ((((k, v(getattr(self, k)) if isinstance(v, Callable) else
        (v, getattr(self, k)) if isinstance(v, str) else
        (v[1], v[0](getattr(self, k))) if isinstance(v, tuple) else
        (k, v)) for k, v in aliases.items())))))

@bar
def update(self, **updates):
    for k, v in updates.items():
        if isinstance(v, Callable):
            v = v(getattr(self, k))
        setattr(self, k, v)
    self.on_update()
    return self


def insert(self):
    db.session.add(self)
    db.session.flush()
    self.on_insert()
    return self

class map(__builtins__.map):
    def __init__(self, iterable, func):
        super().__init__(func, iterable)

    select = select
    select_value = select_value
    update = update

class filter(__builtins__.filter):
    def __init__(self, iterable, match):
        super().__init__(match, iterable)

    select = select
    select_value = select_value
    update = update

class chain(itertools.chain):
    select = select
    select_value = select_value
    update = update


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

class Wrapper:
    def __init__(self, raw):
        self.raw = raw

    def __getattr__(self, name):
        return (lambda t: type(self)(t) if isinstance(t, type(self).T) else self.__deco(t))(getattr(self.raw, name))

    def __iter__(self):
        return iter(self.raw)

    def __deco(self, func):
        return wraps(lambda *args, **kwargs: (lambda t: type(self)(t) if isinstance(t, type(self).T) else t)(func(*args, **kwargs)))

class ZvmsWrapper:
    select = select
    update = update
    select_value = select_value

class Query(ZvmsWrapper):
    T = _Query

    def delete(self):
        for item in self:
            item.on_delete()
        self.raw.delete()

    def get_or_error(self, ident, message='未查询到相关数据'):
        ret = self.raw.get(ident)
        if not ret:
            raise ZvmsError(message)
        return ret

    def first_or_error(self, message='未查询到相关数据'):
        ret = self.raw.first()
        if not ret:
            raise ZvmsError(message)
        return ret

    def one_or_error(self, message='未查询到相关数据'):
        ret = self.raw.one()
        if not ret:
            raise ZvmsError(message)
        return ret

    # def paginate(self, **kwargs):
    #     return Pagination(self.raw.paginate(**kwargs))

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


def error(message):
    db.session.rollback()
    return {'type': 'ERROR', 'message': message}


def success(message, *result, **kwresult):
    ret = {'type': 'SUCCESS', 'message': message}
    if result:
        ret['result'] = result[0]
    elif kwresult:
        ret['result'] = kwresult
    db.session.commit()
    return ret


class ZvmsError(Exception):
    def __init__(self, message):
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
    return json.dumps({'type': 'ERROR', 'message': '请求接口错误', 'expected': str(expected), 'found': parse(found)})