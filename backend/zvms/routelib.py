from flask import request
from functools import wraps
from jwt.exceptions import InvalidSignatureError
from datetime import datetime
import json

from zvms import app, db
from zvms.res import AUTH
from zvms.util import ZvmsError, success, error
import zvms.tokenlib as tk

class Named:
    def __init__(self, raw, name):
        self.raw = raw
        self.name = name
    
    def __call__(self, json):
        return self.raw(json)

    def __str__(self):
        return self.name

Any = Named(lambda _: True, 'any')
Int = Named(lambda x: isinstance(x, int), 'number(int)')
Float = Named(lambda x: isinstance(x, float), 'number(float)')
Number = Named(lambda x: Int(x) or Float(x), 'number')
Boolean = Named(lambda x: isinstance(x, bool), 'boolean')
String = Named(lambda x: isinstance(x, str), 'string')
Null = Named(lambda x: x == None, 'null')

class Array:
    def __init__(self, sub, allow_empty=True):
        self.sub = sub
        self.allow_empty = allow_empty

    def __call__(self, json):
        if not isinstance(json, list):
            return False
        for i in json:
            if not self.sub(json):
                return False
        return self.allow_empty or len(json) > 0

    def __str__(self):
        return f'[ {self.sub}, ... ]{"" if self.allow_empty else "(不可为空)"}'

class Object:
    def __init__(self, **pairs):
        self.pairs = pairs

    def __call__(self, json):
        if not isinstance(json, dict):
            return False
        for k, v in self.pairs.items():
            if k not in json or not v(json[k]):
                return False
        return True

    def __str__(self):
        return '{ ' + ', '.join(map(lambda p: f'"{p[0]}": {p[1]}', self.pairs.items())) + ' }'

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


def route(*,rule, method='GET', impl_func, params=Any, auth=0xffff):
    app.add_url_rule(rule, methods=[method], view_func=deco(impl_func, params, auth))

# 不要听下面的注释, 现在已经没有装饰器了
# 以后把调试的代码写在这边，把一些公用的功能也可以移到这边
# 在所有函数名前面加上@Deco()
# 这样路由的函数直接返回一个字典就好了
def deco(impl, params, auth):
    @wraps(impl)
    def wrapper(*args,**kwargs):
        if request.method == 'GET':
            json_data = request.args
        else:
            try: # 为了防止空POST出锅
                json_data = json.loads(request.get_data().decode("utf-8"))
            except:
                json_data = {}
            
        token_data = {}
        if auth != None:
            try:
                token_data = request.headers.get('Authorization')
                if not token_data:
                    raise InvalidSignatureError()
                token_data = tk.read(token_data)
                if not tk.exists(token_data):
                    return json.dumps({'type':'ERROR', 'message':"Token失效, 请重新登陆"})
                if not (token_data['auth'] & (auth | AUTH.SYSTEM)):
                    return json.dumps({'type': 'ERROR', 'message': '权限不足'})
            except InvalidSignatureError as ex:
                return json.dumps({'type':'ERROR', 'message':"未获取到Token, 请重新登陆"})

        if not params(json_data):
            return json.dumps({'type': 'ERROR', 'message': '请求接口错误',
                'expected': str(params), 'found': parse(json_data)})

        try:
            with open('log.txt', 'a', encoding='utf-8') as f:
                if auth:
                    f.write(f'({token_data["id"]}) ')
                f.write(f'[{datetime.now()}] {request.method} {request.url}\n')
            return impl(*args, **kwargs, **json_data, token_data=token_data)
        except ZvmsError as ex:
            return error(ex.message)
    return wrapper
