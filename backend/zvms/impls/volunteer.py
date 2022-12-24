from zvms.models import *
from zvms.res import *
from zvms.util import *

#[GET] /volunteers
def search_volunteers(token_data, **kwargs):
    conds = []
    try:
        if 'h' in kwargs:
            conds.append(Volunteer.holder_id == int(kwargs['h']))
        if 's' in kwargs:
            conds.append(Volunteer.id.in_(StuVol.query.filter_by(
                stu_id=int(kwargs['s'])).select_value('notice_id')))
        if 'c' in kwargs:
            conds.append(Volunteer.id.in_(ClassVol.query.filter_by(
                cls_id=int(kwargs['c'])).select_value('notice_id')))
        if 'n' in kwargs:
            conds.append(Volunteer.name.like(f'%{kwargs["n"]}%'))
    except ValueError:
        return error('请求接口错误: 非法的URL参数')
    def process_query(query):
        ret = list(query.select('id', 'name', 'time'))
        for i in ret:
            i['time'] = str(i['time'])
        if not ret:
            return error('未查询到相关数据')
        return success('获取成功', ret)
    if not conds:
        return process_query(Volunteer.query)
    return process_query(Volunteer.query.filter(*conds))

#[GET] /volunteers/<int:id>
def get_volunteer_info(id, token_data):
    ret = Volunteer.query.get_or_error(id).select('name', 'description',
                                                  'time', 'type', 'reward', holder_id='holder')
    ret['time'] = str(ret['time'])
    return success('获取成功', **ret)

#[POST] /volunteers
def create_volunteer(token_data, **kwargs):
    try:
        VOL_TYPE(kwargs['type'])
    except ValueError:
        return error('请求接口错误: 未知的义工类型')
    Volunteer(
        **kwargs,
        holder_id=token_data['id'],
    ).insert()
    return success('创建成功')

#[PUT] /volunteers/<int:id>
def update_volunteer(token_data, id, **kwargs):
    try:
        VOL_TYPE(kwargs['type'])
    except ValueError:
        return error('请求接口错误: 未知的义工类型')
    vol = Volunteer.query.get_or_error(id)
    auth_self(vol.holder_id, token_data, '权限不足: 不能修改其他人的义工')
    vol.update(**kwargs)
    return success('修改成功')

#[DELETE] /volunteers/<int:id>
def delete_volunteer(token_data, id):
    auth_self(Volunteer.query.get_or_error(id).holder_id, token_data, '权限不足: 不能删除其他人的义工')
    Volunteer.query.filter_by(id=id).delete()
    return success('删除成功')