from zvms.models import *
from zvms.util import *
import zvms.tokenlib as tk


@api(rule='/user/check')
def check(token_data):
    return success('获取成功', token_data)


@api(rule='/user/login', method='POST', params='Login')
def login(id, pwd, token_data):
    user = User.query.get(id)
    if not user or user.pwd != pwd:
        return error(200, '用户名或密码错误')
    return success('登录成功', token=tk.generate(**user.select('id', 'auth', cls_id='cls')))


@api(rule='/user/logout', method='POST')
def logout(token_data):
    tk.remove(token_data)
    return success('登出成功')


@api(rule='/user/search')
def search_users(token_data, n=None, c=None):
    if n:
        query = User.query.filter(User.name.like(f'%{n}%'))
    else:
        query = User.query
    if c:
        try:
            def filter_(u): return u.auth & int(c)
        except ValueError:
            return error(400, '非法URL参数')
    else:
        def filter_(_): return True
    return success('获取成功', list_or_error(select(filter(filter_, query), 'id', 'name')))


@api(rule='/user/<int:id>')
def get_user_info(id, token_data):
    user = User.query.get_or_error(id)
    return success('获取成功', **user.select('name', 'auth',
        *(('inside', 'outside', 'large')
            if user.auth & Categ.STUDENT else ()),
        cls_id='cls'), clsName=user.cls.name)


@api(rule='/user/mod-pwd', method='POST', params='ModPwd')
def modify_password(old, new, token_data):
    if len(new) != 32:
        return error(400, '密码格式错误')
    user = User.query.get(token_data['id'])
    if user.pwd != old:
        return error(400, '旧密码错误')
    user.pwd = new
    return success('修改成功')


@api(rule='/user/change-class', method='POST', params='ChangeClass')
def change_class(cls, token_data):
    User.query.get(token_data['id']).cls_id = cls
    return success('修改成功')


@api(rule='/user/create', method='POST', params='Users', auth=Categ.SYSTEM)
def create_user(users, token_data):
    for user in users:
        Class.query.get_or_error(user['cls'], '班级不存在')
        if len(user['pwd']) != 32:
            return error(400, '密码格式错误')
        User(
            id=user['id'],
            name=user['name'],
            cls_id=user['cls'],
            auth=user['auth'],
            pwd=user['pwd']
        ).insert()
    return success('创建成功')


@api(rule='/user/<int:id>/modify', method='POST', params='User', auth=Categ.SYSTEM)
def modify_user(id, name, cls, auth, token_data):
    Class.query.get_or_error(cls, '班级不存在')
    User.query.get_or_error(id, '用户不存在').update(
        name=name,
        cls_id=cls,
        auth=auth,
    )
    return success('修改成功')


@api(rule='/user/<int:id>/delete', method='POST', auth=Categ.SYSTEM)
def delete_user(id, token_data):
    User.query.filter_by(id=id).delete()
    return success('删除成功')
