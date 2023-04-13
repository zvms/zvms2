from contextlib import contextmanager
import datetime

class CheckerError(Exception):
    message: str

class Checker:
    def __call__(self):
        return self

    def render(self): ...

    def stringify(self):
        return self.render()

    def check(self, json): ...

    def as_json(self):
        return self.stringify()
    
    where = []

    @contextmanager
    def path(s: str):
        Checker.where.append(s)
        yield
        Checker.where.pop()

    def error(expected: 'Checker', found):
        where = '.'.join(Checker.where)
        Checker.where.clear()
        raise CheckerError(where, expected.as_json(), found)

class Any(Checker):
    def render(self):
        return '{}'

    def stringify(self):
        return 'any'

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
            Checker.error(self, json)
        for k, v in self.fields():
            with Checker.path(k):
                if k not in json:
                    Checker.error(v, None)
                v.check(json[k])

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
        if not isinstance(json, self.type):
            Checker.error(self, json)

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
        except (ValueError, TypeError):
            print('!!!')
            Checker.error(self, json)

DateTime = String

class Array(Checker):
    def __init__(self, item):
        self.item = item

    def render(self):
        return f'Array<{self.item.render()}>'

    def check(self, json):
        if not isinstance(json, (list, tuple)):
            Checker.error(self, json)
        for i, item in enumerate(json):
            with Checker.path(f'[{i}]'):
                self.item.check(item)

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
                return
        Checker.error(self, json)

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
        self.simple.check(json)
        if not (self.min == '' or json >= self.min) and (self.max == '' or json < self.max):
            Checker.error(self, json)

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
        self.simple.check(json) 
        if not (self.min == '' or len(json) >= self.min) and (self.max == '' or len(json) < self.max):
            Checker.error(self, json)

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
        except (ValueError, TypeError):
            Checker.error(self, json)

class ParsableEnum(Enum):
    def check(self, json):
        try:
            int(json)
        except ValueError:
            Checker.error(self, json)
        super().check(int(json))

class Optional(Object):
    def check(self, json):
        fields = dict(self.fields())
        if not isinstance(json, dict):
            Checker.error(self, json)
        for k, v in json.items():
            with Checker.path(k):
                if k in fields:
                    fields[k].check(v)

    def as_params(self):
        return {'kwargs': self.render()}
