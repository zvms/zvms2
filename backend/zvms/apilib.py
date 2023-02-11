from functools import wraps
from queue import Queue
from threading import Barrier
import datetime
import json

from flask import request
from jwt.exceptions import InvalidSignatureError

from zvms.typing.checker import Any
from zvms.res import Categ
from zvms.util import *
from zvms import app
import zvms.tokenlib as tk
import zvms.typing.structs as structs

def process_queue():
    with app.app_context():
        while True:
            while not queue.empty():
                task = queue.get()
                task.run()
                task.bar.wait()

queue = Queue()

class Task:
    def __init__(self, bar, func, args, kwargs, json_data, token_data):
        self.bar = bar
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.json_data = json_data
        self.token_data = token_data


    def run(self):
        self.result = self.func(*self.args, **self.kwargs, **self.json_data, token_data=self.token_data)


def api(*, rule, method='GET', params=Any, response=Any, auth=Categ.ANY):
    def wrapper(func):
        nonlocal params, response
        if isinstance(params, str):
            params = getattr(structs, params)
        if isinstance(response, str):
            response = getattr(structs, response)
        app.add_url_rule(rule, methods=[method], view_func=deco(func, params, response, auth))
        return func
    return wrapper

# 不要听下面的注释, 现在已经没有装饰器了
# 以后把调试的代码写在这边，把一些公用的功能也可以移到这边
# 在所有函数名前面加上@Deco()
# 这样路由的函数直接返回一个字典就好了
def deco(impl, params, response, auth):
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
                    return json.dumps({'type': 'ERROR', 'message': "Token失效, 请重新登陆"})
                if not auth.authorized(token_data['auth']):
                    return json.dumps({'type': 'ERROR', 'message': '权限不足'})
            except InvalidSignatureError as ex:
                return json.dumps({'type': 'ERROR', 'message': "未获取到Token, 请重新登陆"})
        try:
            with open('log.txt', 'a', encoding='utf-8') as f:
                if auth != Categ.NONE:
                    f.write(f'({token_data["id"]}) ')
                f.write(
                    f'[{datetime.datetime.now()}] {request.method} {request.url}\n')
            if not params(json_data):
                print(json.loads(interface_error(params, json_data)))
                print(json_data)
                return interface_error(params, json_data)
            bar = Barrier(2)
            task = Task(bar, impl, args, kwargs, json_data, token_data)
            queue.put(task)
            bar.wait()
            if not response(task.result.get('result')):
                return {'type': 'ERROR', 'message': '响应返回错误', 'expected': str(response), 'found': parse(task.result)}
            return json.dumps(task.result)
            ret = impl(*args, **kwargs, **json_data, token_data=token_data)
            if not response(ret.get('result')):
                return {'type': 'ERROR', 'message': '响应返回错误', 'expected': str(response), 'found': parse(ret)}
            return json.dumps(ret)
        except ZvmsError as ex:
            return json.dumps(error(ex.message))
    return wrapper
