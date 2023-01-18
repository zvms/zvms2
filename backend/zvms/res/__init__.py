import sys
from . import auth, catagories


class Categ(catagories.UserCatagoriesRaw):  # pylint: disable=invalid-enum-extension

    info = catagories.UserCatagoriesInfo

    def authorized(self, categ):
        return (Categ.SYSTEM | self) & categ


if sys.platform == 'linux':
    STATIC_FOLDER = '/tmp/zvms_backend'
elif sys.platform == 'win32':
    STATIC_FOLDER = 'C:\\zvms_backend'

__all__ = [
    'Categ',
    'auth',
    'STATIC_FOLDER'
]
