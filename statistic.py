from collections import defaultdict
from operator import itemgetter
import sys
import os
import os.path

count = defaultdict(int)

def add(path, ext):
    if path.endswith(ext):
        count[ext] += os.path.getsize(path)
        return True

exts = ('.py', '.ts', '.vue', '.js', '.sql', '.sh', '.ps1', '.json', '.yaml', '.html', '.css')

def traversal(path):
    if os.path.isfile(path):
        for ext in exts:
            if add(path, ext):
                break
        return
    if path.endswith('node_modules'):
        return
    for sub in os.scandir(path):
        traversal(sub.path)

traversal(sys.argv[1])

for k, v in sorted(count.items(), key=itemgetter(1)):
    print(k, v / 1024, 'KB')