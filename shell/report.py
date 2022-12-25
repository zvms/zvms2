from shell import App
from req import req

report = App('report', '反馈问题:')

@report.route('report <report>')
def send_report(report):
    '''发送通知'''
    req.post('/report', report=report)