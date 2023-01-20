import time

begin = time.perf_counter()

import ast
import os
import io

import yaml

from util import *
from param import *

def item_assign(value):
    return ast.Assign(
        lineno=1,
        targets=[ast.Name(id=Convertor(value[0], 'camel').export('upper_snake'))],
        value=ast.Constant(value=value[1]['id'])
    )

def genpyres(module, enum, pep_name):
    existing_enum = find(module.body, lambda cd: isinstance(cd, ast.ClassDef) and cd.name == pep_name)
    if existing_enum:
        for value in enum[1].items():
            if value[0].startswith('_'):
                continue
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

def gentsres(enum, ts_output):
    ts_output.write(f'export enum {pep_name} {{')
    comma = False
    items = sorted(enum[1].items(), key=lambda x: x[1]['id'])
    for field, value in items:
        if field.startswith('_'):
            continue
        if comma:
            ts_output.write(',\n')
        else:
            ts_output.write('\n')
            comma = True
        ts_output.write(f'    {Convertor(field, "camel").export("pascal")} = {value["id"]}')
    ts_output.write('\n}\n')
    ts_output.write(f'''export function get{pep_name}Name(id: number) {{
    switch (id) {{
''')
    for field, value in items:
        if field.startswith('_'):
            continue
        ts_output.write(f'''        case {value["id"]}:
            return "{value["name"]}";
''')
    ts_output.write('''        default:
            throw Error("Invalid enum value");
    }
}
''')

with open('apis/res.yaml', encoding='utf-8') as yaml_file, open('backend/zvms/res.py', encoding='utf-8') as py_file:
    enums = yaml.full_load(yaml_file)
    module = ast.parse(py_file.read())

if not module.body or not isinstance(module.body[0], ast.ImportFrom) or (module.body[0].module != 'enum' and not find(module.body[0].names, lambda a: a.name == 'IntEnum')):
    module.body.insert(0, ast.ImportFrom(
        module='enum',
        names=[ast.alias(name='IntEnum')]
    ))
with open('web/src/apis/types/enums.ts', 'w', encoding='utf-8') as ts_output:
    for enum in enums.items():
        pep_name = Convertor(enum[0], 'camel').export('pascal')
        comma = False
        py_config = enum[1].get('_py')
        ts_config = enum[1].get('_ts')
        if not py_config or 'ignore' not in py_config:
            genpyres(module, enum, pep_name)
        if not ts_config or 'ignore' not in ts_config:
            gentsres(enum, ts_output)
    print('web/src/apis/types/enums.ts 生成完成!')

with open('backend/zvms/res.py', 'w', encoding='utf-8') as output:
    output.write(ast.unparse(module))
    print('backend/zvms/res.py', '生成完成!')

with open('backend/zvms/typing/structs.py', encoding='utf-8') as input_file, open('web/src/apis/types/structs.ts', 'w', encoding='utf-8') as output_file:
    input = ast.parse(input_file.read())
    output_file.write('import * as enums from "./enums.js";\n')
    for struct in input.body:
        if not isinstance(struct, ast.Assign):
            continue
        if struct.value.func.id not in ('Object', 'Optional', 'Extends'):
            continue
        output_file.write(assign(struct).unwrap_struct(struct.targets[0].id))
    print('web/src/apis/types/structs.ts 生成完成!')

parent = ast.Module(
    body=[],
    type_ignores=[]
)
output_ts = io.StringIO()
output_ts.write('  //--METHODS START----\n\n')
Identifier.internal = False

def get_attr(attr):
    return (Convertor(attr.attr, 'upper_snake').export('pascal'), )

def traversal_op(op):
    if isinstance(op, ast.Attribute):
        return get_attr(op)
    return chain(traversal_op(op.left), get_attr(op.right))

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
            if args['params'].id == 'Any':
                params = Empty
            else:
                params = checkers.get(args['params'].id).with_url(args['rule'].value) or Empty
            docstring = ast.get_docstring(api)
            output_ts.write(f'''/**{f"""
   * ## {docstring}""" if docstring else ''}
   * ### [{args['method'].value}] {args['rule'].value}
   * #### Authorization: {' | '.join(traversal_op(args['auth']))}{params.unwrap_docstring()}
   */
  {Convertor(api.name, 'snake').export('camel')}({params.unwrap_full_args()}): ForegroundApiRunner<[]> {{
    return createForegroundApiRunner({params.formatter.format('this', f'"{args["method"].value}"', f'"{args["rule"].value}"', params.unwrap_call())});
  }}
''')
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
output_ts.write('  //--METHODS END----')

methods_block = re.compile(r'  //--METHODS START----.+  //--METHODS END----', re.S)

with open('web/src/apis/fApi-template.ts', encoding='utf-8') as f:
    origin = f.read()
with open('web/src/apis/fApi.ts', 'w', encoding='utf-8') as f:
    output_ts.seek(0)
    f.write(methods_block.sub(output_ts.read(), origin))
print('web/src/apis/fApi.ts 生成完成!')

print(f'用时{time.perf_counter() - begin}秒')