import hy
from time import perf_counter
start = perf_counter()
hy.macros.require('hyrule', None, assignments=[['case', 'case']], prefix='')
from enum import IntEnum, IntFlag
from collections import defaultdict
from itertools import chain
from operator import itemgetter
import enum as e
import json
import sys
import re
import os
import yaml
import zvms.res as res
import zvms.typing.structs as structs
import zvms.typing.checker as checker
import zvms.views as views
from zvms.typing.checker import *
from zvms.apilib import Api

def write_file(file_name, *content):
    _hy_anon_var_1 = None
    with open(file_name, 'w', encoding='utf-8') as f:
        _hy_anon_var_1 = f.write(str.join('', content))
    return print(os.path.realpath(file_name), '生成完成!')
hy.macros.macro('for/join')(lambda hyx_XampersandXcompiler, sep, it, *body: hy.models.Expression([hy.models.Expression([hy.models.Symbol('.'), hy.models.Symbol('str'), hy.models.Symbol('join')]), sep, hy.models.Expression([hy.models.Symbol('gfor'), *(it or []), hy.models.Expression([hy.models.Expression([hy.models.Symbol('.'), hy.models.Symbol('str'), hy.models.Symbol('join')]), hy.models.String(''), hy.models.Expression([hy.models.Symbol('map'), hy.models.Symbol('str'), hy.models.Tuple([*(body or [])])])])])]))

def convert(ident, src, dst):
    _hyx_case_keyXUffffX1 = src
    _hy_let_elems_2 = map(str.lower, ident.split('_') if _hyx_case_keyXUffffX1 == hy.models.Symbol('snake') else ident.split('_') if _hyx_case_keyXUffffX1 == hy.models.Symbol('upper_snake') else chain((re.match('^[a-z]*', ident).group(),), re.findall('[A-Z][a-z]*', ident)) if _hyx_case_keyXUffffX1 == hy.models.Symbol('camel') else re.findall('[A-Z][a-z]*', ident) if _hyx_case_keyXUffffX1 == hy.models.Symbol('pascal') else ident.split('-') if _hyx_case_keyXUffffX1 == hy.models.Symbol('lisp') else ident.split('/') if _hyx_case_keyXUffffX1 == hy.models.Symbol('url') else ident.split() if _hyx_case_keyXUffffX1 == hy.models.Symbol('text') else None)
    _hyx_case_keyXUffffX2 = dst
    if _hyx_case_keyXUffffX2 == hy.models.Symbol('snake'):
        _hy_anon_var_6 = str.join('_', _hy_let_elems_2)
    else:
        if _hyx_case_keyXUffffX2 == hy.models.Symbol('upper_snake'):
            _hy_anon_var_5 = str.join('_', map(str.upper, _hy_let_elems_2))
        else:
            if _hyx_case_keyXUffffX2 == hy.models.Symbol('camel'):
                _hy_let_iter_3 = iter(_hy_let_elems_2)
                _hy_anon_var_4 = next(_hy_let_iter_3) + str.join('', map(str.capitalize, _hy_let_iter_3))
            else:
                _hy_anon_var_4 = str.join('', map(str.capitalize, _hy_let_elems_2)) if _hyx_case_keyXUffffX2 == hy.models.Symbol('pascal') else str.join('-', _hy_let_elems_2) if _hyx_case_keyXUffffX2 == hy.models.Symbol('lisp') else None
            _hy_anon_var_5 = _hy_anon_var_4
        _hy_anon_var_6 = _hy_anon_var_5
    return _hy_anon_var_6
categs = sorted(((k, v) for [k, v] in res.Categ.__dict__.items() if type(v) == res.Categ), key=itemgetter(1), reverse=True)

def hyx_auth_XgreaterHthan_signXstring(auth):
    if auth == 0:
        _hy_anon_var_7 = ()
    else:
        for [k, v] in categs:
            hy.models.Keyword('if')
            auth & v and v <= auth
            return chain((convert(k, hy.models.Symbol('upper_snake'), hy.models.Symbol('pascal')),), hyx_auth_XgreaterHthan_signXstring(auth & ~v))
        _hy_anon_var_7 = None
    return _hy_anon_var_7
_hy_anon_var_8 = None
with open('genconfig.yaml', encoding='utf-8') as config_file:
    config = yaml.full_load(config_file.read())
    _hy_anon_var_8 = None
_hy_anon_var_9 = None
with open(config['enums-mapping'], encoding='utf-8') as mapping_file, open(config['apis-template'], encoding='utf-8') as template_file:
    mapping = yaml.full_load(mapping_file.read())
    template = template_file.read()
    _hy_anon_var_9 = None
