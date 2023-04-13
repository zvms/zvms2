import datetime
from zvms.models import *
from zvms.util import *
from zvms.res import *
from zvms.apilib import Api


@Api(rule='/notice/search', params='SearchNotices', response='SearchNoticesResponse')
def search_notices(token_data, **kwargs):
    '''搜索通知'''
    conds = [Notice.deadtime > datetime.datetime.now()]
    if 'sender' in kwargs:
        conds.append(Notice.sender == int(kwargs['sender']))
    if 'receiver' in kwargs:
        conds.append(Notice.id.in_(UserNotice.query.filter_by(
            user_id=int(kwargs['receiver'])).select_value('notice_id')))
    if 'cls' in kwargs:
        conds.append(Notice.id.in_(ClassNotice.query.filter_by(
            cls_id=int(kwargs['cls'])).select_value('notice_id')))
    if 'school' in kwargs:
        conds.append(Notice.id.in_(SchoolNotice.query.select_value('notice_id')))
    return success('获取成功', list_or_error(Notice.query.filter(*conds).select(
        'id',
        'title',
        'content',
        'sender',
        senderName='sender_name',
        sendtime=str,
        deadtime=str
    )))


def _save_notice(title, content, deadtime, id):
    return Notice(
        title=title,
        content=content,
        sendtime=datetime.datetime.now(),
        deadtime=deadtime,
        sender=id
    ).insert().id


@Api(rule='/notice/send/user', method='POST', params='Notice', auth=Categ.MANAGER | Categ.TEACHER)
def send_user_notice(title, content, deadtime, targets, token_data):
    '''发送用户通知'''
    id = _save_notice(title, content, deadtime, token_data['id'])
    for i in targets:
        if User.query.get_or_error(i, '未找到目标用户').auth == Categ.STUDENT and not (token_data['auth'] & Categ.SYSTEM):
            return error('不能对普通学生发通知')
        UserNotice(user_id=i, notice_id=id).insert()
    return success('发送成功')


@Api(rule='/notice/send/class', method='POST', params='Notice', auth=Categ.MANAGER | Categ.TEACHER)
def send_class_notice(title, content, deadtime, targets, token_data):
    '''发送班级通知'''
    id = _save_notice(title, content, deadtime, token_data['id'])
    for i in targets:
        Class.query.get_or_error(i, '未找到目标班级')
        ClassNotice(cls_id=i, notice_id=id).insert()
    return success('发送成功')


@Api(rule='/notice/send/school', method='POST', params='SchoolNotice', auth=Categ.MANAGER | Categ.TEACHER)
def send_school_notice(title, content, deadtime, anonymous, token_data):
    '''发送学校通知'''
    SchoolNotice(
        notice_id=_save_notice(title, content, deadtime, 0 if anonymous else token_data['id'])
    ).insert()
    return success('发送成功')


@Api(rule='/notice/<int:id>/delete', method='POST', auth=Categ.MANAGER | Categ.TEACHER)
def delete_notice(id, token_data):
    '''删除一个通知'''
    notice = Notice.query.get_or_error(id)
    auth_self(notice.sender, token_data, '权限不足: 不能删除其他人的通知')
    Notice.query.filter_by(id=id).delete()
    return success('删除成功')


@Api(rule='/notice/<int:id>/modify', method='POST', params='NoticeBody', auth=Categ.MANAGER | Categ.TEACHER)
def modify_notice(id, title, content, deadtime, token_data):
    '''修改一个通知'''
    notice = Notice.query.get_or_error(id)
    auth_self(notice.sender, token_data, '权限不足: 不能修改其他人的通知')
    notice.update(
        title=title,
        content=content,
        deadtime=deadtime
    )
    return success('修改成功')
