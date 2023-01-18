from zvms.models import *
from zvms.res import *
from zvms.util import *


def list_classes(token_data):
    '[GET] /class/list'
    return success('获取成功', list_or_error(Class.query.select('id', 'name')))


def get_class_info(id, token_data):
    '[GET] /class/<int:id>'
    cls = Class.query.get_or_error(id)
    members = cls.members

    def filter_(categ):
        return list(select(filter(lambda m: (m.categ & categ), members), 'id', 'name'))
    return success('获取成功',
        teachers=filter_(Categ.TEACHER),
        students=filter_(Categ.STUDENT)
    )


def delete_class(id, token_data):
    '[POST] /class/<int:id>/delete'
    Class.query.filter_by(id=id).delete()
    return success('删除成功')


def create_class(id, name, token_data):
    '[POST] /class/create'
    Class(
        id=id,
        name=name
    ).insert()
    return success('创建成功')


def modify_class(id, name, token_data):
    '[POST] /classes/<int:id>/modify'
    Class.query.get_or_error(id, '班级不存在').name = name
    return success('修改成功')
