from shell import App
from req import req
from util import morf, search

volunteers = App('volunteers', '义工管理:')

@volunteers.route('vol -h: 举办者 <int:id> -c: 班级 <int:id> -s: 学生 <int:id> -n: 名称 <name>')
def search_volunteers(**kwargs):
    '''搜索义工'''
    url = f'/volunteers?{search(kwargs)}'
    res = req.get(url.encode('gbk').decode('gbk'))
    if res:
        for i in res:
            print('{id} {name} 过期于{time}'.format(**i))

@volunteers.route('vol <int:id>')
def get_volunteer_info(id):
    '''获取义工详细信息'''
    res = req.get(f'/volunteers/{id}')
    vol_types = {1: '校内', 2: '校外', 3: '大型'}
    if res:
        print('''{name}
{description}
过期于{time}
举办者: {holder}
类型: {vol_type}
报酬: {reward}
'''.format(**res, vol_type=vol_types[res['type']]))

@volunteers.route('vol create <name> <time> <int:type> <int:reward> -m: 描述 <description> -f: 存放描述的文件路径 <file>')
def create_volunteer(**kwargs):
    '''创建义工'''
    description = morf(kwargs)
    if description is not None:
        req.post('/volunteers', **kwargs, description=description)

@volunteers.route('vol mod <int:id> <name> <time> <int:type> <int:reward> -m: 描述 <description> -f: 存放描述的文件路径 <file>')
def modify_volunteers(id, **kwargs):
    '''修改义工'''
    description = morf(kwargs)
    if description is not None:
        req.put(f'/volunteers/{id}', **kwargs, description=description)

@volunteers.route('vol del <int:id>')
def delete_volunteer(id):
    '''删除义工'''
    req.delete(f'/volunteers/{id}')