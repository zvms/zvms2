import datetime
from zvms.models import *
from zvms.res import *
from zvms.util import *
from zvms.apilib import Api


@Api(rule='/signup/list/<int:cls>', response='ListSignupResponse')
def list_signup(cls, token_data):
    '''列出一个班级的报名'''
    return success('获取成功', list_or_error((sv.select(stu_id='stuId', vol_id='volId', stu_name='stuName', vol_name='volName') for sv in StuVol.query if sv.stu.cls_id == cls)))


@Api(rule='/signup/<int:volId>/<int:stuId>/audit', method='POST', auth=Categ.CLASS | Categ.TEACHER)
def audit_signup(volId, stuId, token_data):
    '''审核一个报名'''
    stu_vol = StuVol.query.get((volId, stuId))
    if not stu_vol:
        return error('学生未报名该义工')
    auth_cls(User.query.get(stuId).cls_id, token_data)
    stu_vol.status = ThoughtStatus.UNSUBMITTED
    return success('审核成功')


@Api(rule='/signup/<int:volId>', method='POST', params='Signup')
def signup(students, volId, token_data):
    '''报名一个义工'''
    vol = Volunteer.query.get_or_error(volId, '该义工不存在')
    if vol.status == VolStatus.UNAUDITED:
        return error('该义工未过审')
    if vol.time < datetime.datetime.now():
        return error('该义工报名已截止')
    for stuId in students:
        if StuVol.query.get((volId, stuId)):
            return error('学生已报名该义工')
        stu = User.query.get_or_error(stuId, '该学生不存在')
        cv = ClassVol.query.get_or_error((volId, stu.cls_id), '该班级不能报名')
        if cv.now >= cv.max:
            return error('名额已满')
        if stu.auth & Categ.TEACHER:
            return error('不能报名教师')
        if (Categ.TEACHER | Categ.CLASS).authorized(token_data['auth']):
            auth_cls(User.query.get(stuId).cls_id, token_data, '不能报名其他班级')
            StuVol(
                stu_id=stuId,
                vol_id=volId,
                status=ThoughtStatus.UNSUBMITTED,
            ).insert()
        else:
            auth_self(stuId, token_data, '不能给其他人报名')
            StuVol(
                stu_id=stuId,
                vol_id=volId,
                status=ThoughtStatus.UNSUBMITTED#ThoughtStatus.WAITING_FOR_SIGNUP_AUDIT
            ).insert()
    UserNotice(
        user_id=vol.holder_id,
        notice_id=Notice(
            title='义工报名',
            content=f'学生{token_data["name"]}报名了你的义工{vol.name}',
            deadtime=datetime.datetime.now() + datetime.timedelta(days=1),
            sender=0
        ).insert().id
    )
    return success('报名成功')



@Api(rule='/signup/<int:volId>/<int:stuId>/rollback', method='POST')
def rollback(volId, stuId, token_data):
    '''撤回一个报名'''
    StuVol.query.get_or_error((volId, stuId), '未报名该义工')
    if (Categ.TEACHER | Categ.CLASS).authorized(token_data['auth']):
        auth_cls(User.query.get(stuId).cls_id, token_data, '不能修改其他班级')
    else:
        auth_self(stuId, token_data, '不能撤回其他人的报名')
    StuVol.query.filter_by(stu_id=stuId, vol_id=volId).delete()
    return success('撤回成功')
