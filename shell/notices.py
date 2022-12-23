from shell import App
from req import req

notices = App('notices', '通知管理:')

@notices.route('notice -f: 发送者 <id:int> -t: 目标用户 <id:int> -c: 目标班级 <id:int> -s: 学校通知')
def search_notices(**kwargs):
    '''搜索通知'''
    url = '/notices?' + '&'.join(
        (f'{k}={v[0]}' if v else f'{k}=_' for k, v in kwargs.items())
    )
    res = req.get(url)
    if res:
        for i in res:
            print('''id: {id}
发送者: {sender}
标题: {title}
{content}
过期于{deadtime}'''.format(**i))

@notices.route('notice send <int:type> <title> <deadtime> -m: 正文 <content> -f: 存放正文的文件路径 <file> -t: 目标 <int:target>')
def send_notice(type, title, deadtime, **kwargs):
    '''发送通知'''
    if 'm' in kwargs:
        content = kwargs['m'][0]
    elif 'f' in kwargs:
        try:
            with open(kwargs['f'][0], encoding='utf-8') as f:
                content = f.read()
        except:
            print('文件读取失败')
            return
    else:
        print('必须指定-m和-f选项中的一个')
        return
    if 't' in kwargs:
        target = kwargs['t'][0]
    else:
        target = None
    req.post('/notices', title=title, content=content, deadtime=deadtime, type=type, target=target)

@notices.route('notice del <int:id>')
def delete_notice(id):
    '''删除通知'''
    req.delete(f'/notices/{id}')

@notices.route('notice mod <int:id> <title> <deadtime> -m: 正文 <content> -f: 存放正文的文件路径 <file>')
def modify_notice(id, title, deadtime, **kwargs):
    '''修改通知'''
    if 'm' in kwargs:
        content = kwargs['m'][0]
    elif 'f' in kwargs:
        try:
            with open(kwargs['f'][0], encoding='utf-8') as f:
                content = f.read()
        except:
            print('文件读取失败')
    else:
        print('必须指定-m和-f选项中的一个')
        return
    req.put(f'/notices/{id}', title=title, content=content, deadtime=deadtime)