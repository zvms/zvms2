from zvms.models import *
from zvms.res import *
from zvms.util import *
from zvms.apilib import api


@api(rule='/class/list')
def list_classes(token_data):
    return success('获取成功', list_or_error(Class.query.select('id', 'name')))


@api(rule='/class/<int:id>')
def get_class_info(id, token_data):
    cls = Class.query.get_or_error(id)
    members = cls.members

    def filter_(auth):
        return list(select(filter(lambda m: (m.auth & auth), members), 'id', 'name'))
    return success('获取成功',
        name=cls.name,
        teachers=filter_(Categ.TEACHER),
        students=filter_(Categ.STUDENT)
    )


@api(rule='/class/<int:id>/delete', method='POST', auth=Categ.SYSTEM)
def delete_class(id, token_data):
    Class.query.filter_by(id=id).delete()
    return success('删除成功')


@api(rule='/class/create', method='POST', params='Class', auth=Categ.SYSTEM)
def create_class(id, name, token_data):
    Class(
        id=id,
        name=name
    ).insert()
    return success('创建成功')


@api(rule='/class/<int:id>/modify', method='POST', params='Class', auth=Categ.SYSTEM)
def modify_class(id, name, token_data):
    Class.query.get_or_error(id, '班级不存在').name = name
    return success('修改成功')
