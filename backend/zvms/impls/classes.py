from zvms.models import *
from zvms.res import *
from zvms.util import *


def list_classes(token_data):
    '[GET] /classes'
    return success('获取成功', list(Class.query.select('id', 'name')))


def get_class_info(id, token_data):
    '[GET] /classes/<int:id>'
    cls = Class.query.get_or_error(id)
    members = cls.members

    def filter_(auth):
        return list(select(filter(lambda m: (m.auth & auth), members), 'id', 'name'))
    return success('获取成功',
        teachers=filter_(Categ.TEACHER),
        students=filter_(Categ.STUDENT)
    )


def delete_class(id, token_data):
    '[DELETE] /classes/<int:id>'
    Class.query.filter_by(id=id).delete()
    ClassVol.query.filter_by(cls_id=id).delete()
    ClassNotice.query.filter_by(cls_id=id).delete()
    User.query.filter_by(cls_id=id).delete()
    return success('删除成功')


def create_class(id, name, token_data):
    '[POST] /classes'
    Class(
        id=id,
        name=name
    ).insert()
    return success('创建成功')


def modify_class(id, name, token_data):
    '[PUT] /classes/<int:id>'
    Class.query.get_or_error(id, '班级不存在').name = name
    return success('修改成功')
