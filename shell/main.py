from shell import App
from users import users
from classes import classes

app = App('zvms-shell', '镇海中学义工管理系统终端', title='镇海中学义工管理系统终端', prompt='(未登录)> ')

app.register(users)
app.register(classes)

if __name__ == '__main__':
    app.run_shell()