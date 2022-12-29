from shell import App
from req import req

classes = App('classes', '班级管理:')

@classes.route('class')
def list_classes():
    '''获取班级列表'''
    res = req.get('/classes')
    if res:
        for i in res:
            print(i['id'], i['name'])

@classes.route('class <int:id>')
def get_class_info(id):
    '''获取班级详细信息'''
    res = req.get(f'/classes/{id}')
    if res:
        def print_users(users):
            for i in users:
                print(i['id'], i['name'])
        print('教师:')
        print_users(res['teachers'])
        print('学生:')
        print_users(res['students'])

@classes.route('class create <int:id> <name>')
def create_class(id, name):
    '''创建班级'''
    req.post('/classes', id=id, name=name)

@classes.route('class delete <int:id>')
def delete_class(id):
    '''删除班级'''
    req.delete(f'/classes/{id}')

@classes.route('class modify <int:id> <name>')
def modify_class(id, name):
    '''修改班级'''
    req.put(f'/classes/{id}', name=name)