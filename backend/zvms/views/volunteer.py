import datetime

from zvms.models import *
from zvms.res import *
from zvms.util import *
from zvms.apilib import Api

def is_signable(id, status, time, token_data, now = datetime.datetime.now())->bool:
    if status != VolStatus.AUDITED:
        return False
    cv = ClassVol.query.get((id, token_data['cls']))
    return not is_outdated(time, now) and cv is not None and cv.now < cv.max

def is_joiner(joiners: list, me: int):
    return any(x['id']==me for x in joiners)


@Api(rule='/volunteer/list', params='ListVolunteers', response='SearchVolunteersResponse')
def list_volunteers(token_data, **kwargs):
    '''列出义工'''
    see_all = token_data['auth'] & (Categ.AUDITOR | Categ.MANAGER | Categ.SYSTEM) #type: bool
    see_class = token_data['auth'] & Categ.CLASS
    def process_query(query):
        ret = list_or_error(query.select(
            'id',
            'name',
            'joiners',
            'time',
            status='calculated_status',
            holder=rpartial(getattr, 'id'),
            holderName=('holder', rpartial(getattr, 'name'))
        ))
        result = []
        now  = datetime.datetime.now()
        for vol in ret:
            signable = is_signable(vol['id'], vol['status'], vol['time'], token_data, now)
            if see_all or ( see_class and vol['id'] in (ClassVol.query.filter_by(
                cls_id=int(token_data['cls'])).select_value('vol_id')) ):
                result.append({
                    **vol,
                    'time': str(vol['time']),
                    'signable': signable
                })
            else:
                myid = token_data['id']
                if signable or vol['holder']==myid or any(x['id']==myid for x in vol['joiners']):
                    result.append({
                        **vol,
                        'time': str(vol['time']),
                        'signable': signable
                    })
        return success('获取成功', result)
    
    conds = []
    try:
        if 'cls' in kwargs:
            conds = [Volunteer.id.in_(ClassVol.query.filter_by(
                cls_id=int(kwargs['cls'])).select_value('vol_id'))]
    except ValueError:
        return error('传入的数据错误: 非法的URL参数')
    
    return process_query(Volunteer.query.filter(*conds).order_by(Volunteer.id.desc()))


@Api(rule='/volunteer/search', params='SearchVolunteers', response='SearchVolunteersResponse')
def search_volunteers(token_data, **kwargs):
    '''搜索义工'''
    see_all = token_data['auth'] & (Categ.AUDITOR | Categ.MANAGER | Categ.SYSTEM)
    conds = [Volunteer.status != VolStatus.REJECTED]

    def filter_(_):
        return True
    def filter_2(v):
        if see_all:
            return True
        else:
            return is_joiner(v['joiners'], token_data['id']) or is_signable(v['id'], v['status'], v['time'], token_data)
    def filter_signable(v):
        return is_signable(v['id'], v['status'], v['time'], token_data)
    try:
        if 'holder' in kwargs:
            conds.append(Volunteer.holder_id == int(kwargs['holder']))
        if 'student' in kwargs:
            conds.append(Volunteer.id.in_(StuVol.query.filter_by(
                stu_id=int(kwargs['student'])).select_value('vol_id')))
        if 'cls' in kwargs:
            conds.append(Volunteer.id.in_(ClassVol.query.filter_by(
                cls_id=int(kwargs['cls'])).select_value('vol_id')))
        if 'name' in kwargs:
            conds.append(Volunteer.name.like(f'%{kwargs["name"]}%'))
        if 'status' in kwargs:
            conds.append(Volunteer.status == int(kwargs['status']))
        if kwargs.get('signable'):
            filter_ = filter_signable
    except ValueError:
        return error('传入的数据错误: 非法的URL参数')

    def process_query(query):
        ret = list_or_error(query.select(
            'id',
            'name',
            'joiners',
            time=str,
            status='calculated_status',
            holder=rpartial(getattr, 'id'),
            holderName=('holder', rpartial(getattr, 'name'))
        ))
        ret = list(filter(filter_, filter(filter_2, ret)))
        for i in ret:
            i['signable'] = is_signable(i['id'], i['status'], i['time'], token_data)
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
        'description',
        'classes',
        status='calculated_status',
        holder=rpartial(getattr, 'id'),
        holderName=('holder', rpartial(getattr, 'name'))
    )
    ret['signable'] = is_signable(id, ret['status'], ret['time'], token_data)
    ret['time'] = str(ret['time'])
    classes = []
    for cls in ret['classes']:
        classes.append({
            **cls,
            'name': Class.query.get_or_error(cls['id']).name
        })
    ret['classes'] = classes
    return success('获取成功', **ret)


