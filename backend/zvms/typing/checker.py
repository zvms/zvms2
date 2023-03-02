import datetime

class Checker:
    def __call__(self):
        return self

    def render(self): pass

    def stringify(self):
        return self.render()

    def check(self, json): pass

    def as_json(self):
        return self.stringify()

class Any(Checker):
    def render(self):
        return '{}'

    def stringify(self):
        return 'any'

    def check(self, json):
        return True

    def as_params(self):
        return {}

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
            if k not in json or not(v.check(json[k])):
                return False
        return True

    def as_params(self):
        return {k: v.render() for k, v in self.fields()}

    def as_json(self):
        return dict(((k, v.as_json()) for k, v in self.fields()))

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

    def as_json(self):
        return [self.item.as_json()]

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

    def as_json(self):
        return [i.as_json() for i in self.elems]

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

    def as_json(self):
        return self.simple.as_json()

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

    def as_json(self):
        return self.simple.as_json()

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

class ParsableEnum(Enum):
    def check(self, json):
        return isinstance(json, int) and super().check(self, int(json))

class Optional(Object):
    def check(self, json):
        fields = dict(fields)
        if not isinstance(json, dict):
            return False
        for k, v in json.items():
            if k in fields.keys() and not v.check(fields[k]):
                return False
        return True

    def as_params(self):
        return {'kwargs': self.render()}
