"""Attempt 12: move the static, fully inlined helpers (optIniBoolG, parseButtonX) to other
places in the file (cgraph order -> IPA inline order, inlined block indices), alone and with
each single trick removal of op12x.py.

python tools/wip/dehint/op12mv.py [rm ...]"""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib, op12x

SRC = optlib.read_src(optlib.SRC)


def cut(text, head, endmark='\n}\n'):
    """cut the function starting at head (with its comment block just above)"""
    i = text.index(head)
    c = text.rfind('/*', 0, i)
    if text[c:i].count('*/') == 1 and text[text.index('*/', c) + 2:i].strip() == '':
        i0 = c
    else:
        i0 = i
    j = text.index(endmark, i) + len(endmark)
    return text[:i0] + text[j:], text[i0:j]


ANCH = ['int baseFileExists(const char *name)', 'int perboxExists(const char *name)',
        'int iniConsoleType(void)', '/* a boolean option from a perbox file',
        'int optIniInt(const char *name', '/* applyIniOptions\' copy of parseButton',
        'int parseButton(const char *s)', 'void stripColons(char *s)', 'int macidSet(void)',
        '/* a boolean option given as name', '/* one name[=value]', '/* the ;-separated',
        '/* options from perbox files']
FUNCS = {'G': 'static _Bool optIniBoolG(', 'X': 'static int parseButtonX('}


def variants():
    out = {}
    for k, head in FUNCS.items():
        rest, fn = cut(SRC, head)
        for a in ANCH:
            if a not in rest:
                continue
            # a helper must come before its first use
            t = rest.replace(a, fn + '\n' + a, 1)
            if t.index(head) > t.index('void applyIniOptions(void)'):
                continue
            out['%s@%s' % (k, re.sub(r'\W+', '', a)[:14])] = t
    return out


def run(c):
    name, t, rm = c
    t2 = op12x.apply(t, rm, op12x.RM) if rm else t
    if t2 is None:
        return c[0], rm, {'compile': 'edit missing'}
    return name, rm, optlib.score_text(t2)


def main():
    rms = sys.argv[1:] or ['', 'rv2', 'rv2i', 'bxz', 'bxe', 'pbe', 'ms', 'dz2']
    vs = variants()
    combos = [(n, t, [r] if r else []) for n, t in vs.items() for r in rms]
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(run, combos))
    for n, rm, r in sorted(res, key=lambda x: x[2].get('total', 99999)):
        print('%-22s %-6s %s' % (n, ','.join(rm) or '-', optlib.fmt(r)[:150]))


if __name__ == '__main__':
    main()