def _create_volunteer(token_data, kwargs):
    kwargs['time'] = try_parse_time(kwargs['time'])
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
    if (Categ.CLASS | Categ.TEACHER | Categ.MANAGER | Categ.SYSTEM).authorized(token_data['auth']):
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
    clses = set()
    for joiner in joiners:
        user = User.query.get(joiner)
        if user is None:
            return error(f'学生{joiner}不存在')
        if user.auth & Categ.TEACHER:
            return error(f'不可报名教师{joiner}')
        clses.add(user.cls_id)
        StuVol(
            stu_id=joiner,
            vol_id=id,
            status=ThoughtStatus.DRAFT,
            thought='',
            reward=-1,
            reason='',
            ever_repulsed=False
        ).insert()
    for cls in clses:
        ClassVol(
            cls_id=cls,
            vol_id=id,
            max=0
        ).insert()
    return success('创建成功')


@Api(rule='/volunteer/<int:id>/modify', method='POST', params='Volunteer')
def modify_volunteer(token_data, id, classes, time, **kwargs):
    '''修改义工'''
    vol = Volunteer.query.get_or_error(id)
    auth_self(vol.holder_id, token_data, '权限不足: 不能修改其他人的义工')
    for cls in classes:
        cls_ = Class.query.get_or_error(cls['id'], '班级不存在')
        if cls['max'] > cls_.members.count():
            return error('义工永远无法报满')
        cv = ClassVol.query.get((id, cls['id']))
        if cv is None:
            ClassVol(
                cls_id=cls['id'],
                vol_id=id,
                max=cls['max']
            ).insert()
        else:
            cv.max = cls['max']
        if cv.now > cls['max']:
            return error('义工报名溢出')
    vol.update(time=try_parse_time(time), **kwargs)
    return success('修改成功')


@Api(rule='/volunteer/<int:id>/delete', method='POST')
def delete_volunteer(token_data, id):
    '''删除义工'''
    auth_self(Volunteer.query.get_or_error(id).holder_id, token_data, '权限不足: 不能删除其他人的义工')
    Volunteer.query.filter_by(id=id).delete()
    ClassVol.query.filter_by(vol_id=id).delete()
    StuVol.query.filter_by(vol_id=id).delete()
    return success('删除成功')


@Api(rule='/volunteer/<int:id>/audit', method='POST', auth=Categ.CLASS | Categ.TEACHER)
def audit_volunteer(token_data, id):
    '''审核通过义工'''
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
            content=f'您的义工 {vol.name} 已过审，属于报名范围内的学生可以在义工列表看到并报名。',
            sendtime=datetime.datetime.now(),
            deadtime=datetime.datetime.now() + datetime.timedelta(days=10),
            sender=0
        ).insert().id
    ).insert()
    return success('审核成功')


@Api(rule='/volunteer/<int:id>/repulse', method='POST', auth=Categ.CLASS | Categ.TEACHER)
def repulse_volunteer(token_data, id):
    '''审核打回义工'''
    vol = Volunteer.query.get_or_error(id)
    if (Categ.TEACHER | Categ.CLASS) & token_data['auth']:
        auth_cls(vol.holder.cls_id, token_data)
    Volunteer.query.get_or_error(id).update(
        status=VolStatus.REJECTED
    )
    UserNotice(
        user_id=vol.holder_id,
        notice_id=Notice(
            title='义工被打回',
            content=f'您的义工 {vol.name} 已被打回, 其他学生无法将看见和报名该义工。',
            sendtime=datetime.datetime.now(),
            deadtime=datetime.datetime.now() + datetime.timedelta(days=10),
            sender=0
        ).insert().id
    ).insert()
    return success('打回成功')

@Api(rule='/volunteer/create/special', method='POST', auth=Categ.MANAGER, params='SpecialVolunteer')
def create_special_volunteer(token_data, name: str, type: VolType, reward: int, joiners: list[int]):
    vol_id = Volunteer(
        name=name,
        description='',
        status=VolStatus.AUDITED,
        holder_id=token_data['id'],
        time=datetime.datetime.now(),
        type=type,
        reward=reward
    ).insert().id
    notice_id = Notice(
        title='义工时间',
        content=f'您由于{name}获得了{reward}义工时间',
        sender=0,
        sendtime=datetime.datetime.now(),
        deadtime=datetime.datetime.now() + datetime.timedelta(days=3)
    )
    for joiner in joiners:
        User.query.get_or_error(joiner, '学生不存在')
        StuVol(
            vol_id=vol_id,
            stu_id=joiner,
            status=ThoughtStatus.ACCEPTED,
            thought=name,
            reason='',
            ever_repulsed=False,
            reward=reward
        ).insert()
        UserNotice(
            user_id=joiner,
            notice_id=notice_id
        ).insert()