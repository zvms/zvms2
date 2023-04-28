from functools import wraps
from pprint import pprint
import datetime
import json
import re

from flask import request
from jwt.exceptions import InvalidSignatureError

from zvms.typing.checker import Any
from zvms.res import Categ
from zvms.util import *
from zvms.models import *
from zvms.typing.checker import CheckerError
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

jsonHeader = {"Content-Type": "application/json ; charset=utf-8"}

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
                    return json.dumps({'type': 'ERROR', 'message': "Token失效, 请重新登陆"}), jsonHeader
                if not auth.authorized(token_data['auth']):
                    print('权限不足')
                    return json.dumps({'type': 'ERROR', 'message': '权限不足'}), jsonHeader
            except InvalidSignatureError as ex:
                print('未获取到Token', auth, request.path)
                return json.dumps({'type': 'ERROR', 'message': "未获取到Token, 请重新登陆"}), jsonHeader
        try:
            with open('log.txt', 'a', encoding='utf-8') as f:
                t = datetime.datetime.now().replace(microsecond=0)
                s = f'{t}[{request.remote_addr}]'
                if auth != Categ.NONE:
                    s+=f'({token_data["id"]})'
                s+= f'[{request.method}]{request.path}'
                print(s)
                f.write(s+'\n')
            # if not params.check(json_data):
            #     return interface_error(params, json_data), jsonHeader
            check(params, json_data, '传入的数据错误')
            ret = impl(*args, **kwargs, **json_data, token_data=token_data)
            result = ret.get('result')
            # if ret['type'] == 'SUCCESS' and not response.check(result):
            #     return {'type': 'ERROR', 'message': '服务器返回的数据错误', 'expected': response.as_json(), 'found': parse(result)}, jsonHeader
            if ret['type'] == 'SUCCESS':
                check(response, result, '服务器返回的数据错误')
            return json.dumps(ret), jsonHeader
        except ZvmsError as ex:
            return json.dumps(error(ex.message)), jsonHeader
        except CheckerError as ex:
            dict = {
                'where': ex.args[0],
                'expected': ex.args[1],
                'found': ex.args[2]
            }
            Report(
                time=datetime.datetime.now(),
                reporter=0,
                content='(用户: {}) {}: {}'.format(token_data['id'] if id in token_data else '<未登录>', ex.message, json.dumps(dict, indent=4))
            ).insert()
            return json.dumps(error(ex.message) | dict)
    return wrapper
