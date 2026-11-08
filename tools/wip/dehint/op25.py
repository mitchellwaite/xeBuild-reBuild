#!/usr/bin/env python3
"""Attempt 25: the whole dummy group (dz1, dz2, both asm gotos, the macid memset, the rev
feeds) removed at once, then natural many-key levers on top.

python tools/wip/dehint/op25.py [-d] [-o out.c] [-v fn] variant ..
  a variant is names from V joined by `+`, applied in order to src/options.c; `dzall` is the
  group removal.  -d also writes p1/run.sh dumps under build/v/aio_p1/a25_<variant>
  (tags with `+` -> `_`)."""
import os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import optlib

R = optlib.R
SRC = open(optlib.SRC).read()

MS = '\t\t\t\t\t__builtin_memset(s, 0, __builtin_constant_p(xb.macid[1] + 9));\n'
AG1 = '\t\t\t\t\t__asm__ goto ("" :::: dz1);\n'
AG2 = '\t\t\t\t__asm__ goto ("" :::: dz2);\n'
i0 = SRC.index('\t\t\t/* dead feeds that key the dummies')
i1 = SRC.index('\t\t}\n\t}\n\treturn;\n\t/* the dummy heap')
FEEDS = SRC[i0:i1]
TAIL = SRC[i1:SRC.index('dz2:\n\t__builtin_unreachable();\n}\n') + len('dz2:\n\t__builtin_unreachable();\n}\n')]
for x in (MS, AG1, AG2, FEEDS, TAIL):
    assert SRC.count(x) == 1, x[:40]

V = {}


def rep(*pairs):
    return list(pairs)


V['base'] = []
V['dzall'] = rep((MS, ''), (AG1, ''), (AG2, ''), (FEEDS, ''), (TAIL, '\t\t}\n\t}\n}\n'))
# subsets: dz1 group only (memset, asm goto 1, dz1 label); dz2's feed then stands alone
V['dz2only_feed'] = rep((FEEDS, '\t\t\tif (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 15), 0)) { if (__builtin_expect(__builtin_constant_p(xb.blSuffix[1] + 16), 0)) goto dz2; }\n'))

# partial removals: one dummy group gone, the other fed alone
def X(n):
    return '__builtin_constant_p(xb.blSuffix[1] + %d)' % n


I3 = '\t\t\t'
T1 = 'dz1:\n\t__builtin_unreachable();\n}\n'
T2 = 'dz2:\n\t__builtin_unreachable();\n}\n'
TL = '\t\t}\n\t}\n\treturn;\n'
FD1 = {
    'a': I3 + 'if (%s) { if (__builtin_expect(%s, 0)) goto dz1; return; }\n' % (X(1), X(2)),
    'b': I3 + 'if (__builtin_expect(%s, 0)) goto dz1;\n' % X(1),
    'c': I3 + 'if (%s) { if (%s > 0) goto dz1; return; }\n' % (X(1), X(2)),
}
FD2 = {
    'a': I3 + 'if (__builtin_expect(%s, 0)) { if (__builtin_expect(%s, 0)) goto dz2; }\n' % (X(15), X(16)),
    'b': I3 + 'if (%s) { if (%s) goto dz2; return; }\n' % (X(1), X(2)) + I3 + 'if (__builtin_expect(%s, 0)) { if (__builtin_expect(%s, 0)) goto dz2; }\n' % (X(15), X(16)),
    'c': I3 + 'if (__builtin_expect(%s, 0)) goto dz2;\n' % X(15),
    'd': I3 + 'if (__builtin_expect(%s, 0)) { if (%s) goto dz2; return; }\n' % (X(15), X(16)),
}
# dz2's asm goto moved into the xellbutton / xellbutton2 traces (op25inj on nodz2a: a dummy
# pushed there works with keys -8..-19), so its feed can be a natural split
XL = '\t\t\t\tlog_printf(1, "default console DVD eject button is being used to start xell\\n");\n'
XS = '\t\t\t\txb.xellButton = 0x12;\n'
YL = '\t\t\tif (!xb.xellButton)\n\t\t\t\tlog_printf(1, "alternate xell button is disabled\\n");\n'
AGX = '\t\t\t\t__asm__ goto ("" :::: dz2);\n'
assert XL in SRC and XS in SRC and YL in SRC
POS = {
    'xa': [(XL, XL + AGX)],
    'xb': [(XL, AGX + XL)],
    'xc': [(XS, XS + AGX)],
    # between the xellbutton and xellbutton2 statements / at the end of xellbutton's block
    'xj': [(XS + '\t\t\t}\n\t\t}\n', XS + '\t\t\t}\n\t\t}\n\t\t__asm__ goto ("" :::: dz2);\n')],
    'xk': [(XS + '\t\t\t}\n\t\t}\n', XS + '\t\t\t}\n\t\t\t__asm__ goto ("" :::: dz2);\n\t\t}\n')],
    'ya': [(YL, '\t\t\tif (!xb.xellButton) {\n' + XL.replace('default console DVD eject button is being used to start xell', 'alternate xell button is disabled') + AGX + '\t\t\t}\n')],
    'yb': [(YL, '\t\t\tif (!xb.xellButton) {\n' + AGX + XL.replace('default console DVD eject button is being used to start xell', 'alternate xell button is disabled') + '\t\t\t}\n')],
}
AF = {'p': '{n1}', 'gt': '{n1} > 0', 'lt': '{n1} < 0', 'eq': '{n1} == 5', 'ne': '{n1} != 5'}
CF = {'p': '{n15}', 'gt': '{n15} > 0', 'lt': '{n15} < 0', 'eq': '{n15} == 5', 'ne': '{n15} != 5'}
DF = {'p': '{n16}', 'gt': '{n16} > 0', 'lt': '{n16} < 0', 'eq': '{n16} == 5', 'ne': '{n16} != 5'}


