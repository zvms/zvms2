from functools import wraps
from pprint import pprint
from threading import Lock
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

class ZvmsExit(KeyboardInterrupt): ...

class Api:
    counter_lock = Lock()
    counter = 0

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
                    return json.dumps({'type': 'ERROR', 'message': "Token失效, 请重新登陆"}), jsonHeader
                if not auth.authorized(token_data['auth']):
                    return json.dumps({'type': 'ERROR', 'message': '权限不足'}), jsonHeader
            except InvalidSignatureError as ex:
                return json.dumps({'type': 'ERROR', 'message': "未获取到Token, 请重新登陆"}), jsonHeader
        try:
            if __debug__:
                with Api.counter_lock:
                    Api.counter += 1
                    print('Api访问次数:', Api.counter)
                    if Api.counter % 10000 == 0:
                        Report(
                            reporter=0,
                            content=f'喜报: Api访问量达到{Api.counter}',
                            time=datetime.datetime.now()
                        )
                with open('log.txt', 'a', encoding='utf-8') as f:
                    t = datetime.datetime.now().replace(microsecond=0)
                    s = f'{t}[{request.remote_addr}]'
                    if auth != Categ.NONE:
                        s+=f'({token_data["id"]})'
                    s+= f'[{request.method}]{request.path}'
                    print(s)
                    f.write(s+'\n')
            check(params, json_data, '传入的数据错误')
            ret = impl(*args, **kwargs, **json_data, token_data=token_data)
            result = ret.get('result')
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
            if __debug__:
                pprint(dict)
            Report(
                time=datetime.datetime.now(),
                reporter=0,
                content='(用户: {}) {}: {}'.format(token_data['id'] if id in token_data else '<未登录>', ex.message, json.dumps(dict, indent=4))
            ).insert()
            return json.dumps(error(ex.message) | dict)
    return wrapper
