class Ident:
    def __init__(self, name: str):
        self.name = name
    def match(self, cmd):
        return cmd == self.name

class Param:
    def __init__(self, name: str, master):
        self.name = name
        self.__master = master

    def match(self, cmd: str):
        if 'int:' in self.name:
            try:
                self.__master.kwargs[self.name[5:-1]] = int(cmd)
                return True
            except ValueError:
                return False
        self.__master.kwargs[self.name[1:-1]] = cmd
        return True

class VarParams:
    def __init__(self, name: str, master):
        self.name = name
        self.__master = master
        self.__params = []

    def add_param(self, param: Param):
        self.__params.append(Param(f"<{param}>", self))
    
    def ready(self):
        self.__params_iter = iter(self.__params)

    def match(self, cmd: str):
        if self.name not in self.__master.kwargs:
            self.__master.kwargs[self.name] = [{}]
        self.kwargs = self.__master.kwargs[self.name][-1]
        try:
            p = next(self.__params_iter)
        except StopIteration:
            self.__master.kwargs[self.name].append({})
            self.__params_iter = iter(self.__params)
            self.kwargs = self.__master.kwargs[self.name][-1]
            p = next(self.__params_iter)
        if not p.match(cmd):
            return False
        return True

    def ok(self):
        if self.name not in self.__master.kwargs:
            self.__master.kwargs[self.name] = []
            return True
        try:
            next(self.__params_iter)
            return False
        except StopIteration:
            return True

    def help(self):
        print(self.name, end= '')
        for param in self.__params:
            print(param.name, end=' ')
        print()

class Option:
    def __init__(self, name: str, master):
        self.name = name
        self.__master = master
        self.anno = ''
        self.kwargs = {}
        self.__params = []

    def match(self, cmd_iter):
        self.kwargs.clear()
        param_iter = iter(self.__params)
        while True:
            try:
                p = next(param_iter)
            except StopIteration:
                if self.name.endswith(':'):
                    slice = self.name[1:-1]
                else:
                    slice = self.name[1:]
                self.__master.kwargs[slice] = self.kwargs.copy()
                return True
            try:
                if not p.match(next(cmd_iter)):
                    return False
            except StopIteration:
                return False

    def add_param(self, param: str):
        self.__params.append(Param(param, self))

    def help(self):
        print(self.name, end=' ')
        for param in self.__params:
            print(param.name, end=' ')
        if self.anno:
            print(':', self.anno, end='')
        print()
