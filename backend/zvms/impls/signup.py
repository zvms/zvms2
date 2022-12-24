from zvms.models import *
from zvms.res import *
from zvms.util import *


#[GET] /signup
def list_signup(**kwargs):
    if 'c' not in kwargs:
        return error('请求接口错误: 没有指定班级')
    ret = list(StuVol.query.select(stu_id='stuId', vol_id='volId'))
    if not ret:
        return error('未查询到相关数据')
    for i in ret:
        i['stuName'] = User.query.get(i['stuId']).name
        i['volName'] = Volunteer.query.get(i['volId']).name
    return success('获取成功', list(ret))

#[PATCH] /signup/<int:stuId>/<int:volId>
def audit_signup(stuId, volId, token_data):
    stu_vol = StuVol.query.get((stuId, volId))
    if not stu_vol:
        return error('学生未报名该义工')
    auth_cls(User.query.get(stuId).cls_id, token_data)
    stu_vol.status = STATUS.UNSUBMITTED
    return success('审核成功')

#[POST] /signup/<int:stuId>
def signup(stuId, volId, token_data):
    Volunteer.query.get_or_error(volId, '该义工不存在')
    if StuVol.query.get((stuId, volId)):
        return error('学生已报名该义工')
    if User.query.get_or_error(stuId, '该学生不存在').auth & AUTH.TEACHER:
        return error('不能报名教师')
    if (token_data['auth'] & AUTH.TEACHER) or (token_data['auth'] & AUTH.CLASS):
        auth_cls(User.query.get(stuId).cls_id, token_data)
        StuVol(
            stu_id=stuId,
            vol_id=volId,
            status=STATUS.UNSUBMITTED,
        ).insert()
    else:
        auth_self(stuId, token_data, '不能给其他人报名')
        StuVol(
            stu_id=stuId,
            vol_id=volId,
            status=STATUS.WAITING_FOR_FIRST_AUDIT
        ).insert()
    return success('报名成功')