from shell import App
from req import req
from util import morf, search

notice = App('notice', '通知管理:')

@notice.route('notice search -from: 发送者 <id:int> -to: 目标用户 <id:int> -cls: 目标班级 <id:int> -school: 学校通知')
def search_notices(**kwargs):
    '''搜索通知'''
    res = req.get(f'/notice/search?{search(kwargs)}')
    if res:
        for i in res:
            print('''id: {id}
发送者: {sender}
标题: {title}
{content}
过期于{deadtime}'''.format(**i))

@notice.route('notice send <int:type> <title> <deadtime> -m: 正文 <content> -f: 存放正文的文件路径 <file> *targets int:target')
def send_notice(type, **kwargs):
    '''发送通知'''
    content = morf(kwargs, 'content')
    if content is not None:
        url = '/notice/send/' + ('user', 'class', 'school')[type - 1]
        kwargs['targets'] = [i['target'] for i in kwargs['targets']]
        req.post(url, **kwargs, content=content)

@notice.route('notice delete <int:id>')
def delete_notice(id):
    '''删除通知'''
    req.post(f'/notice/{id}/delete')

@notice.route('notice mododify <int:id> <title> <deadtime> -m: 正文 <content> -f: 存放正文的文件路径 <file>')
def modify_notice(**kwargs):
    '''修改通知'''
    content = morf(kwargs, 'content')
    if content is not None:
        req.post(f'/notice/{id}/modify', **kwargs, content=content)