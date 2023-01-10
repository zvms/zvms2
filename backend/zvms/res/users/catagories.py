from enum import IntFlag


class USER_CATAGORIES(IntFlag):
    NONE = 0b00000001
    STUDENT = 0b00000010
    TEACHER = 0b00000100
    ACLASS = 0b00001000
    MANAGER = 0b00010000
    AUDITOR = 0b00100000
    SYSTEM = 0b01000000

class UserCatagoriesInfo:
    none = {
        'id': 1,
        'name': '未登录',
    }
    student = {
        'id': 2,
        'name': '学生',
    }
    teacher = {
        'id': 4,
        'name': '教师',
    }
    aclass = {
        'id': 8,
        'name': '班级',
    }
    manager = {
        'id': 16,
        'name': '管理',
    }
    auditor = {
        'id': 32,
        'name': '审计部',
    }
    system = {
        'id': 64,
        'name': '系统',
    }
    @staticmethod
    def byId(id):
        _data = {
            USER_CATAGORIES.NONE: {
                'id': 1,
                'name': '未登录',
            },
            USER_CATAGORIES.STUDENT: {
                'id': 2,
                'name': '学生',
            },
            USER_CATAGORIES.TEACHER: {
                'id': 4,
                'name': '教师',
            },
            USER_CATAGORIES.ACLASS: {
                'id': 8,
                'name': '班级',
            },
            USER_CATAGORIES.MANAGER: {
                'id': 16,
                'name': '管理',
            },
            USER_CATAGORIES.AUDITOR: {
                'id': 32,
                'name': '审计部',
            },
            USER_CATAGORIES.SYSTEM: {
                'id': 64,
                'name': '系统',
            },
        }
        return _data[id]
