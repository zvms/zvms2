import datetime

class Checker:
    def render(self): pass

    def stringify(self):
        return self.render()

    def check(self, json): pass

class Any(Checker):
    def render(self):
        return '{}'

    def stringify(self):
        return 'any'

    def check(self, json):
        return True

def all(cls):
    return {} if cls is None else cls.__dict__ | cls.__base__.__dict__
        
class Object(Checker):
    module = ''

    @classmethod
    def fields(cls):
        return ((k, v) for k, v in all(cls).items() if isinstance(v, Checker))

    def render(self):
        return f'{Object.module}{type(self).__name__}'

    def stringify(self):
        return '{' + ', '.join((f'"{k}": {v.render()}' for k, v in self.fields())) + '}'

    def check(self, json):
        if not isinstance(json, dict):
            return False
        for k, v in self.fields():
            if k not in json or not(v(json[k])):
                return False
        return True

class Simple(Checker):
    def __init__(self, type, tsname, name=None):
        self.type = type
        self.tsname = tsname
        self.name = name or tsname

    def render(self):
        return self.tsname

    def strify(self):
        return self.name

    def check(self, json):
        return isinstance(json, self.type)

String = Simple(str, 'string')
Int = Simple(int, 'number', 'int')
Float = Simple(float, 'number', 'float')
Boolean = Simple(bool, 'boolean')
Null = Simple(type(None), 'null')

class Parsable(Checker):
    def __init__(self, simple):
        self.simple = simple

    def render(self):
        return self.simple.render()

    def check(self, json):
        try:
            self.simple.type(json)
            return True
        except (ValueError, TypeError):
            return False

DateTime = Parsable(Simple(datetime.datetime, 'string', 'datetime'))

class Array(Checker):
    def __init__(self, item):
        self.item = item

    def render(self):
        return f'{self.item.render()}[]'

    def check(self, json):
        if not isinstance(json, (list, tuple)):
            return False
        for item in json:
            if not self.item.check(item):
                return False
        return True

class Union(Checker):
    def __init__(self, *elems):
        self.elems = elems

    def render(self):
        return ' | '.join((i.render() for i in self.elems))

    def stringify(self):
        return f'({self.render()})'

    def check(self, json):
        for elem in self.elems:
            if elem.check(json):
                return True
        return False

number = Union(Int, Float)

class Range(Checker):
    def __init__(self, simple, min='', max=''):
        self.simple = simple
        self.min = min
        self.max = max

    def render(self):
        return self.simple.render()

    def stringify(self):
        return f'{self.simple.stringify()}({self.min}...{self.max})'

    def check(self, json):
        return self.simple.check(json) and (self.min == '' or json >= self.min) and (self.max == '' or json < self.max)

class Len(Checker):
    def __init__(self, simple, min='', max=''):
        self.simple = simple
        self.min = min
        self.max = max

    def render(self):
        return self.simple.render()

    def stringify(self):
        return f'{self.simple.stringify()}({self.min}, {self.max})'

    def check(self, json):
        return self.simple.check(json) and (self.min == '' or len(json) >= self.min) and (self.max == '' or len(json) < self.max)

class Enum(Checker):
    def __init__(self, enum):
        self.enum = enum

    def render(self):
        return f'enums.{self.enum.__name__}'

    def stringify(self):
        return self.enum.__name__

    def check(self, json):
        try:
            self.enum(json)
            return True
        except (ValueError, TypeError):
            return False

class Optional(Object):
    def check(self, json):
        fields = dict(fields)
        if not isinstance(json, dict):
            return False
        for k, v in json.items():
            if k in fields.keys() and not v(fields[k]):
                return False
        return True

# class Named:
#     def __init__(self, raw, name):
#         self.raw = raw
#         self.name = name

#     def __call__(self, json):
#         return self.raw(json)

#     def __str__(self):
#         return self.name

# def parsable(type, value):
#     try:
#         type(value)
#         return True
#     except (TypeError, ValueError):
#         return False


# # 下面的谓词开头大写是因为它们有"类型"的含义(虽然实际上不是), 同时还避免了与内置函数重名
# Any = Named(lambda _: True, 'any')
# Int = Named(lambda x: isinstance(x, int), 'number(int)')
# Float = Named(lambda x: isinstance(x, float), 'number(float)')
# Number = Named(lambda x: isinstance(x, (int, float)), 'number')
# UrlInt = Named(lambda x: parsable(int, x), 'int')
# UrlFloat = Named(lambda x: parsable(float, x), 'float')
# Boolean = Named(lambda x: isinstance(x, bool), 'boolean')
# Null = Named(lambda x: x is None, 'null')


# class String:
#     def __init__(self, max_length=None):
#         self.max_length = max_length

#     def __call__(self, json):
#         return isinstance(json, str) and (self.max_length is None or len(json) <= self.max_length)

#     def __str__(self):
#         return 'string' + ('' if self.max_length is None else f'({self.max_length})')


# class Array:
#     def __init__(self, sub, allow_empty=False, distinct=True):
#         self.sub = sub
#         self.allow_empty = allow_empty
#         self.distinct = distinct

#     def __call__(self, json):
#         if not isinstance(json, (list, tuple)):
#             return False
#         for i in json:
#             if not self.sub(i) or (self.distinct and json.count(i) > 1):
#                 return False
#         return self.allow_empty or json

#     def __str__(self):
#         return f'[{self.sub}, ...]{"" if self.allow_empty else "(不可为空)"}{"(不可重复)" if self.distinct else ""}'


# class Object:
#     def __init__(self, **members):
#         self.members = members

#     def __call__(self, json):
#         if not isinstance(json, dict):
#             return False
#         for k, v in self.members.items():
#             if k not in json or not v(json[k]):
#                 return False
#         return True

#     def __str__(self):
#         return '{' + ', '.join(map(lambda p: f'"{p[0]}": {p[1]}', self.members.items())) + '}'


# class Extends(Object):
#     def __init__(self, super, **members):
#         self.members = super.members | members


# class Optional:
#     def __init__(self, **options):
#         self.options = options

#     def __call__(self, json):
#         if not isinstance(json, dict):
#             return False
#         for k, v in json.items():
#             if k in self.options and not self.options[k](v):
#                 return False
#         return True

#     def __str__(self):
#         return '{*, ' + ', '.join(map(lambda p: f'"{p[0]}": {p[1]}', self.options.items())) + '}'


# class Union:
#     def __init__(self, *options):
#         self.options = options

#     def __call__(self, json):
#         for i in self.options:
#             if i(json):
#                 return True
#         return False

#     def __str__(self):
#         return '(' + ' | '.join(map(str, self.options)) + ')'


# class Intersection:
#     def __init__(self, *items):
#         self.items = items

#     def __call__(self, json):
#         for i in self.items:
#             if not i(json):
#                 return False
#         return True

#     def __str__(self):
#         return '(' + ' & '.join(map(str, self.options)) + ')'


# class Literal:
#     def __init__(self, *literals):
#         self.literals = literals

#     def __call__(self, json):
#         try:
#             return json in self.literals or int(json) in self.literals
#         except (ValueError, TypeError):
#             return False

#     def __str__(self):
#         return '(' + ', '.join(map(Literal.__literal_to_str, self.literals)) + ')'

#     @staticmethod
#     def __literal_to_str(literal):
#         if isinstance(literal, (int, float)):
#             return str(literal)
#         if isinstance(literal, bool):
#             return 'true' if literal else 'false'
#         if isinstance(literal, str):
#             return f'"{literal}"'
#         if literal is None:
#             return 'null'
