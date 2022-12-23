from zvms.models import User
from zvms.util import *
import zvms.tokenlib as tk

#[POST] /users/login
def login(id, pwd, token_data):
    user = User.query.get(id)
    if not user or user.pwd != pwd:
        return error('用户名或密码错误')
    return success('登录成功', name=user.name, clz=user.clz_id, clzName=user.clz.name, 
    token=tk.generate(**user.select('id', 'auth', clz_id='clz')), auth=user.auth)

#[POST] /users/logout
def logout(token_data):
    tk.remove(token_data)
    return success('登出成功')

#[GET] /users/<int:id>
def get_user_info(id, token_data):
    user = User.query.get_or_error(id)
    return success('获取成功', **user.select('name', 'auth', clz_id='clz'), clzName=user.clz.name)

#[PATCH] /users/mod-pwd
def modify_password(old, new, token_data):
    user = User.query.get(token_data['id'])
    if user.pwd != old:
        return error('旧密码错误')
    user.pwd = new
    return success('修改成功')

#[PATCH] /users/change-class
def change_class(clz, token_data):
    User.query.get(token_data['id']).clz_id = clz
    return success('修改成功')