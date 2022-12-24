from shell import App
from req import req

signup = App('signup', '报名管理: ')

@signup.route('signup <int:cls>')
def list_signup(cls):
    res = req.get(f'/signup?c={cls}')
    if res:
        for i in res:
            print('{stuId} {stuName} {volId} {volName}'.format(**i))

@signup.route('signup <int:stu> <int:vol>')
def signup_for(stu, vol):
    req.post(f'/signup/{stu}', volId=vol)

@signup.route('signup audit <int:stu> <int:vol>')
def audit_signup(stu, vol):
    req.patch(f'/signup/{stu}/{vol}')