write_file(config['enums'], str.join('\n', (str.join('', map(str, ('export enum ', enum.__name__, '{\n', str.join(',\n', (str.join('', map(str, ('    ', field, ' = ', value))) for [field, value] in valid_cons)), '\n}\n\nexport function get', enum.__name__, 'Name(id:', enum.__name__, '): string {\nswitch (id) {\n', str.join('', (str.join('', map(str, ('        case ', enum.__name__, '.', field, ':\n        return "', map_this[field], '";\n'))) for [field, _] in valid_cons)), '        default:\n        throw new Error("Invalid enum value");\n}\n}'))) for enum in res.__dict__.values() if isinstance(enum, type) and issubclass(enum, e.Enum) and (enum not in (IntEnum, IntFlag)) for map_this in (mapping[enum.__name__],) for valid_cons in ([(convert(field, hy.models.Symbol('upper_snake'), hy.models.Symbol('pascal')), value) for [field, value] in enum.__dict__.items() if type(value) == enum],))))
write_file(config['structs'], 'import * as enums from "./enums;";\n\n', str.join('', (str.join('', map(str, ((f'/* {struct.__doc__} */\n' if struct.__doc__ is not None else '') + 'export interface ' + struct.__name__ + ('' if struct.__base__ in (Object, Optional) else f' extends {struct.__base__.__name__}') + '{\n' + str.join(',\n', (str.join('', map(str, ('    ' + field + ('?: ' if issubclass(struct, Optional) else ': ') + value.render(),))) for [field, value] in struct.__dict__.items() if isinstance(value, Checker))) + '\n}\n' if isinstance(struct, type) and issubclass(struct, Object) and (struct not in (Object, Optional)) else f'export type {name} = {struct.render()}\n' if isinstance(struct, Checker) and (not hasattr(checker, name)) else '' if True else None,))) for [name, struct] in structs.__dict__.items())))
rule_methods_block = re.compile(str.format('{}.+{}', config['methods-flag']['start'], config['methods-flag']['end']), re.S)
rule_to_url = re.compile('(.+?)\\<(?:int:)?(.+?)\\>')
rule_to_url_sub = '\\1${\\2}'
Object.module = 'structs.'

def gen_url(api):
    return rule_to_url.sub(rule_to_url_sub, api.rule)

def is_has_params(api):
    return api.url_params or not isinstance(api.params, Any)
if False:
    _hy_let_args_11, _hy_let_params_10 = None

def _hy_anon_var_13():
    global _hy_let_args_11, _hy_let_params_10
    for api in Api.apis:
        if not is_has_params(api):
            _hy_anon_var_12 = 'this, "' + api.method + '", `' + gen_url(api) + '`'
        else:
            _hy_let_params_10 = api.params.as_params()
            _hy_let_args_11 = '' if isinstance(api.params, Any) else str.join(',\n', (str.join('', map(str, ('        ', arg))) for arg in api.params.as_params()))
            _hy_anon_var_12 = '\n      this,\n      "' + api.method + '",\n      `' + gen_url(api) + (('`, {\n' + _hy_let_args_11 + '\n      }' if _hy_let_params_10 else '`,\n      {}') if api.method == 'POST' else '?` + toURLSearchParams(\n' + _hy_let_args_11 + '\n      )' if _hy_let_params_10 else '`') + '\n    '
        yield str.join('', map(str, ('  /**', '' if api.func.__doc__ is None else '\n   * ## ' + api.func.__doc__, '\n   * ### [', api.method, '] ', api.rule, '\n   * #### 权限: ', str.join(' | ', hyx_auth_XgreaterHthan_signXstring(api.auth)), '' if not is_has_params(api) else '\n' + str.join('\n', (str.join('', map(str, ('   * @param ', name))) for name in chain(api.url_params, api.params.as_params()))), '\n   */\n  ', convert(api.func.__name__, hy.models.Symbol('snake'), hy.models.Symbol('camel')), '(', '' if not is_has_params(api) else '\n' + str.join(',\n', (str.join('', map(str, ('    ', name, ': ', type))) for [name, type] in chain(api.url_params.items(), api.params.as_params().items()))) + '\n  ', '): ForegroundApiRunner<', api.response.render(), '> {\n    return createForegroundApiRunner(', _hy_anon_var_12, ');\n  }\n')))
write_file(config['apis'], rule_methods_block.sub(config['methods-flag']['start'] + '\n' + str.join('', _hy_anon_var_13()) + '\n\n' + config['methods-flag']['end'] + '\n', template))
_hy_let_modules_14 = defaultdict(list)
for api in Api.apis:
    _hy_let_modules_14[api.func.__module__].append(api)
write_file(config['doc'], '# 镇海中学义工管理系统API文档\n\n' + str.join('', (str.join('', map(str, ('## ', i, '.', module, '\n\n### **', sys.modules[module].__dict__.get('SUMMARY', '...'), '**\n', str.join('', (str.join('', map(str, ('\n#### ', i, '.', j, ' ', module, '\n\n[', api.method, '] ', api.rule, '  \n**', api.func.__doc__ or '...', '**  \n\n参数:\n```json\n', json.dumps(api.params.as_json(), indent=4), '\n```\n响应:\n```json\n', json.dumps(api.response.as_json(), indent=4), '\n```\n'))) for [j, api] in enumerate(apis, 1)))))) for [i, [module, apis]] in enumerate(_hy_let_modules_14.items(), 1))))
print(perf_counter() - start)