import sys

__all__ = [
    "types",
    "users"
]

if sys.platform == 'win32':
    STATIC_FOLDER = 'C:\\zvms-backend'
elif sys.platform == 'linux':
    STATIC_FOLDER = '/tmp/zvms-backend'
