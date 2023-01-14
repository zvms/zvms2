from zvms.models import *
from zvms.utils import *
import zvms.tokenlib as tk


def check(token_data):
    '[GET] /users/check'
    return success('获取成功', token_data)


def login(id, pwd, token_data):
    '[POST] /users/login'
    user = User.query.get(id)
    if not user or user.pwd != pwd:
        return error('用户名或密码错误')
    return success('登录成功', token=tk.generate(**user.select('id', 'auth', cls_id='cls')))


def logout(token_data):
    '[POST] /users/logout'
    tk.remove(token_data)
    return success('登出成功')


def search_users(token_data, n=None, a=None):
    '[GET] /users'
    if n:
        query = User.query.filter(User.name.like(f'%{n}%'))
    else:
        query = User.query
    if a:
        try:
            def filter_(u): return u.auth & int(a)
        except ValueError:
            return error('非法URL参数')
    else:
        def filter_(_): return True
    return success('获取成功', list(apply(select)(filter(filter_, query), 'id', 'name')))


def get_user_info(id, token_data):
    '[GET] /users/<int:id>'
    user = User.query.get_or_error(id)
    return success('获取成功', **user.select('name', 'auth',
                   *(('inside', 'outside', 'large')
                     if user.auth & AUTH.STUDENT else ()),
                   cls_id='cls'), clsName=user.cls.name)


def modify_password(old, new, token_data):
    '[PATCH] /users/mod-pwd'
    if len(new) != 32:
        return error('密码不符合规范')
    user = User.query.get(token_data['id'])
    if user.pwd != old:
        return error('旧密码错误')
    user.pwd = new
    return success('修改成功')


def change_class(cls, token_data):
    '[PATCH] /users/change-class'
    User.query.get(token_data['id']).cls_id = cls
    return success('修改成功')


def create_users(users, token_data):
    '[POST] /users/create'
    for user in users:
        Class.query.get_or_error(user['cls'], '班级不存在')
        if len(user['pwd']) != 32:
            return error('密码不符合规范')
        User(
            id=user['id'],
            name=user['name'],
            cls_id=user['cls'],
            auth=user['auth'],
            pwd=user['pwd']
        ).insert()
    return success('创建成功')


def modify_user(id, name, cls, auth, token_data):
    '[PUT] /users/<int:id>'
    Class.query.get_or_error(cls, '班级不存在')
    User.query.get_or_error(id, '用户不存在').update(
        name=name,
        cls_id=cls,
        auth=auth,
    )
    return success('修改成功')


def delete_user(id, token_data):
    '[DELETE] /users/<int:id>'
    User.query.filter_by(id=id).delete()
    UserNotice.query.filter_by(user_id=id).delete()
    StuVol.query.filter_by(stu_id=id).delete()
    query = Volunteer.query.filter_by(holder_id=id)
    for vol in query:
        ClassVol.query.filter_by(vol_id=vol.id).delete()
        StuVol.query.filter_by(vol_id=vol.id).delete()
    query.delete()
    return success('删除成功')
