import hashlib

from shell import App
from req import req,headers

def md5ify(raw):
    md5 = hashlib.md5()
    md5.update(raw.encode())
    return md5.hexdigest()

users = App('users', '用户管理:')

@users.route('user login <int:id> <pwd>')
def login(id, pwd):
    '''登录'''
    res = req.post('/users/login', id=id, pwd=md5ify(pwd))
    if res:
        headers['Authorization'] = res['token']
        App.config['prompt'] = f'{id}> '
        print(f'''用户名: {res['name']}
班级: {res['clz']}''')

@users.route('user logout')
def logout():
    '''登出'''
    req.post('/users/logout')

@users.route('user <int:id>')
def get_user_info(id):
    '''获取一个用户的详细信息'''
    res = req.get(f'/users/{id}')
    if res:
        print('''姓名: {name}
班级: {clz}
权限: {auth}'''.format(**res))

@users.route('user mod-pwd <old> <new>')
def modify_password(old, new):
    '''修改自己的密码'''
    req.patch('/users/mod-pwd', old=md5ify(old), new=md5ify(new))

@users.route('user change-class <clz>')
def change_class(clz):
    '''修改自己(老师)的班级'''
    req.patch('/users/change-class', clz=clz)