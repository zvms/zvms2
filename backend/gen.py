from time import perf_counter

begin = perf_counter()

from enum import IntEnum, IntFlag, EnumType
from itertools import chain
from operator import itemgetter
import re
import os

import yaml

import templates as tpl
import zvms.res as res
import zvms.typing.structs as structs
import zvms.typing.checker as checker
import zvms.views
from zvms.typing.checker import *
from zvms.apilib import Api

def complete(*paths):
    print(os.path.realpath(os.path.join(*paths)), '生成完成!')

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

foo = sorted(((k, v) for k, v in res.Categ.__dict__.items() if type(v) == res.Categ), key=itemgetter(1), reverse=True)

def auth_to_str(auth):
    if not auth:
        return ()
    for k, v in foo:
        if auth & v and v <= auth:
            return chain((convert(k, 'upper_snake', 'pascal'), ), auth_to_str(auth & ~v))

with open('genconfig.yaml', encoding='utf-8') as config_file:
    config = yaml.full_load(config_file.read())
    
with open(config['enums'], 'w', encoding='utf-8') as enums_output,\
    open(config['enums-mapping'], encoding='utf-8') as mapping_file:
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
    complete(config['enums'])

with open(config['structs'], 'w', encoding='utf-8') as structs_output:
    structs_output.write(tpl.STRUCTS_HEADER + '\n\n')
    for name, struct in structs.__dict__.items():
        if isinstance(struct, type) and issubclass(struct, Object) and struct not in (Object, Optional):
            if structs.__doc__ is not None:
                structs_output.write(f'/* {struct.__doc__} */\n')
            structs_output.write(tpl.INTERFACE.format(
                name=struct.__name__,
                inheritance='' if struct.__base__ in (Object, Optional) else tpl.INHERITANCE.format(
                    base=struct.__base__.__name__
                ),
                body=',\n'.join((tpl.INTERFACE_MEMBER.format(
                    field=field,
                    value=value.render()
                ) for field, value in struct.__dict__.items() if isinstance(value, Checker)))
            ))
        elif isinstance(struct, Checker) and not hasattr(checker, name):
            structs_output.write(tpl.TYPE.format(
                name=name,
                alias=struct.render()
            ))
    complete(config['structs'])

rule_methods_block = re.compile(rf'{config["methods-flag"]["start"]}.+{config["methods-flag"]["end"]}', re.S)
rule_to_url = re.compile(r'(.+?)\<(?:int:)?(.+?)\>')
rule_to_url_sub = r'\1${\2}'
Object.module = 'structs.'

def gen_url(api):
    return rule_to_url.sub(rule_to_url_sub, api.rule)

with open(config['apis'], 'w', encoding='utf-8') as apis_output,\
    open(config['apis-template'], encoding='utf-8') as template_input:
    template = template_input.read()
    has_params = lambda api: api.url_params or not isinstance(api.params, Any)
    apis_output.write(rule_methods_block.sub(f'{config["methods-flag"]["start"]}\n' + ''.join((tpl.API.format(
        docstring='' if api.func.__doc__ is None else tpl.DOCSTRING.format(
            docstring=api.func.__doc__
        ),
        method=api.method,
        rule=api.rule,
        auth=' | '.join(auth_to_str(api.auth)),
        params_anno='' if not has_params(api) else '\n' + '\n'.join((tpl.PARAM_ANNO.format(
            name=name
        ) for name in chain(api.url_params, api.params.as_params()))),
        name=convert(api.func.__name__, 'snake', 'camel'),
        params='' if not has_params(api) else '\n' + ',\n'.join((tpl.PARAM.format(
            name=name,
            type=type
        ) for name, type in chain(api.url_params.items(), api.params.as_params().items()))) + '\n  ',
        response=api.response.render(),
        create_args=tpl.CREATE_NO_PARAMS.format(
            method=api.method,
            url=gen_url(api)
        ) if not has_params(api) else tpl.CREATE.format(
            method=api.method,
            url=gen_url(api),
            args='' if isinstance(api.params, Any) else ',\n' + ',\n'.join((tpl.ARG.format(
                arg=arg
            ) for arg in api.params.as_params()))
        )
    ) for api in Api.apis)) + f'\n\n{config["methods-flag"]["end"]}\n', template))
    complete(config['apis'])

with open(config['doc'], 'w', encoding='utf-8') as doc_output:
    doc_output.write(tpl.DOC.format(
        
    ))
    complete(config['doc'])
    

print(f'用时{perf_counter() - begin}秒')