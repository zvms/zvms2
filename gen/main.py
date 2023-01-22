import time

begin = time.perf_counter()

import os.path
import ast
import sys
import os
import io

import yaml

from util import *
from param import *

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])

with open('config/genconfig.yaml', encoding='utf-8') as f:
    config = yaml.full_load(f)

alias = config.get('alias', {})

def complete(*paths):
    print(os.path.realpath(os.path.join(*paths)), '生成完成!')

def item_assign(value):
    return ast.Assign(
        lineno=1,
        targets=[ast.Name(id=Convertor(value[0], 'camel').export('upper_snake'))],
        value=ast.Constant(value=value[1]['id'])
    )

def genpyres(module, enum, name):
    existing_enum = find(module.body, lambda cd: isinstance(cd, ast.ClassDef) and cd.name == name)
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
            name=name,
            bases=[ast.Name(id='IntEnum')],
            keywords=[],
            body=list(map(item_assign, enum[1].items()))
        )
        module.body.append(existing_enum)
    existing_enum.body.sort(key=lambda item: (isinstance(item, ast.Assign) and item.value.value) or float('inf'))

def gentsres(enum, ts_output, name):
    ts_output.write(f'export enum {name} {{')
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
    ts_output.write(f'''export function get{name}Name(id: number): string {{
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

with open(config['res']['yaml'], encoding='utf-8') as yaml_file, open(config['res']['py'], encoding='utf-8') as py_file:
    enums = yaml.full_load(yaml_file)
    module = ast.parse(py_file.read())

if not module.body or not isinstance(module.body[0], ast.ImportFrom) or (module.body[0].module != 'enum' and not find(module.body[0].names, lambda a: a.name == 'IntEnum')):
    module.body.insert(0, ast.ImportFrom(
        module='enum',
        names=[ast.alias(name='IntEnum')]
    ))
with open(config['res']['ts'], 'w', encoding='utf-8') as ts_output:
    for enum in enums.items():
        pep_name = Convertor(enum[0], 'camel').export('pascal')
        py_config = enum[1].get('_py', {})
        ts_config = enum[1].get('_ts', {})
        if 'ignore' not in py_config:
            genpyres(module, enum, py_config.get('name', pep_name))
        if 'ignore' not in ts_config:
            gentsres(enum, ts_output, ts_config.get('name', pep_name))
    complete(config['res']['ts'])

with open(config['res']['py'], 'w', encoding='utf-8') as output:
    output.write(ast.unparse(module))
    complete(config['res']['py'])

with open(config['structs']['py'], encoding='utf-8') as input_file, open(config['structs']['ts'], 'w', encoding='utf-8') as output_file:
    input = ast.parse(input_file.read())
    output_file.write(f'import * as enums from "./{config["rel-enums"]}";\n')
    for struct in input.body:
        if not isinstance(struct, ast.Assign):
            continue
        if struct.value.func.id not in ('Object', 'Optional', 'Extends'):
            continue
        output_file.write(assign(struct).unwrap_struct(struct.targets[0].id))
    complete(config['structs']['ts'])

parent = ast.Module(
    body=[],
    type_ignores=[]
)
output_ts = io.StringIO()
output_ts.write(f'{config["methods-flag"]["start"]}\n')
Identifier.internal = False
rule_to_url = re.compile(r'(.+?)\<(?:int:)?(.+?)\>')
rule_to_url_sub = r'\1${\2}'

def get_attr(attr):
    return (Convertor(attr.attr, 'upper_snake').export('pascal'), )

def traversal_op(op):
    if isinstance(op, ast.Attribute):
        return get_attr(op)
    return chain(traversal_op(op.left), get_attr(op.right))

for view in os.scandir(config['views']):
    if view.is_dir() or view.name == '__init__.py':
        continue
    with open(view.path, encoding='utf-8') as input_file:
        input = ast.parse(input_file.read())
        for api in input.body:
            if not isinstance(api, ast.FunctionDef):
                continue
            api_info = find(api.decorator_list, lambda deco: isinstance(deco, ast.Call) and isinstance(deco.func, ast.Name) and deco.func.id == 'api')
            if not api_info:
                continue
            args = {
                'rule': ast.Constant(value=config['api-defaults']['rule']),
                'method': ast.Constant(value=config['api-defaults']['method']),
                'params': ast.Name(id=config['api-defaults']['params']),
                'auth': ast.Attribute(
                    value=ast.Name(id='Categ'),
                    attr=config['api-defaults']['auth']
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
                params = Empty()
            else:
                params = checkers.get(args['params'].id) or Empty
            params.with_url(args['rule'].value)
            docstring = ast.get_docstring(api)
            output_ts.write(config['api-formatter'].format(
                f'\n   * ## {docstring}' if docstring else '',
                args['method'].value,
                args['rule'].value,
                ' | '.join(traversal_op(args['auth'])),
                params.unwrap_docstring(),
                alias.get(api.name, Convertor(api.name, 'snake').export('camel')),
                params.unwrap_full_args(),
                config[params.formatter].format(f'"{args["method"].value}"', f'`{rule_to_url.sub(rule_to_url_sub, args["rule"].value)}`', params.unwrap_call())
            ))
        parent.body.append(ast.Import(
            names=[ast.alias(name=f'zvms.views.{view.name[:-3]}')]
        ))
with open(os.path.join(config["views"], '__init__.py'), 'w', encoding='utf-8') as parent_file:
    parent_file.write(ast.unparse(parent))
complete(config["views"], '__init__.py')
output_ts.write(f'\n\n{config["methods-flag"]["end"]}\n')

methods_block = re.compile(rf'{config["methods-flag"]["start"]}.+{config["methods-flag"]["end"]}', re.S)

with open(config['template'], encoding='utf-8') as f:
    origin = f.read()
with open(config['apis'], 'w', encoding='utf-8') as f:
    output_ts.seek(0)
    f.write(methods_block.sub(output_ts.read(), origin))
complete(config['apis'])

print(f'用时{time.perf_counter() - begin}秒')