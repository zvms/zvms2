import datetime
import json
from functools import wraps

import zvms.tokenlib as tk
from flask import request
from jwt.exceptions import InvalidSignatureError
from zvms.res import *
from zvms.utils import *

from zvms import app, db


def route(*, rule, method='GET', impl_func, params, auth):
    app.add_url_rule(rule, methods=[method],
                     view_func=deco(impl_func, params, auth))


def route_get(*, rule, impl_func, params, auth):
    app.add_url_rule(rule, methods=['GET'],
                     view_func=deco(impl_func, params, auth))


def route_post(*, rule, impl_func, params, auth):
    app.add_url_rule(rule, methods=['POST'],
                     view_func=deco(impl_func, params, auth))


def route_put(*, rule, impl_func, params, auth):
    app.add_url_rule(rule, methods=['PUT'],
                     view_func=deco(impl_func, params, auth))


def route_delete(*, rule, impl_func, params, auth):
    app.add_url_rule(rule, methods=['DELETE'],
                     view_func=deco(impl_func, params, auth))


def route_patch(*, rule, impl_func, params, auth):
    app.add_url_rule(rule, methods=['PATCH'],
                     view_func=deco(impl_func, params, auth))

# 不要听下面的注释, 现在已经没有装饰器了
# 以后把调试的代码写在这边，把一些公用的功能也可以移到这边
# 在所有函数名前面加上@Deco()
# 这样路由的函数直接返回一个字典就好了


def deco(impl, params, auth):
    @wraps(impl)
    def wrapper(*args, **kwargs):
        if request.method in ('GET', 'DELETE'):
            json_data = request.args
            if 'timestamp' in json_data:
                del json_data['timestamp']
        else:
            try:  # 为了防止空POST出锅
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
                    return json.dumps({'type': 'ERROR', 'message': "Token失效, 请重新登陆"})
                if not auth.authorized(token_data['auth']):
                    return json.dumps({'type': 'ERROR', 'message': '权限不足'})
            except InvalidSignatureError as ex:
                return json.dumps({'type': 'ERROR', 'message': "未获取到Token, 请重新登陆"})
        if not params(json_data):
            return interface_error(params, json_data)
        try:
            with open('log.txt', 'a', encoding='utf-8') as f:
                if auth:
                    f.write(f'({token_data["id"]}) ')
                f.write(
                    f'[{datetime.datetime.now()}] {request.method} {request.url}\n')
            return impl(*args, **kwargs, **json_data, token_data=token_data)
        except ZvmsError as ex:
            return error(ex.message)
    return wrapper
