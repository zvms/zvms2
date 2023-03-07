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

INTERFACE_MEMBER = '''    {field}{colon} {value}'''

TYPE = '''export type {name} = {alias}

'''

API = '''  /**{docstring}
   * ### [{method}] {rule}
   * #### 权限: {auth}{params_anno}
   */
  {name}({params}): ForegroundApiRunner<{response}> {{
    return createForegroundApiRunner({create_args});
  }}
'''

DOCSTRING = '''
   * ## {docstring}'''

PARAM_ANNO = '''   * @param {name}'''

PARAM = '''    {name}: {type}'''

CREATE_NO_PARAMS = '''this, "{method}", `{url}`'''

CREATE = '''
      this,
      "{method}",
      `{url}`{args}
    '''

ARG = '''      {arg}'''

DOC = '''# 镇海中学义工管理系统API文档
{modules}
'''

MODULE = '''## {i}.{name}
### **{summary}**
{apis}

---

'''

API_DOC = '''
#### {i}.{j} {name}
[{method}] {rule}  
**{docstring}**  
参数: 
```json
{params}
```
响应:  
```json
{response}
```
'''