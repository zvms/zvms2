import os.path

from .rule import Rule
from .util import print_, split

class App:
    def __init__(self, name: str, doc = '', **config: dict[str, str]):
        self.name = name
        self.__doc__ = doc
        self.__routes = []
        self.__children = []
        self.config = {
            'prompt': '> ', 
            'cmd_not_found': '未找到命令',
            'failed_to_open': '打开文件失败',
            'autorun': 'autorun.sh',
            'help': ('help', ), 
            'exit': ('exit', ), 
            'vars': ('vars', ), 
            'del': ('del', ), 
            'export': ('export', ), 
            'set': ('set', ), 
            'source': ('source', ), 
            'vars_cfg': 'vars.cfg'
        }
        self.config.update(config)

    def route(self, rule: str):
        def deco(view):
            self.__routes.append((Rule(rule), view))
            return view
        return deco

    def register(self, child: 'App') -> None:
        self.__children.append(child)

    def help(self, args: tuple[str]) -> None:
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
        print()

    def run(self, cmd: list[str]):
        for rule, view in self.__routes:
            r = rule.interpret(cmd)
            if r:
                view(*r[0], **r[1])
                return True
        for child in self.__children:
            if child.run(cmd):
                return True
        return False

    def run_script(self, f, vars, config):
        for line in f:
            if not self.run(split(line, vars)):
                print(config['cmd_not_found'])

    def run_shell(self, **config: dict[str, str]):
        config |= self.config
        App.config = config
        vars = {}
        if os.path.exists(config['vars_cfg']):
            with open(config['vars_cfg'], 'r') as f:
                for line in f:
                    if line[0].isspace():
                        continue
                    eq = line.index('=')
                    vars[line[:eq]] = line[eq + 1:-1]
                vars_export = vars.copy()
        else:
            vars_export = {}
        print_(config.get('title'))
        try:
            f = open(config['autorun'])
            self.run_script(f, vars, config)
        except OSError:
            pass
        while True:
            line = input(config['prompt'])
            cmd = split(line)
            if not cmd:
                continue
            if cmd[0] in config['exit']:
                with open(config['vars_cfg'], 'w') as f:
                    for k, v in vars_export.items():
                        f.write(f'{k}={v}\n')
                return
            elif cmd[0] in config['help']:
                self.help(cmd[1:])
            elif cmd[0] in config['vars']:
                for k, v in vars.items():
                    print(f'{k}={v}')
            elif cmd[0] in config['del']:
                if len(cmd) == 1 or cmd[1] not in vars:
                    print(config['cmd_not_found'])
                else:
                    del vars[cmd[1]]
                    if cmd[1] in vars_export:
                        del vars_export[cmd[1]]
            elif cmd[0] in config['set']:
                if len(cmd) < 3:
                    print(config['cmd_not_found'])
                else:
                    vars[cmd[1]] = cmd[2]
            elif cmd[0] in config['export']:
                if len(cmd) < 3:
                    print(config['cmd_not_found'])
                else:
                    vars[cmd[1]] = cmd[2]
                    vars_export[cmd[1]] = cmd[2]
            elif cmd[0] in config['source']:
                if len(cmd) == 1:
                    print(config['cmd_not_found'])
                else:
                    try:
                        f = open(cmd[1])
                        self.run_script(f, vars, config)
                    except OSError:
                        print(config['failed_to_open'])
                        continue
            elif cmd[0] in vars:
                print(f'{cmd[0]}={vars[cmd[0]]}')
            else:
                if not self.run(split(line, vars)):
                    print(config['cmd_not_found'])