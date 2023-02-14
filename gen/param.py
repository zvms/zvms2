import ast
import re

def parse(node):
    if isinstance(node, ast.Name):
        match node.id:
            case 'Any':
                return 'any'
            case 'Int' | 'Float' | 'Number' | 'UrlInt':
                return 'number'
            case 'Null':
                return 'null'
            case 'Boolean':
                return 'boolean'
            case _:
                return Identifier(node.id)
    elif isinstance(node, ast.Call):
        match node.func.id:
            case 'Object':
                return Object(node.keywords)
            case 'Array':
                return Array(parse(node.args[0]))
            case 'String':
                return 'string'
            case 'Optional':
                return Optional(node.keywords)
            case 'Extends':
                p = parse(node.args[0])
                if isinstance(p, Identifier):
                    return checkers.get(p.name).copy_extend(node.keywords)
                ret = parse(node.args[0])
                ret.extend(node.keywords)
                return ret
            case 'Literal':
                return f'enums.{node.args[0].value.id}'
            # 懒得写这俩了
            # 反正也没用过, 就先放着吧
            case 'Intersection':
                pass
            case 'Union':
                pass
    else:
        raise Exception(f'Unknown checker type {node}')

def assign(assignment):
    ret = parse(assignment.value)
    checkers[assignment.targets[0].id] = ret
    return ret

checkers = {}

class Identifier:
    internal = True

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return ('' if Identifier.internal else 'structs.') + self.name

class Array:
    def __init__(self, sub):
        self.sub = sub

    def unwrap_struct(self, name):
        return f'export type {name} = {self.sub}[];\n'

    def unwrap_full_args(self):
        return f'{self.sub}[]'

    def __str__(self):
        return f'{self.sub}[]'

class Object:
    url_args = re.compile(r'\<.+?\>')
    formatter = 'object-formatter'

    def __init__(self, keywords):
        self.members = {}
        self.url_args = {}
        self.extend(keywords)

    def with_url(self, url):
        self.url_args = {}
        for arg in Object.url_args.findall(url):
            if arg.startswith('<int:'):
                self.url_args[arg[5:-1]] = 'number'
            else:
                self.url_args[arg[1:-1]] = 'string'

    def copy_extend(self, keywords):
        obj = object.__new__(type(self))
        obj.members = self.members.copy()
        obj.extend(keywords)
        return obj

    def extend(self, keywords):
        for kw in keywords:
            self.members[kw.arg] = parse(kw.value)
            
    def unwrap_struct(self, name):
        return '''export interface {} {{
{}
}}
'''.format(name, '\n'.join(f'  {key}: {value};' for key, value in self.members.items()))

    def unwrap_args(mapping, colon=':'):
        return ',\n    '.join(f'{key}{colon} {value}' for key, value in mapping.items())

    def unwrap_full_args(self):
        return '\n    ' + ',\n    '.join(map(Object.unwrap_args, filter(lambda x: x, (self.url_args, self.members)))) + '\n  '

    def unwrap_docstring(self, mapping=None):
        if mapping is None:
            mapping = self.members | self.url_args
        return '\n   * @param ' + '\n   * @param '.join(mapping.keys())

    def unwrap_call(self, mapping=None):
        if mapping is None:
            mapping = self.members
        return ',\n      '.join(mapping.keys())

class Optional(Object):
    def unwrap_full_args(self):
        return '\n    ' + ',\n    '.join(Object.unwrap_args(m, c) for m, c in ((self.url_args, ':'), (self.members, '?:')) if m) + '\n  '

    def unwrap_call(self):
        return '...[\n          ' + ',\n          '.join(self.members.keys()) + '\n        ].filter((value: any) => value != undefined)'

class Empty(Object):
    formatter = 'empty-formatter'

    def __init__(self):
        self.url_args = {}

    def unwrap_docstring(self):
        if self.url_args:
            return Object.unwrap_docstring(None, self.url_args)
        return ''

    def unwrap_full_args(self):
        return Object.unwrap_args(self.url_args, ':')

    def unwrap_call(self):
        return ''
