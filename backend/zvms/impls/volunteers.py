from zvms.models import *
from zvms.res import *
from zvms.utils import *

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
        'time', 'type', 'reward', 'joiners', holder_id='holder')
    ret['time'] = str(ret['time'])
    return success('获取成功', **ret)

#[POST] /volunteers
def create_volunteer(token_data, classes, **kwargs):
    try:
        VOL_TYPE(kwargs['type'])
    except ValueError:
        return error('请求接口错误: 未知的义工类型')
    id = Volunteer(
        **kwargs,
        holder_id=token_data['id'],
    ).insert().id
    if (AUTH.CLASS | AUTH.TEACHER).authorized(token_data['auth']):
        for cls in classes:
            cls_ = Class.query.get_or_error(cls['id'], '班级不存在')
            if cls['max'] > cls_.members.count():
                return error('义工永远无法报满')
            ClassVol(
                cls_id=cls['id'],
                vol_id=id,
                max=cls['max']
            ).insert()
    else:
        for cls in classes:
            if cls != token_data['cls']:
                return error('不能创建其他班级的义工')
            if cls['max'] > Class.query.get(cls).members.count():
                return error('义工永远无法报满')
            ClassVol(
                cls_id=cls['id'],
                vol_id=id,
                max=cls['max']
            ).insert()
    return success('创建成功')

#[PUT] /volunteers/<int:id>
def update_volunteer(token_data, id, classes, **kwargs):
    try:
        VOL_TYPE(kwargs['type'])
    except ValueError:
        return error('请求接口错误: 未知的义工类型')
    vol = Volunteer.query.get_or_error(id)
    auth_self(vol.holder_id, token_data, '权限不足: 不能修改其他人的义工')
    for cls in classes:
        cls_ = Class.query.get_or_error(cls['id'], '班级不存在')
        if cls['max'] > cls_.members.count():
            return error('义工永远无法报满')
        cv = ClassVol.query.get((cls['id'], id))
        if cv:
            ClassVol(
                cls_id=cls['id'],
                vol_id=id,
                max=cls['max']
            ).insert()
        else:
            cv.max = cls['max']
        if cv.now > cls['max']:
            return error('义工报名溢出')
    vol.update(**kwargs)
    return success('修改成功')

#[DELETE] /volunteers/<int:id>
def delete_volunteer(token_data, id):
    auth_self(Volunteer.query.get_or_error(id).holder_id, token_data, '权限不足: 不能删除其他人的义工')
    Volunteer.query.filter_by(id=id).delete()
    StuVol.query.filter_by(vol_id=id).delete()
    ClassVol.query.filter_by(vol_id=id).delete()
    return success('删除成功')