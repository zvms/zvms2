from shell import App
from req import req, headers
from util import md5ify, search

Categ = {
    0b1: '无',
    0b10: '学生',
    0b100: '教师',
    0b1000: '支书',
    0b10000: '管理员',
    0b100000: '审计员',
    0b1000000: '系统'
}

def auth2str(categ):
    return ', '.join((v for k, v in Categ.items() if k & categ))

user = App('user', '用户管理:')

@user.route('user login <int:id> <pwd>')
def login(id, pwd):
    '''登录'''
    res = req.post('/user/login', id=id, pwd=md5ify(pwd))
    if res:
        headers['Authorization'] = res['token']
        App.config['prompt'] = f'{id}> '

@user.route('user logout')
def logout():
    '''登出'''
    req.post('/user/logout')
    headers['Authorization'] = ''
    App.config['prompt'] = '(未登录)> '

@user.route('user search -name <name> -cls <int:categ>')
def search_users(**kwargs):
    '''搜索用户'''
    res = req.get(f'/user/search?{search(kwargs)}')
    if res:
        for i in res:
            print(i['id'], i['name'])

@user.route('user <int:id>')
def get_user_info(id):
    '''获取一个用户的详细信息'''
    res = req.get(f'/user/{id}')
    if res:
        print('''姓名: {name}
班级: {cls}({clsName})
权限: {auth_str}'''.format(**res, auth_str=auth2str(res['categ'])))
        if res['categ'] & 0b10:
            print('''校内时间: {inside}
校外时间: {outside}
大型时间: {large}'''.format(**res))

@user.route('user mod-pwd <old> <new>')
def modify_password(old, new):
    '''修改自己的密码'''
    req.post('/user/mod-pwd', old=md5ify(old), new=md5ify(new))

@user.route('user change-class <cls>')
def change_class(cls):
    '''修改自己(老师)的班级'''
    req.post('/user/change-class', cls=cls)

@user.route('user create *users int:id name int:cls int:categ pwd')
def create_users(users):
    '''创建一批用户'''
    for user in users:
        user['pwd'] = md5ify(user['pwd'])
    req.post('/user/create', users=users)

@user.route('user delete <int:id>')
def delete_user(id):
    '''删除一个用户'''
    req.post(f'/user/{id}')

@user.route('user modify <int:id> <name> <int:cls> <int:categ>')
def modify_user(id, name, categ, cls):
    '''修改一个用户'''
    req.post(f'/user/{id}', name=name, cls=cls, categ=categ)