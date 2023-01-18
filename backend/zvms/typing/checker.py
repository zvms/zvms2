
class Named:
    def __init__(self, raw, name):
        self.raw = raw
        self.name = name

    def __call__(self, json):
        return self.raw(json)

    def __str__(self):
        return self.name


# 下面的谓词开头大写是因为它们有"类型"的含义(虽然实际上不是), 同时还避免了与内置函数重名
Any = Named(lambda _: True, 'any')
Int = Named(lambda x: isinstance(x, int), 'number(int)')
Float = Named(lambda x: isinstance(x, float), 'number(float)')
Number = Named(lambda x: isinstance(x, (int, float)), 'number')
Boolean = Named(lambda x: isinstance(x, bool), 'boolean')
Null = Named(lambda x: x is None, 'null')


class String:
    def __init__(self, max_length=None):
        self.max_length = max_length

    def __call__(self, json):
        return isinstance(json, (list, tuple)) and (self.max_length is None or len(json) <= self.max_length)

    def __str__(self):
        return 'string' + '' if self.max_length is None else f'({self.max_length})'


class Array:
    def __init__(self, sub, allow_empty=False):
        self.sub = sub
        self.allow_empty = allow_empty

    def __call__(self, json):
        if not isinstance(json, list):
            return False
        for i in json:
            if not self.sub(i):
                return False
        return self.allow_empty or json

    def __str__(self):
        return f'[{self.sub}, ...]{"" if self.allow_empty else "(不可为空)"}'


class Object:
    def __init__(self, **members):
        self.members = members

    def __call__(self, json):
        if not isinstance(json, dict):
            return False
        for k, v in self.members.items():
            if k not in json or not v(json[k]):
                return False
        return True

    def __str__(self):
        return '{' + ', '.join(map(lambda p: f'"{p[0]}": {p[1]}', self.members.items())) + '}'


class Extends(Object):
    def __init__(self, super, **members):
        self.members = super.members | members


class Union:
    def __init__(self, *options):
        self.options = options

    def __call__(self, json):
        for i in self.options:
            if i(json):
                return True
        return False

    def __str__(self):
        return '(' + ' | '.join(map(str, self.options)) + ')'


class Intersection:
    def __init__(self, *items):
        self.items = items

    def __call__(self, json):
        for i in self.items:
            if not i(json):
                return False
        return True

    def __str__(self):
        return '(' + ' & '.join(map(str, self.options)) + ')'


class Literal:
    def __init__(self, *literals):
        self.literals = literals

    def __call__(self, json):
        return json in self.literals

    def __str__(self):
        return '(' + ', '.join(map(Literal.__literal_to_str, self.literals)) + ')'

    @staticmethod
    def __literal_to_str(literal):
        if isinstance(literal, (int, float)):
            return str(literal)
        if isinstance(literal, bool):
            return 'true' if literal else 'false'
        if isinstance(literal, str):
            return f'"{literal}"'
        if literal is None:
            return 'null'
