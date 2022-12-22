class Ident:
    def __init__(self, name):
        self.name = name
    def match(self, cmd):
        return cmd == self.name

class Param:
    def __init__(self, name, master):
        self.name = name
        self.__master = master

    def match(self, cmd):
        if 'int:' in self.name:
            try:
                self.__master.args.append(int(cmd))
                return True
            except ValueError:
                return False
        self.__master.args.append(cmd)
        return True

class Option:
    def __init__(self, name, master):
        self.name = name
        self.__master = master
        self.anno = ''
        self.args = []
        self.__params = []

    def match(self, cmd_iter):
        self.args.clear()
        param_iter = iter(self.__params)
        while True:
            try:
                p = next(param_iter)
            except StopIteration:
                if self.name[-1] == ':':
                    slice = self.name[1:-1]
                else:
                    slice = self.name[1:]
                self.__master.kwargs[slice] = self.args.copy()
                return True
            try:
                if not p.match(next(cmd_iter)):
                    return False
            except StopAsyncIteration:
                return False

    def add_param(self, param):
        self.__params.append(Param(param, self))

    def help(self):
        print(self.name, end=' ')
        for param in self.__params:
            print(param.name, end=' ')
        if self.anno:
            print(':', self.anno)
        print()
