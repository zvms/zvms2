import sys

from .types import *
from .users import *

if sys.platform == 'win32':
    STATIC_FOLDER = 'C:\\zvms-backend'
elif sys.platform == 'linux':
    STATIC_FOLDER = '/tmp/zvms-backend'
