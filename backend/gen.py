import ast
import os
import re

class MyUnparser(ast._Unparser):
    def visit_Call(self, node):
        self.write('\n')
        self.set_precedence(ast._Precedence.ATOM, node.func)
        self.traverse(node.func)
        with self.delimit("(", ")"):
            comma = False
            for e in node.keywords:
                if comma:
                    self.write(",")
                else:
                    comma = True
                self.write('\n    ')
                self.traverse(e)
            self.write('\n')

unparser = MyUnparser()

def find(seq, predicate):
    for item in seq:
        if predicate(item):
            return item
    return None

for impl in os.scandir('zvms/impls'):
    if impl.is_dir() or impl.name == '__init__.py':
        continue
    with open(impl.path, encoding='utf-8') as input_file, open(f'zvms/views/{impl.name}', 'w') as output_file:
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
        output_file.write(unparser.visit(output))
        print(impl.path, '生成完成!')