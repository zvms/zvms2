ENUMS = '''export enum {name} {{
{body}
}}

export function get{name}Name(id: {name}): string {{
    switch (id) {{
{switch_body}        default:
            throw Error("Invalid enum value");
    }}
}}

'''

ENUM_CONSTRUCTOR = '''    {field} = {value}'''

SWITCH_CASE = '''        case {enum}.{field}:
            return "{name}";
'''

STRUCTS_HEADER = '''import * as enums from "././enums";'''

INTERFACE = '''export interface {name}{inheritance} {{
{body}
}}

'''

INHERITANCE = ''' extends {base}'''

INTERFACE_MEMBER = '''    {field}: {value}'''

TYPE = '''export type {name} = {alias}

'''

API = ''''''