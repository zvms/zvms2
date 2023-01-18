'''
zvms命令行终端, 用来调试api
windows有命令回溯功能, linux不知道能不能搞
引用了我自己写的命令行库, 轮子造完之后才发现python自带cmd库, 不过懒得改了
'''


from shell import App
from user import user
from class_ import class_
from report import report
from notice import notice
from volunteer import volunteer
from signup import signup
from thought import thought

app = App('zvms-shell', '镇海中学义工管理系统终端', title='镇海中学义工管理系统终端', prompt='(未登录)> ')

app.register(user)
app.register(class_)
app.register(report)
app.register(notice)
app.register(volunteer)
app.register(signup)
app.register(thought)

app.run_shell()