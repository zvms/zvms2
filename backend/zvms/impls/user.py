from zvms.models import *
from zvms.util import *
import zvms.tokenlib as tk


def check(token_data):
    '[GET] /user/check'
    return success('获取成功', token_data)


def login(id, pwd, token_data):
    '[POST] /user/login'
    user = User.query.get(id)
    if not user or user.pwd != pwd:
        return error(200, '用户名或密码错误')
    return success('登录成功', token=tk.generate(**user.select('id', 'categ', cls_id='cls')))


def logout(token_data):
    '[POST] /user/logout'
    tk.remove(token_data)
    return success('登出成功')


def search_users(token_data, n=None, a=None):
    '[GET] /user/search'
    if n:
        query = User.query.filter(User.name.like(f'%{n}%'))
    else:
        query = User.query
    if a:
        try:
            def filter_(u): return u.categ & int(a)
        except ValueError:
            return error(400, '非法URL参数')
    else:
        def filter_(_): return True
    return success('获取成功', list(select(filter(filter_, query), 'id', 'name')))


def get_user_info(id, token_data):
    '[GET] /user/<int:id>'
    user = User.query.get_or_error(id)
    return success('获取成功', **user.select('name', 'categ',
                   *(('inside', 'outside', 'large')
                     if user.categ & Categ.STUDENT else ()),
                   cls_id='cls'), clsName=user.cls.name)


def modify_password(old, new, token_data):
    '[POST] /user/mod-pwd'
    if len(new) != 32:
        return error(400, '密码格式错误')
    user = User.query.get(token_data['id'])
    if user.pwd != old:
        return error(400, '旧密码错误')
    user.pwd = new
    return success('修改成功')


def change_class(cls, token_data):
    '[POST] /user/change-class'
    User.query.get(token_data['id']).cls_id = cls
    return success('修改成功')


def create_user(users, token_data):
    '[POST] /user/create'
    for user in users:
        Class.query.get_or_error(user['cls'], '班级不存在')
        if len(user['pwd']) != 32:
            return error(400, '密码格式错误')
        User(
            id=user['id'],
            name=user['name'],
            cls_id=user['cls'],
            categ=user['categ'],
            pwd=user['pwd']
        ).insert()
    return success('创建成功')


def modify_user(id, name, cls, categ, token_data):
    '[POST] /user/<int:id>/modify'
    Class.query.get_or_error(cls, '班级不存在')
    User.query.get_or_error(id, '用户不存在').update(
        name=name,
        cls_id=cls,
        categ=categ,
    )
    return success('修改成功')


def delete_user(id, token_data):
    '[POST] /user/<int:id>/delete'
    User.query.filter_by(id=id).delete()
    UserNotice.query.filter_by(user_id=id).delete()
    StuVol.query.filter_by(stu_id=id).delete()
    query = Volunteer.query.filter_by(holder_id=id)
    for vol in query:
        ClassVol.query.filter_by(vol_id=vol.id).delete()
        StuVol.query.filter_by(vol_id=vol.id).delete()
    query.delete()
    return success('删除成功')
