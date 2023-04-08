import datetime
import dateparser

from zvms.models import *
from zvms.res import *
from zvms.util import *
from zvms.apilib import Api

def is_outdated(time):
    return time < datetime.datetime.now()

def is_signable(id, time, token_data)->bool:
    cv = ClassVol.query.get((id, token_data['cls']))
    # if not isinstance(time,datetime.datetime):
    #     time = dateparser.parse(time)
    return not is_outdated(time) and (cv is not None) and (cv.now < cv.max)

def is_joiner(joiners:list, me:int):
    return any(x['id']==me for x in joiners)

@Api(rule='/volunteer/search', params='SearchVolunteers', response='SearchVolunteersResponse')
def search_volunteers(token_data, **kwargs):
    '''搜索义工'''

    see_all = token_data['auth']&(Categ.AUDITOR|Categ.MANAGER|Categ.SYSTEM)

    conds = []

    def filter_(v):
        return True
    def filter_2(v):
        if see_all:
            return True
        else:
            return is_joiner(v['joiners'], token_data['id']) or is_signable(v['id'], v['time'], token_data)
    def filter_signable(v):
        return is_signable(v['id'], v['time'], token_data)
    try:
        if 'holder' in kwargs:
            conds.append(Volunteer.holder_id == int(kwargs['holder']))
        if 'student' in kwargs:
            conds.append(Volunteer.id.in_(StuVol.query.filter_by(
                stu_id=int(kwargs['student'])).select_value('notice_id')))
        if 'cls' in kwargs:
            conds.append(Volunteer.id.in_(ClassVol.query.filter_by(
                cls_id=int(kwargs['cls'])).select_value('notice_id')))
        if 'name' in kwargs:
            conds.append(Volunteer.name.like(f'%{kwargs["name"]}%'))
        if 'status' in kwargs:
            conds.append(Volunteer.status == int(kwargs['status']))
        if 'signable' in kwargs and kwargs['signable']:
            filter_ = filter_signable
    except ValueError:
        return error('请求接口错误: 非法的URL参数')

    def process_query(query):
        ret = list_or_error(query.select('id', 'name', 'status', 'time', 'joiners', holder=rpartial(getattr, 'id'), holderName=('holder', rpartial(getattr, 'name'))))
        ret = list(filter(filter_, filter(filter_2, ret)))
        for i in ret:
            i['signable'] = is_signable(i['id'], i['time'], token_data)
            if is_outdated(i['time']):
                i['status'] = VolStatus.FINISHED if i['status'] == VolStatus.AUDITED else VolStatus.DEPRECATED
            i['time'] = str(i['time'])
        return success('获取成功', ret)
    return process_query(Volunteer.query.filter(*conds).order_by(Volunteer.id.desc()))


@Api(rule='/volunteer/<int:id>', response='VolunteerInfoResponse')
def get_volunteer_info(id, token_data):
    '''获取一个义工的详细信息'''
    ret = Volunteer.query.get_or_error(id).select(
        'name',
        'type',
        'reward',
        'joiners',
        'time',
        'status',
        description=render_markdown,
        holder=rpartial(getattr, 'id'),
        holderName=('holder', rpartial(getattr, 'name'))
    )
    ret['signable'] = is_signable(id, ret['time'], token_data)
    if is_outdated(ret['time']):
        ret['status'] = VolStatus.FINISHED if ret['status'] == VolStatus.AUDITED else VolStatus.DEPRECATED
    ret['time'] = str(ret['time'])
    print(ret['joiners'])
    return success('获取成功', **ret)


def _create_volunteer(token_data, kwargs):
    try_parse_time(kwargs['time'])
    if token_data['auth'] == Categ.STUDENT and kwargs['type'] != VolType.OUTSIDE:
        raise ZvmsError('权限不足: 只能创建校外义工')
    return Volunteer(
        **kwargs,
        holder_id=token_data['id'],
        status=int(VolStatus.UNAUDITED if token_data['auth'] == Categ.STUDENT else VolStatus.AUDITED)
    ).insert().id


@Api(rule='/volunteer/create', method='POST', params='Volunteer')
def create_volunteer(token_data, classes, **kwargs):
    '''创建一个义工'''
    id = _create_volunteer(token_data, kwargs)
    if (Categ.CLASS | Categ.TEACHER).authorized(token_data['auth']):
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
            if cls['id'] != token_data['cls']:
                return error('不能创建其他班级的义工')
            if cls['max'] > Class.query.get(cls['id']).members.count():
                return error('义工永远无法报满')
            ClassVol(
                cls_id=cls['id'],
                vol_id=id,
                max=cls['max']
            ).insert()
    return success('创建成功')


@Api(rule='/volunteer/create/appointed', method='POST', params='AppointedVolunteer')
def create_appointed_volunteer(token_data, joiners, **kwargs):
    '''创建一个成员全部指定的义工'''
    id = _create_volunteer(token_data, kwargs)
    for joiner in joiners:
        user = User.query.get(joiner)
        if user is None:
            return error(f'学生{joiner}不存在')
        if user.auth & Categ.TEACHER:
            return error(f'不可报名教师{joiner}')
        StuVol(
            stu_id=joiner['id'],
            vol_id=id
        ).insert()
    return success('创建成功')


@Api(rule='/volunteer/<int:id>/modify', method='POST', params='Volunteer')
def modify_volunteer(token_data, id, classes, **kwargs):
    '''修改义工'''
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


@Api(rule='/volunteer/<int:id>/delete', method='POST')
def delete_volunteer(token_data, id):
    '''删除义工'''
    auth_self(Volunteer.query.get_or_error(id).holder_id, token_data, '权限不足: 不能删除其他人的义工')
    Volunteer.query.filter_by(id=id).delete()
    return success('删除成功')


@Api(rule='/volunteer/<int:id>/audit', method='POST', auth=Categ.CLASS | Categ.TEACHER)
def audit_volunteer(token_data, id):
    '''审核义工(班内)'''
    vol = Volunteer.query.get_or_error(id)
    if (Categ.TEACHER | Categ.CLASS) & token_data['auth']:
        auth_cls(vol.holder.cls_id, token_data)
    Volunteer.query.get_or_error(id).update(
        status=VolStatus.AUDITED
    )
    UserNotice(
        user_id=vol.holder_id,
        notice_id=Notice(
            title='义工过审',
            content=f'您的义工{vol.name}已过审',
            time=datetime.datetime.now() + datetime.timedelta(days=1),
            sender=0
        ).insert().id
    ).insert()
    return success('审核成功')