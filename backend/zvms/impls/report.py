from datetime import datetime

from zvms.util import *

#[POST] /report
def report(report, token_data):
    with open('report.txt', 'a', encoding='utf-8') as f:
        f.write(f'[{datetime.now()}] {report}\n')
    return success('反馈成功')