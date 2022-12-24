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
        print('''用户名: {name}
班级: {clsName}({cls})
权限: {auth}'''.format(**res))

@users.route('user logout')
def logout():
    '''登出'''
    req.post('/users/logout')
    headers['Authorization'] = ''
    App.config['prompt'] = '(未登录)> '

@users.route('user <int:id>')
def get_user_info(id):
    '''获取一个用户的详细信息'''
    res = req.get(f'/users/{id}')
    if res:
        print('''姓名: {name}
班级: {cls}
权限: {auth}'''.format(**res))
        if res['auth'] & 0b10:
            print('''校内时间: {inside}
校外时间: {outside}
大型时间: {large}'''.format(**res))

@users.route('user mod-pwd <old> <new>')
def modify_password(old, new):
    '''修改自己的密码'''
    req.patch('/users/mod-pwd', old=md5ify(old), new=md5ify(new))

@users.route('user change-class <cls>')
def change_class(cls):
    '''修改自己(老师)的班级'''
    req.patch('/users/change-class', cls=cls)