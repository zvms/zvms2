from base64 import b64encode
import webbrowser as browser

from shell import App
from req import req
from util import morf, search, md5ify

thought = App('thought', '感想管理')

@thought.route('thought search -cls: 班级 <int:id> -status: 状态 <int:status> -student: 学生 <int:id> -volunteer: 义工 <int:id>')
def search_thoughts(**kwargs):
    '''获取感想列表'''
    res = req.get(f'/thought/search?{search(kwargs)}')
    thought_status = ('', '', '未提交', '草稿', '等待初审', '等待终审', '通过', '拒绝')
    if res:
        for i in res:
            print('''学生: {stuName}({stuId})
义工: {volName}({volId})
状态: {thought_status}
'''.format(**i, thought_status=thought_status[i['status']]))

@thought.route('thought <int:volId> <int:stuId>')
def get_thought_info(volId, stuId):
    '''获取感想详细信息'''
    possible_results = {
        'reason': '打回原因',
        'reward': '报酬',
        'thought': '感想'
    }
    res = req.get(f'/thought/{volId}/{stuId}')
    if res:
        for k, v in possible_results.items():
            if k in res:
                print(f'{v}: {res[k]}')
        for pic in res.get('pics', ()):
            browser.open(f'http://127.0.0.1:1145/static/pics/{pic}.jpg')

def _upload(volId, stuId, pics, kwargs, url):
    content = morf(kwargs, 'content')
    for i, pic in enumerate(pics):
        try:
            with open(pic['path'], 'rb') as f:
                pics[i] = b64encode(f.read()).decode()
        except Exception as ex:
            print(ex)
            return
    if content:
        req.post(url.format(volId=volId, stuId=stuId), thought=content, pictures=pics)


@thought.route('thought save <int:volId> <int:stuId> -m <content> -f <file> *pics path')
def save_thought(volId, stuId, pics, **kwargs):
    '''保存感想草稿'''
    _upload(volId, stuId, pics, kwargs, '/thought/{volId}/{stuId}/save')

@thought.route('thought submit <int:volId> <int:stuId> -m <content> -f <file> *pics path')
def submit_thought(volId, stuId, pics, **kwargs):
    '''提交感想'''
    _upload(volId, stuId, pics, kwargs, '/thought/{volId}/{stuId}/submit')

@thought.route('thought audit first <int:volId> <int:stuId>')
def first_audit_thought(volId, stuId):
    '''初审感想'''
    req.post(f'/thought/{volId}/{stuId}/audit/first')

@thought.route('thought audit final <int:volId> <int:stuId>')
def final_audit_thought(volId, stuId):
    '''终审感想'''
    req.post(f'/thought/{volId}/{stuId}/audit/final')

@thought.route('thought repulse <int:volId> <int:stuId> <reason>')
def repulse_thought(volId, stuId, reason):
    '''打回感想'''
    req.post(f'/thought/{volId}/{stuId}/repulse', reason=reason)