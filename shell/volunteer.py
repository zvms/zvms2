from shell import App
from req import req
from util import morf, search

volunteer = App('volunteer', '义工管理:')

@volunteer.route('vol search -holder: 举办者 <int:id> -cls: 班级 <int:id> -student: 学生 <int:id> -name: 名称 <name> -status: 状态 <status>')
def search_volunteers(**kwargs):
    '''搜索义工'''
    url = f'/volunteer/search?{search(kwargs)}'
    res = req.get(url)
    if res:
        for i in res:
            print('{id} {name} {audited}过审 过期于{time}'.format(audited='已' if i['status'] == 2 else '未', **i))

@volunteer.route('vol <int:id>')
def get_volunteer_info(id):
    '''获取义工详细信息'''
    res = req.get(f'/volunteer/{id}')
    vol_types = {1: '校内', 2: '校外', 3: '大型'}
    if res:
        print('''{name}
{description}
过期于{time}
举办者: {holder}
类型: {vol_type}
报酬: {reward}
参与者:
'''.format(**res, vol_type=vol_types[res['type']]))
        for i in res['joiners']:
            print('{name}({id})'.format(**i))

@volunteer.route('vol create <name> <time> <int:type> <int:reward> -m: 描述 <description> -f: 存放描述的文件路径 <file> *classes int:id int:max')
def create_volunteer(**kwargs):
    '''创建义工'''
    description = morf(kwargs)
    if description is not None:
        req.post('/volunteer/create', **kwargs, description=description)

@volunteer.route('vol modify <int:id> <name> <time> <int:type> <int:reward> -m: 描述 <description> -f: 存放描述的文件路径 <file> *classes int:id int:max')
def modify_volunteers(id, **kwargs):
    '''修改义工'''
    description = morf(kwargs)
    if description is not None:
        req.post(f'/volunteer/{id}/modify', **kwargs, description=description)

@volunteer.route('vol delete <int:id>')
def delete_volunteer(id):
    '''删除义工'''
    req.post(f'/volunteer/{id}/delete')

@volunteer.route('vol audit <int:id>')
def audit_volunteer(id):
    '''审核义工'''
    req.post(f'/volunteer/{id}/audit')