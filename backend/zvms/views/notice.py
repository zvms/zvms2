from zvms.models import *
from zvms.util import *
from zvms.res import *
from zvms.apilib import api


@api(rule='/notice/search', params='SearchNotices')
def search_notices(token_data, **kwargs):
    conds = []
    try:
        if 'from' in kwargs:
            conds.append(Notice.sender == int(kwargs['from']))
        if 'to' in kwargs:
            conds.append(Notice.id.in_(UserNotice.query.filter_by(
                user_id=int(kwargs['to'])).select_value('notice_id')))
        if 'cls' in kwargs:
            conds.append(Notice.id.in_(ClassNotice.query.filter_by(
                cls_id=int(kwargs['cls'])).select_value('notice_id')))
        if 'school' in kwargs:
            conds.append(Notice.id.in_(
                SchoolNotice.query.select_value('notice_id')))
    except ValueError:
        return error(400, '请求接口错误: 非法的URL参数')

    def process_query(query):
        ret = list_or_error(query.select('id', 'title', 'content', 'sender', 'deadtime', sender_name='senderName'))
        for i in ret:
            i['deadtime'] = str(i['deadtime'])
        return success('获取成功', ret)
    return process_query(Notice.query.filter(*conds))


def _save_notice(title, content, deadtime, token_data):
    try_parse_time(deadtime)
    return Notice(
        title=title,
        content=content,
        deadtime=deadtime,
        sender=token_data['id']
    ).insert().id


@api(rule='/notice/send/user', method='POST', params='Notice', auth=Categ.MANAGER | Categ.TEACHER)
def send_user_notice(title, content, deadtime, targets, token_data):
    id = _save_notice(title, content, deadtime, token_data)
    for i in targets:
        if User.query.get_or_error(i, '未找到目标用户').auth == Categ.STUDENT and not (token_data['auth'] & Categ.SYSTEM):
            return error(403, '不能对普通学生发通知')
        UserNotice(user_id=i, notice_id=id).insert()
    return success('发送成功')


@api(rule='/notice/send/class', method='POST', params='Notice', auth=Categ.MANAGER | Categ.TEACHER)
def send_class_notice(title, content, deadtime, targets, token_data):
    id = _save_notice(title, content, deadtime, token_data)
    for i in targets:
        Class.query.get_or_error(i, '未找到目标班级')
        ClassNotice(cls_id=i, notice_id=id).insert()
    return success('发送成功')


@api(rule='/notice/send/school', method='POST', params='NoticeBody', auth=Categ.MANAGER | Categ.TEACHER)
def send_school_notice(title, content, deadtime, token_data):
    '[POST] /notice/send/school'
    SchoolNotice(
        notice_id=_save_notice(title, content, deadtime, token_data)
    ).insert()
    return success('发送成功')


@api(rule='/notice/<int:id>/delete', method='POST', auth=Categ.MANAGER | Categ.TEACHER)
def delete_notice(id, token_data):
    notice = Notice.query.get_or_error(id)
    auth_self(notice.sender, token_data, '权限不足: 不能删除其他人的通知')
    Notice.query.filter_by(id=id).delete()
    return success('删除成功')


@api(rule='/notice/<int:id>/modify', method='POST', params='NoticeBody', auth=Categ.MANAGER | Categ.TEACHER)
def modify_notice(id, title, content, deadtime, token_data):
    notice = Notice.query.get_or_error(id)
    auth_self(notice.sender, token_data, '权限不足: 不能修改其他人的通知')
    try_parse_time(deadtime)
    notice.update(
        title=title,
        content=content,
        deadtime=deadtime
    )
    return success('修改成功')
