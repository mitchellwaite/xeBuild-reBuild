#!/usr/bin/env python3
"""Attempt 18: parseButtonX's z feed as ONE __builtin_constant_p test (1 trick instead of 2),
over test forms x positions in the chain (power expect kept).

python tools/wip/dehint/op18z.py [form:pos ..]   (no args: every form x position)"""
import itertools, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

SRC = optlib.read_src(optlib.SRC)
Z = '\t\tif (__builtin_constant_p(xb.xellButton + 1)) { if (__builtin_constant_p(xb.xellButton + 2) > 0) goto z; }\n'
assert Z in SRC
SRC = SRC.replace(Z, '', 1)
CP = '__builtin_constant_p(xb.xellButton + 1)'
FORMS = {'t': CP, 'gt0': CP + ' > 0', 'eq1': CP + ' == 1', 'ne1': CP + ' != 1', 'le0': CP + ' <= 0',
         'lt1': CP + ' < 1', 'ge1': CP + ' >= 1', 'not': '!' + CP, 'eq0': CP + ' == 0'}
RP = '\t\tif (!strnicmp(s, "remopower", 9))\n\t\t\tb = 0x20;\n'
RX = '\t\telse if (!strnicmp(s, "remox", 5))\n\t\t\tb = 0x22;\n'
WB = '\t\telse if (!strnicmp(s, "winbutton", 9))\n\t\t\tb = 0x24;\n'
PT = '\t\telse\n\t\t\tb = parseButtonPart(s, 0);\n'
PW = '\t\tb = 0x11;\n'
for x in (RP, RX, WB, PT, PW):
    assert x in SRC, x


def place(t, pos, test):
    g = 'if (%s) goto z;' % test
    if pos == 'head':
        return t.replace(RP, '\t\t' + g + '\n' + RP, 1)
    if pos == 'part':
        return t.replace(PT, '\t\telse {\n\t\t\t' + g + '\n\t\t\tb = parseButtonPart(s, 0);\n\t\t}\n', 1)
    if pos == 'pw':
        return t.replace(PW, PW + '\t\t' + g + '\n', 1)
    raise KeyError(pos)


POS = ('head', 'part', 'pw')


def run(c):
    f, p = c.split(':')
    t = place(SRC, p, FORMS[f])
    return c, optlib.score_text(t)


def main():
    cs = sys.argv[1:] or ['%s:%s' % (f, p) for f in FORMS for p in POS]
    if '-o' in cs:
        i = cs.index('-o'); out = cs[i + 1]; del cs[i:i + 2]
        f, p = cs[0].split(':')
        open(out, 'w', newline='\n').write(place(SRC, p, FORMS[f]))
    with ThreadPoolExecutor(6) as ex:
        for c, r in ex.map(run, cs):
            print('%-10s %s' % (c, optlib.fmt(r)[:160]), flush=True)


if __name__ == '__main__':
    main()
