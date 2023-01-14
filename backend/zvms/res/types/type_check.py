
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
String = Named(lambda x: isinstance(x, str), 'string')
Null = Named(lambda x: x is None, 'null')


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
