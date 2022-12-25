from base64 import b64encode
import webbrowser as browser

from shell import App
from req import req
from util import *

thoughts = App('thoughts', '感想管理')

@thoughts.route('thought -c: 班级 <int:id> -S: 状态 <int:status> -s: 学生 <int:id> -v: 义工 <int:id>')
def search_thoughts(**kwargs):
    '''获取感想列表'''
    res = req.get(f'/thoughts?{search(kwargs)}')
    thought_status = ('', '', '未提交', '等待初审', '等待终审', '通过', '拒绝')
    if res:
        for i in res:
            print('''学生: {stuName}({stuId})
义工: {volName}({volId})
状态: {thought_status}
'''.format(**i, thought_status=thought_status[i['status']]))

@thoughts.route('thought <int:stuId> <int:volId> -s <int:status> -m <thought> -f <file> -r <reason> *pics path')
def thought(stuId, volId, **kwargs):
    '''获取感想详细详细/提交感想/审核感想'''
    if not kwargs:
        res = req.get(f'/thoughts/{stuId}/{volId}')
        if res:
            if 'thought' in res:
                print(f'感想{res["thought"]}')
            if 'reason' in res:
                print(f'打回原因: {res["reason"]}')
            if 'reward' in res:
                print(f'报酬: {res["reward"]}')
            if 'pics' in res:
                browser.open(' '.join((f'http://127.0.0.1:1145/static/pics/{i}.jpg'for i in res['pics'])))
    args = {'pics': []}
    tmp = morf(kwargs, False)
    if tmp:
        args['thought'] = tmp
    for i in kwargs['pics']:
        try:
            with open(i['path'], 'rb') as f:
                args['pics'].append(b64encode(f.read()))
        except:
            print(App.config['failed_to_open'])
    if 'r' in kwargs:
        args['reason'] = kwargs['r']
    if 's' in kwargs:
        args['status'] = kwargs['s']
    req.patch(f'/thoughts/{stuId}/{volId}', **args)