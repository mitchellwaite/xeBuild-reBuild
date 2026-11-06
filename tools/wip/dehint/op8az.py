"""Attempt 8: dz1's asm goto without the macid memset feed, moved to every statement
position of applyIniOptions (and inside the inlined helpers' bodies is not tried).

python tools/wip/dehint/op8az.py [dz1|dz2] [-top N] [-show I -o out.c]
For dz1 the memset line and its asm goto are removed; for dz2 dualboot's asm goto."""
import os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

MEMSET = '\t\t\t\t\t__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));\n'
AG = {'dz1': '\t\t\t\t\t__asm__ goto ("" :::: dz1);\n', 'dz2': '\t\t\t\t__asm__ goto ("" :::: dz2);\n'}
HDR = 'void applyIniOptions(void)\n{\n'


def positions(t, which):
    assert AG[which] in t
    t = t.replace(AG[which], '')
    if which == 'dz1':
        t = t.replace(MEMSET, '')
    i = t.index(HDR) + len(HDR)
    j = t.index('\treturn;\n\t/* the dummy heap entries', i)
    lines = t[i:j].split('\n')
    pos = []
    off = i
    prev = '{'
    for k, l in enumerate(lines):
        s = l.strip()
        if s and not s.startswith(('/*', '*', '}', 'else', 'char ', 'int ')) and prev.endswith((';', '{', '}', '*/')):
            ind = l[:len(l) - len(l.lstrip('\t'))]
            pos.append((off, ind, s))
        if s:
            prev = s
        off += len(l) + 1
    return t, pos


def make(t, p, which):
    off, ind, _ = p
    return t[:off] + ind + '__asm__ goto ("" :::: %s);\n' % which + t[off:]


def main():
    a = sys.argv[1:]
    which = a[0] if a and a[0].startswith('dz') else 'dz1'
    base = optlib.read_src(os.path.join(optlib.R, 'src', 'options.c'))
    t, pos = positions(base, which)
    if '-show' in a:
        k = int(a[a.index('-show') + 1])
        txt = make(t, pos[k], which)
        if '-o' in a:
            open(a[a.index('-o') + 1], 'w', newline='\n').write(txt)
        print(optlib.fmt(optlib.score_text(txt)))
        return
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(lambda k: (k, optlib.score_text(make(t, pos[k], which))), range(len(pos))))
    print('none', optlib.fmt(optlib.score_text(t)))
    res.sort(key=lambda r: r[1].get('total', 99999) if not r[1].get('identical') else -1)
    for k, r in res[:int(a[a.index('-top') + 1]) if '-top' in a else 25]:
        print('%3d %-50s' % (k, pos[k][2][:50]), optlib.fmt(r))


if __name__ == '__main__':
    main()
