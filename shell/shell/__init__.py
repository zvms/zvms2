from .rule import Rule
from .util import print_, split

class App:
    def __init__(self, name, doc = '', **config):
        self.name = name
        self.__doc__ = doc
        self.__routes = []
        self.__children = []
        self.config = {'prompt': '> ', 'help': ('help', ), 'exit': ('exit', )}
        self.config.update(config)

    def route(self, rule):
        def deco(view):
            self.__routes.append((Rule(rule), view))
            return view
        return deco

    def register(self, child):
        self.__children.append(child)

    def help(self, args):
        def help_route():
            for rule, view in self.__routes:
                rule.help()
                if view.__doc__:
                    print(view.__doc__)
        if not args:
            print_(self.__doc__)
            help_route()
            for child in self.__children:
                child.help(())
        else:
            for child in self.__children:
                if args[0] == '-i':
                    print(child.name)
                elif args[0] == child.name:
                    child.help(args[1:])

    def run(self, cmd):
        for rule, view in self.__routes:
            r = rule.interpret(cmd)
            if r:
                view(*r[0], **r[1])
                return True
        for child in self.__children:
            if child.run(cmd):
                return True
        return False

    def run_shell(self, **config):
        config |= self.config
        App.config = config
        print_(config.get('title'))
        while True:
            cmd = split(input(config['prompt']))
            if not cmd:
                continue
            if cmd[0] in config['exit']:
                return
            if cmd[0] in config['help']:
                self.help(cmd[1:])
            else:
                if not self.run(cmd):
                    print('未找到命令')