def fx(s):
    for i in range(40, 0, -1):
        s = s.replace('{n%d}' % i, X(i))
    return s


T21 = 'dz2:\n\t__builtin_unreachable();\ndz1:\n\t__builtin_unreachable();\n}\n'
for pn, pr in POS.items():
    for an, af in AF.items():
        for cn, cf in CF.items():
            for dn, df in DF.items():
                for arm in ('2', '1'):   # D's TRUE arm to dz2 or to dz1
                    for lo in ('12', '21'):
                        d = ('if (%s) goto dz2; goto dz1;' if arm == '2' else 'if (%s) goto dz1; goto dz2;') % df
                        f = fx(I3 + 'if (%s) { if ({n2}) goto dz1; return; }\n' % af + I3 + 'if (%s) { %s }\n' % (cf, d))
                        V['mv:%s:%s,%s,%s:%s%s' % (pn, an, cn, dn, arm, lo)] = rep((AG2, ''), *pr) + [(FEEDS, f), (TAIL, TL + (TAIL[len(TL):] if lo == '12' else T21))]

# one dummy for both asm gotos (dualboot's asm goto targets dz1)
for k, f in FD1.items():
    V['onedz' + k] = rep((AG2, AG2.replace('dz2', 'dz1')), (FEEDS, f), (TAIL, TL + T1))
for k, f in FD1.items():
    V['nodz2' + k] = rep((AG2, ''), (FEEDS, f), (TAIL, TL + T1))
for k, f in FD2.items():
    V['nodz1' + k] = rep((MS, ''), (AG1, ''), (FEEDS, f), (TAIL, TL + T2))

