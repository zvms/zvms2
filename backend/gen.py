import ast
import os
import re

for impl in os.scandir('zvms/impls'):
    if impl.is_dir() or impl.name == '__init__.py':
        continue
    with open(impl.path, encoding='utf-8') as f:
        tree = ast.parse(f.read())
        