from zvms.models import *
from zvms.res import *
from zvms.util import *


def list_signup(cls, token_data):
    '[GET] /signup/list/<int:cls>'
    return success('获取成功', list_or_error((sv.select(stu_id='stuId', vol_id='volId', stu_name='stuName', vol_name='volName') for sv in StuVol.query if sv.stu.cls_id == cls)))


def audit_signup(volId, stuId, token_data):
    '[POST] /signup/<int:volId>/<int:stuId>'
    stu_vol = StuVol.query.get((volId, stuId))
    if not stu_vol:
        return error(403, '学生未报名该义工')
    auth_cls(User.query.get(stuId).cls_id, token_data)
    stu_vol.status = ThoughtStatus.UNSUBMITTED
    return success('审核成功')


def signup(students, volId, token_data):
    '[POST] /signup/<int:volId>'
    vol = Volunteer.query.get_or_error(volId, '该义工不存在')
    if vol.status == VolStatus.UNAUDITED:
        return error(403, '该义工未过审')
    if vol.time < datetime.datetime.now():
        return error(403, '该义工报名已截至')
    for stuId in students:
        if StuVol.query.get((volId, stuId)):
            return error(403, '学生已报名该义工')
        stu = User.query.get_or_error(stuId, '该学生不存在')
        cv = ClassVol.query.get_or_error((volId, stu.cls_id), '该班级不能报名', 403)
        if cv.now >= cv.max:
            return error(403, '名额已满')
        if stu.categ & Categ.TEACHER:
            return error(403, '不能报名教师')
        if (Categ.TEACHER | Categ.CLASS).authorized(token_data['categ']):
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
                status=ThoughtStatus.WAITING_FOR_SIGNUP_AUDIT
            ).insert()
    return success('报名成功')


def rollback(volId, stuId, token_data):
    '[POST] /signup/<int:volId>/<int:stuId>/audit'
    StuVol.query.get_or_error((volId, stuId), '未报名该义工')
    if (Categ.TEACHER | Categ.CLASS).authorized(token_data['categ']):
        auth_cls(User.query.get(stuId).cls_id, token_data, '不能修改其他班级')
    else:
        auth_self(stuId, token_data, '不能撤回其他人的报名')
    StuVol.query.filter_by(stu_id=stuId, vol_id=volId).delete()
    return success('撤回成功')
