from enum import IntFlag


class UserCatagories(IntFlag):
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
            UserCatagories.NONE: {
                'id': 1,
                'name': '未登录',
            },
            UserCatagories.STUDENT: {
                'id': 2,
                'name': '学生',
            },
            UserCatagories.TEACHER: {
                'id': 4,
                'name': '教师',
            },
            UserCatagories.ACLASS: {
                'id': 8,
                'name': '班级',
            },
            UserCatagories.MANAGER: {
                'id': 16,
                'name': '管理',
            },
            UserCatagories.AUDITOR: {
                'id': 32,
                'name': '审计部',
            },
            UserCatagories.SYSTEM: {
                'id': 64,
                'name': '系统',
            },
        }
        return _data[id]
