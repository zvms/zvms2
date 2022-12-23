# what the fuck?
def split(raw: str, vars: dict[str, str]={}) -> list[str]:
    ret = []
    literals = {"'": 0, '"': 0}
    s = ''
    def append():
        nonlocal s
        if s[0] == "'":
            s = s[1:-1]
        elif s[0] == '"':
            bar = split(s[1:-1])
            for i in range(len(bar)):
                if bar[i][0] == '$' and bar[i][1:] in vars:
                    bar[i] = vars[bar[i][1:]]
            s = ' '.join(bar)
        elif s in vars:
            s = vars[s]
        ret.append(s)
        s = ''
    for c in raw:
        for k, v in literals.items():
            if v > 0:
                if c == k:
                    literals[k] = 3 - literals[k]
                    if literals[k] == 1:
                        s += c
                    break
                elif v == 1:
                    literals[k] = 0
                else:
                    s += c
                    break
        else:
            if c.isspace():
                append()
                s = ''
            else:
                s += c
            for k in literals:
                literals[k] = 2 if c == k else 0
    if s:
        append()
    return ret

def print_(s):
    if s:
        print(s)
        print()