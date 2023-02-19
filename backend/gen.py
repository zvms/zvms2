from time import perf_counter

begin = perf_counter()

from enum import IntEnum, IntFlag, EnumType
from itertools import chain
import re

import yaml

import zvms.res as res
import zvms.typing.structs as structs
import templates as tpl
from zvms.typing.checker import *
from zvms.apilib import Api

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

def convert(ident, src, dst):
    return Convertor(ident, src).export(dst)

def find(seq, predicate):
    for item in seq:
        if predicate(item):
            return item
    return None

with open('genconfig.yaml', encoding='utf-8') as config_file:
    config = yaml.full_load(config_file.read())
    
with open(config['enums'], 'w', encoding='utf-8') as enums_output, open(config['enums-mapping'], encoding='utf-8') as mapping_file:
    mapping = yaml.full_load(mapping_file.read())
    for enum in (i for i in res.__dict__.values() if isinstance(i, EnumType) and i not in (IntEnum, IntFlag)):
        map_this = mapping[enum.__name__]
        valid_cons = lambda: ((convert(field, 'upper_snake', 'pascal'), value) for field, value in enum.__dict__.items() if type(value) == enum)
        enums_output.write(tpl.ENUMS.format(
            name=enum.__name__,
            body=',\n'.join((tpl.ENUM_CONSTRUCTOR.format(
                field=field,
                value=value
            ) for field, value in valid_cons())),
            switch_body=''.join((tpl.SWITCH_CASE.format(
                enum=enum.__name__,
                field=field,
                name=map_this[field]
            ) for field, value in valid_cons()))
        ))

print(f'用时{perf_counter() - begin}秒')