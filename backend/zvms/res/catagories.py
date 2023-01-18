from enum import IntFlag


class UserCatagoriesRaw(IntFlag):
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
            UserCatagoriesRaw.NONE: {
                'id': 1,
                'name': '未登录',
            },
            UserCatagoriesRaw.STUDENT: {
                'id': 2,
                'name': '学生',
            },
            UserCatagoriesRaw.TEACHER: {
                'id': 4,
                'name': '教师',
            },
            UserCatagoriesRaw.ACLASS: {
                'id': 8,
                'name': '班级',
            },
            UserCatagoriesRaw.MANAGER: {
                'id': 16,
                'name': '管理',
            },
            UserCatagoriesRaw.AUDITOR: {
                'id': 32,
                'name': '审计部',
            },
            UserCatagoriesRaw.SYSTEM: {
                'id': 64,
                'name': '系统',
            },
        }
        return _data[id]