# --- levers (on top of dzall) ---
# macidSet's loop as do-while (x1.125 scale of applyIniOptions' counts)
MSET = 'int macidSet(void)\n{\n\tint i;\n\n\tfor (i = 0; i < 6; i++)\n\t\tif (xb.macid[i] != 0xff)\n\t\t\treturn 1;\n\treturn 0;\n}\n'
assert MSET in SRC
V['msdo'] = rep((MSET, 'int macidSet(void)\n{\n\tint i;\n\n\ti = 0;\n\tdo {\n\t\tif (xb.macid[i] != 0xff)\n\t\t\treturn 1;\n\t} while (++i < 6);\n\treturn 0;\n}\n'))
# OPT <-> optIniBoolG per site
SITES = {
    'nomobile': ('\tOPT("nomobile", 0x20000000, 0);\n', 0x20000000),
    'noremap': ('\tOPT("noremap", 0x40000000, 0);\n', 0x40000000),
    'noecdremap': ('\tif (!(xb.bootFlags & 0x80000000)) optIniBoolG("noecdremap", 0x80000000, 0, 0);\n', 0x80000000),
    'nandmu': ('\tif (!(xb.bootFlags & (0x10000000))) optIniBoolG("nandmu", 0x10000000, 0, 0);\n', 0x10000000),
    'nosecurity': ('\tif (!(xb.bootFlags & (0x4000000))) optIniBoolG("nosecurity", 0x4000000, 0, 0);\n', 0x4000000),
    'nosusecurity': ('\tOPT("nosusecurity", 0x1000000, 0);\n', 0x1000000),
    'smcnocheck': ('\tOPT("smcnocheck", 0x200000, 0);\n', 0x200000),
    'cygnos': ('\t\tif (!(xb.bootFlags & (1))) optIniBoolG("cygnos", 1, 0, 0);\n', 1),
    'demon': ('\t\tOPT("demon", 8, 0);\n', 8),
    'patchsmc': ('\t\tOPT("patchsmc", 0x8000000, 0);\n', 0x8000000),
    'smcnoeject': ('\t\tif (!(xb.bootFlags & (0x400000))) optIniBoolG("smcnoeject", 0x400000, 0, 0);\n', 0x400000),
    'smcnoblink': ('\t\tOPT("smcnoblink", 0x800000, 0);\n', 0x800000),
    'nodvd': ('\t\tOPT("nodvd", 2, 4);\n', 2),
}
for n, (line, bit) in SITES.items():
    assert line in SRC, n
    ind = line[:len(line) - len(line.lstrip('\t'))]
    clear = 4 if n == 'nodvd' else 0
    hx = '0x%x' % bit if bit > 9 else str(bit)
    g = '%sif (!(xb.bootFlags & (%s))) optIniBoolG("%s", %s, %d, 0);\n' % (ind, hx, n, hx, clear)
    o = '%sOPT("%s", %s, %d);\n' % (ind, n, hx, clear)
    V['f_' + n] = rep((line, o if 'optIniBoolG' in line else g))


def apply(text, names):
    for n in names.split('+'):
        for a, b in V[n]:
            assert a in text, (n, a[:50])
            text = text.replace(a, b, 1)
    return text


def run(names, dump=False, out=None, vfn=None):
    t = apply(SRC, names)
    if out:
        open(out, 'w', newline='\n').write(t)
    if vfn is not None:
        optlib.vdiff(t, only=vfn or None)
        return names, None
    r = optlib.score_text(t)
    s = 'IDENTICAL' if r.get('identical') else ('%s %s %s' % (r.get('total'), r.get('per'), ' '.join(r.get('notes', [])))) if 'total' in r else r
    if dump:
        tag = 'a25_' + names.replace('+', '_').replace(':', '-')
        p = os.path.join(optlib.BUILD, 'a25', tag + '.c')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', newline='\n').write(t)
        env = dict(os.environ, GFL='-O3 --param builtin-expect-probability=83')
        q = subprocess.run(['sh', os.path.join(R, 'tools', 'wip', 'aio', 'p1', 'run.sh'), p, tag],
                           capture_output=True, text=True, env=env)
        s += '  [dump %s: %s]' % (tag, q.stdout.strip().splitlines()[-1] if q.stdout.strip() else q.stderr[-200:])
    return names, s


if __name__ == '__main__':
    a = sys.argv[1:]
    a = [y for x in a for y in (open(x[1:]).read().split() if x.startswith('@') else [x])]
    if '-pre' in a:
        i = a.index('-pre'); p = a[i + 1]; del a[i:i + 2]
        a = [n for n in V if n.startswith(p)]
    dump = '-d' in a
    if dump:
        a.remove('-d')
    out = None
    if '-o' in a:
        i = a.index('-o'); out = a[i + 1]; del a[i:i + 2]
    vfn = None
    if '-v' in a:
        i = a.index('-v')
        vfn = a[i + 1] if i + 1 < len(a) and a[i + 1] not in V and '+' not in a[i + 1] else ''
        del a[i:i + (2 if vfn else 1)]
    if vfn is not None or out:
        for n in a:
            run(n, dump, out, vfn)
        sys.exit()
    with ThreadPoolExecutor(8) as ex:
        for n, s in ex.map(lambda n: run(n, dump), a):
            print('%-40s %s' % (n, s), flush=True)
