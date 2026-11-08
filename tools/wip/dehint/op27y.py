#!/usr/bin/env python3
"""Attempt 27: attempt 26's untried idea.  dz2 moves out of applyIniOptions into a private
copy of parseButton for xellbutton2 (parseButtonY), fed there; dualboot's asm goto goes and
the rev feeds keep only dz1 (attempt 25's nodz2a feed: 2 cp + 1 expect).  The replay map
(attempt 26, positions confirmed by attempt 27's controls) allows a dummy extracted from
xellbutton2's parseButton trace (198) with key -6..-8 or -12..-19; only 198 itself
(remopower, freq 17) has the count, so the feed sits in the power-failed arm.

python tools/wip/dehint/op27y.py [-d] [-m] [-o out.c] variant ..   (variants: see V)"""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib
import op23

SRC = open(optlib.SRC).read()
AG2 = '\t\t\t\t__asm__ goto ("" :::: dz2);\n'
i0 = SRC.index('\t\t\tif (__builtin_constant_p(xb.blSuffix[1] + 1))')
i1 = SRC.index('\t\t}\n\t}\n\treturn;\n\t/* the dummy heap')
FEEDS = SRC[i0:i1]
T12 = 'dz1:\n\t__builtin_unreachable();\ndz2:\n\t__builtin_unreachable();\n}\n'
T1 = 'dz1:\n\t__builtin_unreachable();\n}\n'
CALL2 = 'xb.xellAltButton = parseButton(getIniValue("xellbutton2"));'
PB = 'int parseButton(const char *s)\n{'
for x in (AG2, FEEDS, T12, CALL2, PB):
    assert SRC.count(x) == 1, x[:40]
X = lambda n: '__builtin_constant_p(xb.blSuffix[1] + %d)' % n
Y = lambda n: '__builtin_constant_p(xb.xellAltButton + %d)' % n
I3 = '\t\t\t'
FD1 = {
    'a': I3 + 'if (%s) { if (__builtin_expect(%s, 0)) goto dz1; return; }\n' % (X(1), X(2)),
    'b': I3 + 'if (__builtin_expect(%s, 0)) goto dz1;\n' % X(1),
}

NAMES = ('\tif (!strnicmp(s, "power", 5))\n\t\tb = 0x11;\n\telse if (!strnicmp(s, "remopower", 9))\n'
         '\t\tb = 0x20;\n\telse if (!strnicmp(s, "remox", 5))\n\t\tb = 0x22;\n'
         '\telse if (!strnicmp(s, "winbutton", 9))\n\t\tb = 0x24;\n\telse\n\t\tb = parseButtonPart(s, 0);\n')
assert NAMES in SRC


def pby(feed, where):
    """parseButtonY: parseButton with `feed` (a statement that may goto dz) placed at `where`"""
    if where == 'else':   # power failed, before remopower
        body = ('\tif (!strnicmp(s, "power", 5))\n\t\tb = 0x11;\n\telse {\n' + feed +
                '\t\tif (!strnicmp(s, "remopower", 9))\n\t\t\tb = 0x20;\n\t\telse if (!strnicmp(s, "remox", 5))\n'
                '\t\t\tb = 0x22;\n\t\telse if (!strnicmp(s, "winbutton", 9))\n\t\t\tb = 0x24;\n\t\telse\n'
                '\t\t\tb = parseButtonPart(s, 0);\n\t}\n')
    elif where == 'rx':   # remopower failed, before remox
        body = ('\tif (!strnicmp(s, "power", 5))\n\t\tb = 0x11;\n\telse if (!strnicmp(s, "remopower", 9))\n'
                '\t\tb = 0x20;\n\telse {\n' + feed + '\t\tif (!strnicmp(s, "remox", 5))\n'
                '\t\t\tb = 0x22;\n\t\telse if (!strnicmp(s, "winbutton", 9))\n\t\t\tb = 0x24;\n\t\telse\n'
                '\t\t\tb = parseButtonPart(s, 0);\n\t}\n')
    elif where == 'top':  # after the null test
        body = feed.replace('\t\t', '\t') + NAMES
    else:
        raise KeyError(where)
    return ('static int parseButtonY(const char *s)\n{\n\tint b = 0;\n\n\tif (!s)\n\t\treturn 0;\n' + body +
            '\treturn b;\ndz:\n\t__builtin_unreachable();\n}\n\n')


FEED2 = {
    'e1': '\t\tif (__builtin_expect(%s, 1)) goto dz;\n' % Y(1),
    'e0': '\t\tif (__builtin_expect(%s, 0)) goto dz;\n' % Y(1),
    'n2e': '\t\tif (%s) { if (__builtin_expect(%s, 1)) goto dz; }\n' % (Y(1), Y(2)),
    'n2r': '\t\tif (%s) { if (__builtin_expect(%s, 0)) goto dz; return 0; }\n' % (Y(1), Y(2)),
    'n2r1': '\t\tif (%s) { if (__builtin_expect(%s, 1)) goto dz; return 0; }\n' % (Y(1), Y(2)),
    'gt': '\t\tif (%s > 0) goto dz;\n' % Y(1),
}
AGY = '\t\t__asm__ goto ("" :::: dz);\n'
# with an asm goto (the dummy needs one to live until bbro: a block reached only by a dead
# feed is gone once the feed folds): asm goto + feed in one arm
for k in list(FEED2):
    FEED2['ag' + k] = AGY + FEED2[k]
    FEED2[k + 'ag'] = FEED2[k] + AGY
FEED2['ag'] = AGY

V = {}
for fk, fd in FD1.items():
    for gk, g in FEED2.items():
        for w in ('else', 'rx', 'top'):
            for pos in ('before', 'after'):
                V['y:%s:%s:%s:%s' % (fk, gk, w, pos)] = (fd, g, w, pos)


def build(name):
    fd, g, w, pos = V[name]
    t = SRC.replace(AG2, '', 1).replace(FEEDS, fd, 1).replace(T12, T1, 1)
    t = t.replace(CALL2, CALL2.replace('parseButton(', 'parseButtonY('), 1)
    f = pby(g, w)
    if pos == 'before':   # defined before parseButton
        t = t.replace(PB, f + PB, 1)
    else:                 # right before applyIniOptions
        k = t.index('void applyIniOptions(')
        k = t.rindex('\n\n', 0, k) + 2
        t = t[:k] + f + t[k:]
    return t


if __name__ == '__main__':
    a = sys.argv[1:]
    m = '-m' in a
    a = [x for x in a if x != '-m']
    out = None
    if '-o' in a:
        i = a.index('-o'); out = a[i + 1]; del a[i:i + 2]
    names = [n for x in a for n in V if n == x or (x.endswith('*') and n.startswith(x[:-1]))]

    def one(n):
        t = build(n)
        r = optlib.score_text(t)
        return n, optlib.fmt(r), (op23.metric(t, optlib.P83) if m else '')
    with ThreadPoolExecutor(6) as ex:
        for n, s, mm in ex.map(one, names):
            print('%-28s %s %s' % (n, s, mm), flush=True)
    if out:
        open(out, 'w', newline='\n').write(build(names[-1]))
