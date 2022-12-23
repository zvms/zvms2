'''
zvms命令行终端, 用来调试api
windows有命令回溯功能, linux不知道能不能搞
引用了我自己写的命令行库, 轮子造完之后才发现python自带cmd库, 不过懒得改了
'''


from shell import App
from users import users
from classes import classes
from report import report
from notices import notices

app = App('zvms-shell', '镇海中学义工管理系统终端', title='镇海中学义工管理系统终端', prompt='(未登录)> ')

app.register(users)
app.register(classes)
app.register(report)
app.register(notices)

if __name__ == '__main__':
    app.run_shell()