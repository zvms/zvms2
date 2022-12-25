from shell import App
from req import req
from util import *

thoughts = App('thoughts', '感想管理')

@thoughts.route('thought -c <int:id> -S <int:status> -s <int:id> -v <int:id>')
def search_thoughts(**kwargs):
    res = req.get(f'/thoughts?{search(kwargs)}')
    thought_status = ('', '', '未提交', '等待初审', '等待终审', '通过', '拒绝')
    if res:
        for i in res:
            print('''学生: {stuName}({stuId})
义工: {volName}({volId})
状态: {thought_status}
'''.format(**i, thought_status=thought_status[i['status']]))