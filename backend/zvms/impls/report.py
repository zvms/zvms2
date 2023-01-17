import datetime

from zvms.util import *


def report(report, token_data):
    '[POST] /report'
    with open('report.txt', 'a', encoding='utf-8') as f:
        f.write(f'[{datetime.datetime.now()}] {report}\n')
    return success('反馈成功')
