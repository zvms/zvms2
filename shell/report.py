from shell import App
from req import req

report = App('report', '反馈问题:')

@report.route('report <report>')
def send_report(report):
    req.post('/report', report=report)