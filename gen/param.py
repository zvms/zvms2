import ast
import re

from util import Convertor

def parse(node):
    if isinstance(node, ast.Name):
        match node.id:
            case 'Any':
                return 'any'
            case 'Int' | 'Float' | 'Number':
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

    def __str__(self):
        return f'Array<{self.sub}>'

class Object:
    url_args = re.compile('(\<\>)')
    formatter = 'object-formatter'

    def __init__(self, keywords):
        self.members = {}
        self.extend(keywords)

    def with_url(self, url):
        self.url_args = {}
        for arg in Object.url_args.findall(url):
            if arg.startswith('<int:'):
                self.url_args[arg[5:-1]] = 'number'
            else:
                self.url_args[arg[1:-1]] = 'string'
        return self

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
        return ',\n    '.join(map(Object.unwrap_args, filter(lambda x: x, (self.url_args, self.members)))) + '\n  '

    def unwrap_docstring(self):
        return '\n   * @param ' + '\n   * @param '.join(self.members.keys())

    def unwrap_call(self):
        return ',\n        '.join(self.members.keys())

class Optional(Object):
    def unwrap_full_args(self):
        return ',\n    '.join(Object.unwrap_args(m, c) for m, c in ((self.url_args, ':'), (self.members, '?:')) if m) + '\n  '

    def unwrap_call(self):
        return '...Array<any>(' + ',\n        '.join(self.members.keys()) + ').filter((value: any) => value != undefined)'

class Empty:
    formatter = 'empty-formatter'

    def unwrap_full_args():
        return ''
    
    def unwrap_docstring():
        return ''

    def unwrap_call():
        return ''
