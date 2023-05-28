import os.path
import traceback
import sys

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
            'failed_to_read': '读取文件失败',
            'autorun': 'autorun.sh',
            'info': '输入help -a获取帮助',
            'on_exiting': [],
            'help': ('help', ), 
            'exit': ('exit', ), 
            'vars': ('vars', ), 
            'del': ('del', ), 
            'export': ('export', ), 
            'set': ('set', ), 
            'source': ('source', ), 
            'eval': ('eval', ), 
            'exec': ('exec', ), 
            'restart': ('restart', ),
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
                print()
        if not args:
            print_(self.__doc__)
            help_route()
            for child in self.__children:
                child.help(())
        else:
            if args[0] == '-a':
                    print(f'''{' '.join(self.config['help'])} 获取帮助
    -a 全局帮助
    -i 子模块索引
    <name> 子模块帮助
    (无参数) 全部帮助
{' '.join(self.config['vars'])} 查看所有变量
{' '.join(self.config['del'])} 删除变量
{' '.join(self.config['export'])} 导出变量
{' '.join(self.config['source'])} 执行脚本
{' '.join(self.config['eval'])} 执行Python表达式
{' '.join(self.config['exec'])} 执行Python语句
{' '.join(self.config['exit'])} 退出
''', end='')
            for child in self.__children:
                if args[0] == '-i':
                    print(child.name)
                elif args[0] == child.name:
                    child.help(args[1:])
        print()

    def run(self, cmd: list[str]):
        for rule, view in self.__routes:
            r = rule.interpret(cmd)
            if r is not None:
                view(**r)
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
        config = self.config | config
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
        print_(config.get('info'))
        try:
            f = open(config['autorun'])
            self.run_script(f, vars, config)
        except OSError:
            pass
        while True:
            line = input(config['prompt'])
            cmd = split(line)
            def check(length):
                return print(config['cmd_not_found']) if len(cmd) < length else True
            if not cmd:
                continue
            if cmd[0] in config['exit']:
                for func in config['on_exiting']:
                    func()
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
                if check(3):
                    vars[cmd[1]] = cmd[2]
            elif cmd[0] in config['export']:
                if check(3):
                    vars[cmd[1]] = cmd[2]
                    vars_export[cmd[1]] = cmd[2]
            elif cmd[0] in config['source']:
                if check(2):
                    try:
                        f = open(cmd[1])
                        self.run_script(f, vars, config)
                    except OSError:
                        print(config['failed_to_read'])
                        continue
            elif cmd[0] in config['eval']:
                if check(2):
                    try:
                        ret = eval(split(line, vars)[1],)
                        if ret is not None:
                            print(ret)
                    except:
                        traceback.print_exc()
            elif cmd[0] in config['exec']:
                if check(2):
                    try:
                        exec(split(line, vars)[1],)
                    except:
                        traceback.print_exc()
            elif cmd[0] in config['restart']:
                __import__(sys.argv[0][:-3])
                return
            elif cmd[0] in vars:
                print(f'{cmd[0]}={vars[cmd[0]]}')
            else:
                if not self.run(split(line, vars)):
                    print(config['cmd_not_found'])