from shell import App
from req import req

signup = App('signup', '报名管理: ')

@signup.route('signup list <int:class>')
def list_signup(**kwargs):
    '''获取报名列表'''
    res = req.get(f'/signup/list/{kwargs["class"]}')
    if res:
        for i in res:
            print('{stuId} {stuName} {volId} {volName}'.format(**i))

@signup.route('signup <int:vol> *stus int:stu')
def signup_for(stus, vol):
    '''提交报名'''
    req.post(f'/signup/{vol}', students=[i['stu'] for i in stus])

@signup.route('signup audit <int:vol> <int:stu>')
def audit_signup(stu, vol):
    '''审核报名'''
    req.post(f'/signup/{vol}/{stu}/audit')

@signup.route('signup rollback <int:vol> <int:stu>')
def rollback_signup(stu, vol):
    '''撤回报名'''
    req.post(f'/signup/{vol}/{stu}/rollback')