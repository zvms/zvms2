import sys

if sys.platform == 'win32':
    STATIC_FOLDER = 'C:\zcvms-backend'
elif sys.platform == 'linux':
    STATIC_FOLDER = '/tmp/zvms-backend'
