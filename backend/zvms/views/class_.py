from zvms.models import *
from zvms.res import *
from zvms.util import *
from zvms.apilib import Api


@Api(rule='/class/list', response='ListClassesResponse')
def list_classes(token_data):
    '''列出所有班级'''
    return success('获取成功', list_or_error(Class.query.select('id', 'name')))


@Api(rule='/class/<int:id>', response='ClassInfoResponse')
def get_class_info(id, token_data):
    '''获取一个班级的详细信息'''
    cls = Class.query.get_or_error(id)
    members = cls.members
    def filter_(auth):
        return list(select(filter(lambda m: (m.auth & auth), members), 'id', 'name'))
    return success('获取成功',
        name=cls.name,
        teachers=filter_(Categ.TEACHER),
        students=filter_(Categ.STUDENT)
    )


@Api(rule='/class/<int:id>/delete', method='POST', auth=Categ.SYSTEM)
def delete_class(id, token_data):
    '''删除一个班级'''
    Class.query.filter_by(id=id).delete()
    return success('删除成功')


@Api(rule='/class/create', method='POST', params='Class', auth=Categ.SYSTEM)
def create_class(id, name, token_data):
    '''创建一个班级'''
    Class(
        id=id,
        name=name
    ).insert()
    return success('创建成功')


@Api(rule='/class/<int:id>/modify', method='POST', params='Class', auth=Categ.SYSTEM)
def modify_class(id, name, token_data):
    '''修改一个班级的名称'''
    Class.query.get_or_error(id, '班级不存在').name = name
    return success('修改成功')
