from zvms.models import User
from zvms.util import *
import zvms.tokenlib as tk

#[GET] /check
def check(token_data):
    return success('获取成功', token_data)

#[POST] /users/login
def login(id, pwd, token_data):
    user = User.query.get(id)
    if not user or user.pwd != pwd:
        return error('用户名或密码错误')
    return success('登录成功', token=tk.generate(**user.select('id', 'auth', cls_id='cls')))

#[POST] /users/logout
def logout(token_data):
    tk.remove(token_data)
    return success('登出成功')

#[GET] /users/<int:id>
def get_user_info(id, token_data):
    user = User.query.get_or_error(id)
    return success('获取成功', **user.select('name', 'auth',
                   *(('inside', 'outside', 'large') if user.auth & AUTH.STUDENT else ()),
                   cls_id='cls'), clsName=user.cls.name)

#[PATCH] /users/mod-pwd
def modify_password(old, new, token_data):
    user = User.query.get(token_data['id'])
    if user.pwd != old:
        return error('旧密码错误')
    user.pwd = new
    return success('修改成功')

#[PATCH] /users/change-class
def change_class(cls, token_data):
    User.query.get(token_data['id']).cls_id = cls
    return success('修改成功')