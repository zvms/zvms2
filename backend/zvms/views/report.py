import datetime

from zvms.apilib import Api
from zvms.models import Report, User
from zvms.util import *
from zvms.res import *


@Api(rule='/report', method='POST', params='Report')
def report(report, token_data):
    '''发送反馈'''
    Report(
        time=datetime.datetime.now(),
        reporter=token_data['id'],
        content=report
    ).insert()
    return success('反馈成功')

@Api(rule='/report/fetch', method='GET', response='FetchReportsResponse', auth=Categ.SYSTEM | Categ.MANAGER)
def fetch_report(token_data):
    '''获取反馈'''
    return success('获取成功', list_or_error(Report.query.select(
        'reporter',
        'content',
        time=str,
        reporterName=('reporter', lambda id: User.query.get(id).name)
    )))