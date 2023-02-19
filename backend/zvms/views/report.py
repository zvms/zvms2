import datetime

from zvms.apilib import Api
from zvms.util import *


@Api(rule='/report', method='POST', params='Report')
def report(report, token_data):
    '''发送反馈'''
    with open('report.txt', 'a', encoding='utf-8') as f:
        f.write(f'[{datetime.datetime.now()}] {report}\n')
    return success('反馈成功')
