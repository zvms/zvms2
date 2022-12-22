def split(raw: str):
    literal = False
    s = ''
    ret = []
    def append():
        nonlocal s
        ret.append(s[1:-1] if s[0] == '|' and s[-1] == '|' else s)
        s = ''
    for c in raw:
        if c == '|':
            literal = not literal
        if c.isspace() and not literal:
            if s:
                append()
            s = ''
        else:
            s += c
    if s:
        append()
    return ret

def print_(s):
    if s:
        print(s)
        print()