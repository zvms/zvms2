from functools import wraps
import traceback
import datetime
import json
import re

from flask import request
from jwt.exceptions import InvalidSignatureError

from zvms.typing.checker import Any
from zvms.res import Categ
from zvms.util import *
import zvms.tokenlib as tk
import zvms.typing.structs as structs


class Api:
    apis: list['Api'] = []
    rule_url_args = re.compile(r'\<.+?\>')

    def __init__(self, rule, method='GET', params=Any(), response=Any(), auth=Categ.ANY):
        self.rule = rule
        self.url_params = {}
        for arg in Api.rule_url_args.findall(rule):
            if arg.startswith('<int:'):
                self.url_params[arg[5:-1]] = 'number'
            else:
                self.url_params[arg[1:-1]] = 'string'
        self.method = method
        if isinstance(params, str):
            self.params = getattr(structs, params)()
        else:
            self.params = params
        if isinstance(response, str):
            self.response = getattr(structs, response)()
        else:
            self.response = response
        self.auth = auth

    def __call__(self, func):
        self.func = func
        Api.apis.append(self)

    def init_app(app):
        for api in Api.apis:
            app.add_url_rule(api.rule, methods=[api.method], view_func=deco(api.func, api.params, api.response, api.auth))

def deco(impl, params, response, auth):
    @wraps(impl)
    def wrapper(*args, **kwargs):
        if request.method in ('GET', 'DELETE'):
            json_data = request.args
            if 'timestamp' in json_data:
                del json_data['timestamp']
        else:
            try:
                json_data = json.loads(request.get_data().decode("utf-8"))
            except:
                json_data = {}
        if 'csrf_token' in json_data:
            del json_data['csrf_token']
        token_data = {}
        if auth != Categ.NONE:
            try:
                token_data = request.headers.get('Authorization')
                if not token_data:
                    raise InvalidSignatureError()
                token_data = tk.read(token_data)
                if not tk.exists(token_data):
                    print('Token失效')
                    return json.dumps({'type': 'ERROR', 'message': "Token失效, 请重新登陆"})
                if not auth.authorized(token_data['auth']):
                    print('权限不足')
                    return json.dumps({'type': 'ERROR', 'message': '权限不足'})
            except InvalidSignatureError as ex:
                print('未获取到Token')
                return json.dumps({'type': 'ERROR', 'message': "未获取到Token, 请重新登陆"})
        try:
            with open('log.txt', 'a', encoding='utf-8') as f:
                if auth != Categ.NONE:
                    print(f'({token_data["id"]})', end=' ')
                    f.write(f'({token_data["id"]}) ')
                print(f'[{datetime.datetime.now()}] {request.method} {request.url}')
                f.write(f'[{datetime.datetime.now()}] {request.method} {request.url}\n')
            if not params(json_data):
                print(json.loads(interface_error(params, json_data)))
                print(json_data)
                return interface_error(params, json_data)
            ret = impl(*args, **kwargs, **json_data, token_data=token_data)
            if not response(ret.get('result')):
                return {'type': 'ERROR', 'message': '响应返回错误', 'expected': str(response), 'found': parse(ret)}
            return json.dumps(ret)
        except ZvmsError as ex:
            return json.dumps(error(ex.message))
    return wrapper
