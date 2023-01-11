from zvms.models import *
from zvms.res import *
from backend.zvms.utils import *

#[GET] /classes
def list_classes(token_data):
    return success('获取成功', list(Class.query.select('id', 'name')))

#[GET] /classes/<int:id>
def get_class_info(id, token_data):
    cls = Class.query.get_or_error(id)
    members = cls.members
    def filter_(auth):
        return list(apply(select)(filter(lambda m: (m.auth & auth), members), 'id', 'name'))
    return success('获取成功',
        teachers=filter_(AUTH.TEACHER),
        students=filter_(AUTH.STUDENT)
    )

#[DELETE] /classes/<int:id>
def delete_class(id, token_data):
    Class.query.filter_by(id=id).delete()
    ClassVol.query.filter_by(cls_id=id).delete()
    ClassNotice.query.filter_by(cls_id=id).delete()
    User.query.filter_by(cls_id=id).delete()
    return success('删除成功')

#[POST] /classes
def create_class(id, name, token_data):
    Class(
        id=id,
        name=name
    ).insert()
    return success('创建成功')

#[PUT] /classes/<int:id>
def modify_class(id, name, token_data):
    Class.query.get_or_error(id, '班级不存在').name = name
    return success('修改成功')