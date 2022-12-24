from .elems import Ident, Param, Option
from .util import split

class Rule:
    def __init__(self, rule: str):
        self.kwargs = {}
        self.__elems = []
        self.__options = {}
        option = ''
        anno = False
        for s in split(rule):
            if s.startswith('-'):
                if s.endswith(':'):
                    option = s[:-1]
                    anno = True
                else:
                    option = s
                self.__options[option] = Option(option, self)
            elif option:
                if anno:
                    self.__options[option].anno = s
                elif s.startswith('<') and s.endswith('>'):
                    self.__options[option].add_param(s)
                else:
                    option = ''
                    self.__elems.append(Ident(s))
                anno = False
            elif s.startswith('<') and s.endswith('>'):
                self.__elems.append(Param(s, self))
            else:
                self.__elems.append(Ident(s))

    def help(self):
        for elem in self.__elems:
            print(elem.name, end=' ')
        if self.__options:
            print('\n可选的参数')
            for option in self.__options.values():
                option.help()
        else:
            print()

    def interpret(self, cmd):
        self.kwargs.clear()
        elem_iter = iter(self.__elems)
        cmd_iter = iter(cmd)
        while True:
            try:
                c = next(cmd_iter)
            except StopIteration:
                try:
                    c = next(elem_iter)
                    return None
                except StopIteration:
                    return self.kwargs.copy()
            if c in self.__options:
                if not self.__options[c].match(cmd_iter):
                    return None
                continue
            try:
                if not next(elem_iter).match(c):
                    return None
            except StopIteration:
                return None
