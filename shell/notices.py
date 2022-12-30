from shell import App
from req import req
from util import morf, search

notices = App('notices', '通知管理:')

@notices.route('notice -f: 发送者 <id:int> -t: 目标用户 <id:int> -c: 目标班级 <id:int> -s: 学校通知')
def search_notices(**kwargs):
    '''搜索通知'''
    res = req.get(f'/notices?{search(kwargs)}')
    if res:
        for i in res:
            print('''id: {id}
发送者: {sender}
标题: {title}
{content}
过期于{deadtime}'''.format(**i))

@notices.route('notice send <int:type> <title> <deadtime> -m: 正文 <content> -f: 存放正文的文件路径 <file> *targets int:target')
def send_notice(**kwargs):
    '''发送通知'''
    content = morf(kwargs, 'content')
    if content is not None:
        if kwargs['targets']:
            kwargs['targets'] = [i['target'] for i in kwargs['targets']]
        else:
            kwargs['targets'] = None
        req.post('/notices', **kwargs, content=content)

@notices.route('notice del <int:id>')
def delete_notice(id):
    '''删除通知'''
    req.delete(f'/notices/{id}')

@notices.route('notice mod <int:id> <title> <deadtime> -m: 正文 <content> -f: 存放正文的文件路径 <file>')
def modify_notice(**kwargs):
    '''修改通知'''
    content = morf(kwargs, 'content')
    if content is not None:
        req.put(f'/notices/{id}', **kwargs, content=content)