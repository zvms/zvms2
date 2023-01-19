import json
import ast
import sys
import os

from util import *

def item_assign(value):
    return ast.Assign(
        lineno=1,
        targets=[ast.Name(id=Convertor(value[0], 'camel').export('upper_snake'))],
        value=ast.Constant(value=value[1]['id'])
    )

with open('apis/res.json', encoding='utf-8') as json_file, open('backend/zvms/res.py', encoding='utf-8') as py_file:
    enums = json.load(json_file)
    module = ast.parse(py_file.read())

if not module.body or not isinstance(module.body[0], ast.ImportFrom) or (module.body[0].module != 'enum' and not find(module.body[0].names, lambda a: a.name == 'IntEnum')):
    module.body.insert(0, ast.ImportFrom(
        module='enum',
        names=[ast.alias(name='IntEnum')]
    ))
for enum in enums.items():
    pep_name = Convertor(enum[0], 'camel').export('pascal')
    existing_enum = find(module.body, lambda cd: isinstance(cd, ast.ClassDef) and cd.name == pep_name)
    if existing_enum:
        for value in enum[1].items():
            pep_field_name = Convertor(value[0], 'camel').export('upper_snake')
            existing_value = find(existing_enum.body, lambda ass: isinstance(ass, ast.Assign) and 
                find(ass.targets, lambda name: name.id == pep_field_name))
            if existing_value:
                existing_value.value = ast.Constant(value=value[1]['id'])
            else:
                existing_enum.body.append(item_assign(value))
    else:
        existing_enum = ast.ClassDef(
            decorator_list=[],
            name=pep_name,
            bases=[ast.Name(id='IntEnum')],
            keywords=[],
            body=list(map(item_assign, enum[1].items()))
        )
        module.body.append(existing_enum)
    existing_enum.body.sort(key=lambda item: (isinstance(item, ast.Assign) and item.value.value) or float('inf'))

with open('backend/zvms/res.py', 'w', encoding='utf-8') as output:
    output.write(ast.unparse(module))
    print('backend/zvms/res.py', '生成完成!')


parent = ast.Module(
    body=[],
    type_ignores=[]
)
for impl in os.scandir('backend/zvms/impls'):
    if impl.is_dir() or impl.name == '__init__.py':
        continue
    with open(impl.path, encoding='utf-8') as input_file, open(f'backend/zvms/views/{impl.name}', 'w') as output_file:
        input = ast.parse(input_file.read())
        output = ast.Module(
            body=[
                ast.ImportFrom(
                    module=module,
                    names=[ast.alias(name=names)]
                ) for module, names in (('zvms.typing.structs', '*'), (f'zvms.impls.{impl.name[:-3]}', '*'), ('zvms.routelib', 'route'), ('zvms.res', 'Categ'))
            ],
            type_ignores=[]
        )
        for api in input.body:
            if not isinstance(api, ast.FunctionDef):
                continue
            api_info = find(api.decorator_list, lambda deco: isinstance(deco, ast.Call) and isinstance(deco.func, ast.Name) and deco.func.id == 'api')
            if not api_info:
                continue
            args = {
                'rule': ast.Constant(value='/'),
                'method': ast.Constant(value='GET'),
                'params': ast.Name(id='Any'),
                'auth': ast.Attribute(
                    value=ast.Name(id='Categ'),
                    attr='ANY'
                ),
            }
            for k in args:
                find_result = find(api_info.keywords, lambda kw: kw.arg == k)
                if find_result is None:
                    continue
                if k == 'params' and isinstance(find_result.value, ast.Constant):
                    args[k] = ast.Name(id=find_result.value.value)
                else:
                    args[k] = find_result.value
            output.body.append(
                ast.Expr(ast.Call(
                    func=ast.Name(id='route'),
                    args=[],
                    keywords=[
                        ast.keyword(
                            arg='impl',
                            value=ast.Name(id=api.name)
                        ),
                        *(ast.keyword(
                            arg=k,
                            value=v
                        ) for k, v in args.items())
                    ]
                ))
            )
        output_file.write(route_unparser.visit(output))
        print(impl.path.replace('impls', 'views'), '生成完成!')
        parent.body.append(ast.Import(
            names=[ast.alias(name=f'zvms.views.{impl.name[:-3]}')]
        ))
with open('backend/zvms/views/__init__.py', 'w', encoding='utf-8') as parent_file:
    parent_file.write(ast.unparse(parent))
print('backend/zvms/views/__init__.py 生成完成!')