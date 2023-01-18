from itertools import chain
import ast
import re

class RouteUnparser(ast._Unparser):
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

route_unparser = RouteUnparser()

class Convertor:
    def __init__(self, ident, style):
        match style:
            case 'snake' | 'upper_snake':
                self.elems = ident.split('_')
            case 'camel':
                self.elems = chain((re.match(r'^[a-z]*', ident).group(), ), re.findall(r'[A-Z][a-z]*', ident))
            case 'pascal':
                self.elems = re.findall(r'[A-Z][a-z]*', ident)
            case 'kebab':
                self.elems = ident.split('-')
            case 'url':
                self.elems = ident.split('/')
            case 'text':
                self.elems = ident.split()
        self.elems = map(str.lower, self.elems)

    def export(self, style):
        match style:
            case 'snake':
                return '_'.join(self.elems)
            case 'upper_snake':
                return '_'.join(map(str.upper, self.elems))
            case 'camel':
                _iter = iter(self.elems)
                return next(_iter) + ''.join(map(str.capitalize, _iter))
            case 'pascal':
                return ''.join(map(str.capitalize, self.elems))
            case 'kebab':
                return '-'.join(self.elems)

def find(seq, predicate):
    for item in seq:
        if predicate(item):
            return item
    return None